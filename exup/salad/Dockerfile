FROM pytorch/pytorch:2.13.0-cuda13.2-cudnn9-runtime

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    YOLO_CONFIG_DIR=/tmp/ultralytics \
    EXUP_MODEL=/opt/exup/yolo11n.pt \
    EXUP_EXPECTED_MODEL_SHA256=0ebbc80d4a7680d14987a577cd21342b65ecfd94632bd9a8da63ae6417644ee1 \
    EXUP_REQUIRE_CUDA=1 \
    EXUP_DEVICE=0

WORKDIR /opt/exup
COPY requirements.txt ./requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt \
    && python -c "from urllib.request import urlretrieve; urlretrieve('https://huggingface.co/Ultralytics/YOLO11/resolve/main/yolo11n.pt', '/opt/exup/yolo11n.pt')" \
    && echo '0ebbc80d4a7680d14987a577cd21342b65ecfd94632bd9a8da63ae6417644ee1  /opt/exup/yolo11n.pt' | sha256sum -c -
COPY server.py ./server.py
EXPOSE 8000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--no-access-log"]
