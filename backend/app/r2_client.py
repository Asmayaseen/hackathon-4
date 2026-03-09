import json
from typing import Any

import boto3
from botocore.exceptions import ClientError

from app.config import settings


def get_r2_client() -> Any:
    return boto3.client(
        "s3",
        endpoint_url=f"https://{settings.R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
        aws_access_key_id=settings.R2_ACCESS_KEY_ID,
        aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
        region_name="auto",
    )


def fetch_chapter_body(r2_key: str) -> dict[str, Any]:
    """Fetch chapter JSON from Cloudflare R2. Returns dict with body, word_count."""
    client = get_r2_client()
    try:
        response = client.get_object(Bucket=settings.R2_BUCKET_NAME, Key=r2_key)
        content = response["Body"].read().decode("utf-8")
        return json.loads(content)
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "NoSuchKey":
            return {"body": "", "word_count": 0, "error": "not_found"}
        raise


def upload_chapter_body(r2_key: str, data: dict[str, Any]) -> None:
    """Upload chapter JSON to Cloudflare R2."""
    client = get_r2_client()
    client.put_object(
        Bucket=settings.R2_BUCKET_NAME,
        Key=r2_key,
        Body=json.dumps(data, ensure_ascii=False),
        ContentType="application/json",
    )
