FROM python:3.11-slim-bookworm

WORKDIR /app

ENV PYTHONPATH=/app
ENV TORCH_HOME=/static/bert

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --default-timeout=1000 --retries 10 -r requirements.txt

COPY . .

CMD ["uvicorn", "backend.entry:app", "--host", "0.0.0.0", "--port", "8000"]