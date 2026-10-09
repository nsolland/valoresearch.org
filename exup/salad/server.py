import asyncio
import hashlib
import io
import os
import statistics
from pathlib import Path

import numpy as np
import torch
from fastapi import FastAPI, File, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError
from ultralytics import YOLO
from ultralytics.data.converter import coco80_to_coco91_class

MODEL_PATH = Path(os.environ.get("EXUP_MODEL", "/opt/exup/yolo11n.pt"))
EXPECTED_MODEL_SHA256 = os.environ.get(
    "EXUP_EXPECTED_MODEL_SHA256",
    "0ebbc80d4a7680d14987a577cd21342b65ecfd94632bd9a8da63ae6417644ee1",
)
DEVICE = os.environ.get("EXUP_DEVICE", "0")
REQUIRE_CUDA = os.environ.get("EXUP_REQUIRE_CUDA", "1").lower() not in {"0", "false", "no"}

app = FastAPI(title="EXUP-PUBLIC-01 inference", docs_url=None, redoc_url=None)
_model = None
_category_map = coco80_to_coco91_class()
_inference_ms = []
_request_count = 0
_error_count = 0
_model_lock = asyncio.Lock()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


@app.on_event("startup")
def load_model():
    global _model
    if not MODEL_PATH.is_file():
        raise RuntimeError(f"model file is missing: {MODEL_PATH}")
    actual_sha = sha256_file(MODEL_PATH)
    if actual_sha != EXPECTED_MODEL_SHA256:
        raise RuntimeError(f"model SHA-256 mismatch: {actual_sha}")
    if REQUIRE_CUDA and not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for this Salad deployment but is unavailable")
    if torch.cuda.is_available():
        torch.cuda.set_device(int(DEVICE))
    _model = YOLO(str(MODEL_PATH))


@app.get("/healthz")
def healthz():
    if _model is None:
        raise HTTPException(status_code=503, detail="model is not ready")
    return {
        "status": "ready",
        "case_id": "EXUP-PUBLIC-01",
        "model_sha256": EXPECTED_MODEL_SHA256,
        "device": f"cuda:{DEVICE}" if torch.cuda.is_available() else "cpu",
        "gpu": torch.cuda.get_device_name(int(DEVICE)) if torch.cuda.is_available() else None,
    }


@app.get("/stats")
def stats():
    values = sorted(_inference_ms)
    p50 = statistics.median(values) if values else None
    p95 = values[max(0, int(len(values) * 0.95) - 1)] if values else None
    return {
        "completed_requests": _request_count,
        "failed_requests": _error_count,
        "inference_p50_ms": p50,
        "inference_p95_ms": p95,
        "stored_inputs_or_outputs": False,
    }


@app.post("/v1/predict")
async def predict(image_id: int, file: UploadFile = File(...)):
    global _request_count, _error_count
    if image_id < 0:
        raise HTTPException(status_code=400, detail="image_id must be non-negative")
    if _model is None:
        raise HTTPException(status_code=503, detail="model is not ready")
    try:
        raw = await file.read()
        image = Image.open(io.BytesIO(raw)).convert("RGB")
        array = np.asarray(image)
    except (UnidentifiedImageError, OSError, ValueError):
        _error_count += 1
        raise HTTPException(status_code=400, detail="invalid image")
    finally:
        await file.close()
    try:
        async with _model_lock:
            results = _model.predict(
                source=array,
                imgsz=640,
                conf=0.001,
                iou=0.7,
                device=DEVICE,
                batch=1,
                verbose=False,
            )
        result = results[0]
        rows = []
        if result.boxes is not None:
            boxes = result.boxes.xyxy.cpu().numpy()
            scores = result.boxes.conf.cpu().numpy()
            classes = result.boxes.cls.cpu().numpy().astype(int)
            for box, score, cls in zip(boxes, scores, classes):
                x1, y1, x2, y2 = map(float, box)
                rows.append({
                    "image_id": image_id,
                    "category_id": int(_category_map[cls]),
                    "bbox": [x1, y1, x2 - x1, y2 - y1],
                    "score": float(score),
                })
        _request_count += 1
        inference_ms = float(result.speed.get("inference", 0.0))
        _inference_ms.append(inference_ms)
        return {"image_id": image_id, "detections": rows, "inference_ms": inference_ms}
    except Exception as exc:
        _error_count += 1
        raise HTTPException(status_code=500, detail=f"inference failed: {type(exc).__name__}") from exc
