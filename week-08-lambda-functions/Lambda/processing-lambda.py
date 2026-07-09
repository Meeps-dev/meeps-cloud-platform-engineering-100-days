import json
import logging
import os
import time
from datetime import datetime, timezone
from urllib.parse import unquote_plus

import boto3 # type: ignore

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")
sns = boto3.client("sns")
dynamodb = boto3.resource("dynamodb")

TABLE_NAME = os.environ["TABLE_NAME"]
TOPIC_ARN = os.environ["TOPIC_ARN"]

table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    logger.info("SQS event received: %s", json.dumps(event))

    records = event.get("Records", [])

    for sqs_record in records:
        body = json.loads(sqs_record["body"])

        logger.info("EventBridge message body: %s", json.dumps(body))

        detail = body.get("detail", {})
        bucket_name = detail.get("bucket", {}).get("name")
        object_key = detail.get("object", {}).get("key")
        object_size = detail.get("object", {}).get("size", 0)
        event_name = body.get("detail-type", "unknown")

        if not bucket_name or not object_key:
            raise ValueError("Missing bucket or object key in EventBridge event")

        object_key = unquote_plus(object_key)

        if not object_key.startswith("uploads/"):
            logger.info("Skipping object outside uploads prefix: %s", object_key)
            continue

        if "fail" in object_key.lower():
            raise Exception(f"Intentional failure test for key: {object_key}")

        if "slow" in object_key.lower():
            logger.info("Intentional timeout test started")
            time.sleep(10)

        logger.info("Reading uploaded file: s3://%s/%s", bucket_name, object_key)

        s3_object = s3.get_object(
            Bucket=bucket_name,
            Key=object_key
        )

        file_bytes = s3_object["Body"].read()
        preview = file_bytes[:200].decode("utf-8", errors="replace")

        processed_at = datetime.now(timezone.utc).isoformat()
        processed_key = object_key.replace("uploads/", "processed/", 1) + ".summary.json"

        processed_output = {
            "fileId": object_key,
            "bucket": bucket_name,
            "sourceKey": object_key,
            "processedKey": processed_key,
            "sourceSize": object_size,
            "preview": preview,
            "status": "processed",
            "processedAt": processed_at
        }

        s3.put_object(
            Bucket=bucket_name,
            Key=processed_key,
            Body=json.dumps(processed_output, indent=2).encode("utf-8"),
            ContentType="application/json"
        )

        logger.info("Processed output written: s3://%s/%s", bucket_name, processed_key)

        table.update_item(
            Key={
                "fileId": object_key
            },
            UpdateExpression="""
                SET #status = :status,
                    processedAt = :processedAt,
                    updatedAt = :updatedAt,
                    processedKey = :processedKey,
                    eventName = :eventName,
                    objectSize = :objectSize
            """,
            ExpressionAttributeNames={
                "#status": "status"
            },
            ExpressionAttributeValues={
                ":status": "processed",
                ":processedAt": processed_at,
                ":updatedAt": processed_at,
                ":processedKey": processed_key,
                ":eventName": event_name,
                ":objectSize": object_size
            }
        )

        logger.info("DynamoDB metadata updated for fileId: %s", object_key)

        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject="Meeps Week 8 file processed",
            Message=json.dumps({
                "message": "File processed successfully",
                "fileId": object_key,
                "bucket": bucket_name,
                "processedKey": processed_key,
                "processedAt": processed_at
            }, indent=2)
        )

        logger.info("SNS notification published for fileId: %s", object_key)

    return {
        "message": "SQS messages processed",
        "processedCount": len(records)
    }