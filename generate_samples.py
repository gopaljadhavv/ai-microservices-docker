import base64
import json
import os
from pathlib import Path
import time
import requests


AI_URL = os.getenv("AI_SERVICE_URL", "http://localhost:8001/detect/")
SAMPLES_DIR = Path("sample_data")
OUTPUT_DIR = Path("demo_outputs")


def encode_image(path: Path) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def save_outputs(filename: str, result: dict):
    OUTPUT_DIR.mkdir(exist_ok=True)
    name = Path(filename).stem
    # save json
    json_path = OUTPUT_DIR / f"{name}_results.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    # save image
    if result.get("image"):
        img_bytes = base64.b64decode(result["image"])
        img_path = OUTPUT_DIR / f"{name}_detected.jpg"
        with open(img_path, "wb") as f:
            f.write(img_bytes)
    return True


def main():
    images = [p for p in SAMPLES_DIR.glob("*.*") if p.suffix.lower() in {".jpg", ".jpeg", ".png"}]
    if not images:
        print("No images found in sample_data/")
        return

    summary = []
    for img in images:
        print(f"Processing {img.name} ...")
        payload = {"image": encode_image(img), "image_path": img.name}
        r = requests.post(AI_URL, json=payload, timeout=60)
        r.raise_for_status()
        result = r.json()
        save_outputs(img.name, result)
        summary.append({"file": img.name, "count": result.get("count", 0)})
        time.sleep(0.2)

    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(OUTPUT_DIR / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print("Done. Outputs saved to demo_outputs/")


if __name__ == "__main__":
    main()


