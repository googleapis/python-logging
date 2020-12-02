FROM python:3.7-slim

# This Dockerfile must be built at the repo root

# show python logs as they occur
ENV PYTHONUNBUFFERED=0

# Install test code dependencies.
COPY tests/environments/test-code/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Add test scripts.
COPY tests/environments/test-code/*.py /app/

# install logging from local directory.
WORKDIR /app
ENV PATH="/app:${PATH}"
COPY . /app/python-logging
RUN pip install -e /app/python-logging

# Start script
CMD python router.py
