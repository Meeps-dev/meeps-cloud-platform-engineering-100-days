import json
import logging
import os
from collections import Counter

import boto3  # type: ignore

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    logger.info("Scheduled event received: %s", json.dumps(event))

    result = table.scan(
        ProjectionExpression="#status",
        ExpressionAttributeNames={
            "#status": "status"
        }
    )

    items = result.get("Items", [])
    counts = Counter(item.get("status", "unknown") for item in items)

    summary = {
        "message": "Meeps Week 8 scheduled summary",
        "totalItems": len(items),
        "statusCounts": dict(counts)
    }

    logger.info("Summary: %s", json.dumps(summary))

    return summary