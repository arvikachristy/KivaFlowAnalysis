FROM python:latest

COPY ingest /workspace/ingest/
COPY setup.py /workspace
WORKDIR /workspace

RUN pip install -e .

ENTRYPOINT ["gunicorn", "-w", "4", "-b", "0.0.0.0:4000", "ingest.app:app"]
