import json
from typing import Any

from app.config import settings

# R2 is optional — if credentials are "local", skip R2 entirely
_R2_ENABLED = settings.R2_ACCOUNT_ID not in ("local", "", None)


def _get_r2_client() -> Any:
    import boto3
    return boto3.client(
        "s3",
        endpoint_url=f"https://{settings.R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
        aws_access_key_id=settings.R2_ACCESS_KEY_ID,
        aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
        region_name="auto",
    )


def fetch_chapter_body(r2_key: str) -> dict[str, Any]:
    """Fetch chapter JSON from Cloudflare R2. Returns empty dict when R2 not configured."""
    if not _R2_ENABLED:
        return {}
    from botocore.exceptions import ClientError
    client = _get_r2_client()
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
    """Upload chapter JSON to Cloudflare R2. No-op when R2 not configured."""
    if not _R2_ENABLED:
        return
    client = _get_r2_client()
    client.put_object(
        Bucket=settings.R2_BUCKET_NAME,
        Key=r2_key,
        Body=json.dumps(data, ensure_ascii=False),
        ContentType="application/json",
    )
