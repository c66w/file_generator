#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME=${IMAGE_NAME:-markdown-pdf}
CONTAINER_NAME=${CONTAINER_NAME:-markdown-pdf}

echo "Building image ${IMAGE_NAME}..."
docker build -t "${IMAGE_NAME}" .

if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}\$"; then
  echo "Removing existing container ${CONTAINER_NAME}..."
  docker rm -f "${CONTAINER_NAME}"
fi

echo "Starting container ${CONTAINER_NAME}..."
docker run -d --name "${CONTAINER_NAME}" -p 8000:8000 "${IMAGE_NAME}"

echo "Redeploy complete."
