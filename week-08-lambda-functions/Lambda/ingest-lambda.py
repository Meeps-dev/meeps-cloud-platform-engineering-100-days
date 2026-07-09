import base64
import json
import logging
import os
import re
import uuid
from datetime import datetime, timezone
from urllib.parse import unquote

import boto3 # type: ignore

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

TABLE_NAME = os.environ["TABLE_NAME"]
BUCKET_NAME = os.environ["BUCKET_NAME"]

table = dynamodb.Table(TABLE_NAME)


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body, default=str)
    }


def safe_file_name(file_name):
    file_name = file_name.split("/")[-1].split("\\")[-1]
    cleaned = re.sub(r"[^A-Za-z0-9._-]", "-", file_name)
    return cleaned or "upload.txt"


def parse_body(event):
    raw_body = event.get("body") or "{}"

    if event.get("isBase64Encoded"):
        raw_body = base64.b64decode(raw_body).decode("utf-8")

    return json.loads(raw_body)


def lambda_handler(event, context):
    logger.info("API event received: %s", json.dumps(event))

    method = event.get("requestContext", {}).get("http", {}).get("method", "")
    raw_path = event.get("rawPath", "")

    if method == "GET" and raw_path == "/health":
        return response(200, {
            "status": "ok",
            "service": "meeps-week8-api",
            "week": 8
        })

    if method == "GET" and raw_path == "/files":
        result = table.scan(Limit=50)
        items = result.get("Items", [])

        return response(200, {
            "count": len(items),
            "items": items
        })

    if method == "GET" and raw_path.startswith("/files/"):
        file_id = unquote(raw_path.replace("/files/", "", 1))

        result = table.get_item(
            Key={
                "fileId": file_id
            }
        )

        item = result.get("Item")

        if not item:
            return response(404, {
                "message": "File metadata not found",
                "fileId": file_id
            })

        return response(200, item)

    if method == "POST" and raw_path == "/files":
        body = parse_body(event)

        file_name = safe_file_name(body.get("fileName", "upload.txt"))
        content_type = body.get("contentType", "text/plain")

        if "contentBase64" in body:
            file_bytes = base64.b64decode(body["contentBase64"])
        else:
            file_bytes = str(body.get("content", "")).encode("utf-8")

        job_id = str(uuid.uuid4())
        object_key = f"uploads/{job_id}-{file_name}"

        logger.info("Uploading file to S3: bucket=%s key=%s", BUCKET_NAME, object_key)

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=object_key,
            Body=file_bytes,
            ContentType=content_type
        )

        now = datetime.now(timezone.utc).isoformat()

        item = {
            "fileId": object_key,
            "jobId": job_id,
            "bucket": BUCKET_NAME,
            "key": object_key,
            "originalFileName": file_name,
            "size": len(file_bytes),
            "status": "uploaded",
            "createdAt": now,
            "updatedAt": now,
            "project": os.environ.get("PROJECT", "meeps"),
            "environment": os.environ.get("ENVIRONMENT", "dev")
        }

        table.put_item(Item=item)

        logger.info("Initial metadata written to DynamoDB: %s", object_key)

        return response(202, {
            "message": "File accepted for processing",
            "jobId": job_id,
            "fileId": object_key,
            "bucket": BUCKET_NAME,
            "key": object_key,
            "status": "uploaded"
        })

    return response(404, {
        "message": "Route not found",
        "method": method,
        "path": raw_path
    })