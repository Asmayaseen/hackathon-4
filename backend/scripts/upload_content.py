"""
Upload chapter JSON files from content/chapters/*.json to Cloudflare R2.
Run from backend/ directory: python scripts/upload_content.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import settings
from app.r2_client import upload_chapter_body


def main():
    content_dir = Path(__file__).parent.parent / "content" / "chapters"
    if not content_dir.exists():
        print(f"Content directory not found: {content_dir}")
        print("Create content/chapters/ and add chapter JSON files first.")
        sys.exit(1)

    files = sorted(content_dir.glob("*.json"))
    if not files:
        print("No JSON files found in content/chapters/")
        sys.exit(1)

    print(f"Uploading {len(files)} chapter files to R2 bucket: {settings.R2_BUCKET_NAME}")

    for f in files:
        with open(f) as fp:
            data = json.load(fp)

        order_index = data.get("chapter_id") or data.get("order_index")
        slug = f.stem
        r2_key = f"chapters/{order_index}/{slug}.json"

        upload_chapter_body(r2_key, data)
        print(f"  ✓ Uploaded {f.name} → {r2_key}")

    print("Upload complete.")


if __name__ == "__main__":
    main()
