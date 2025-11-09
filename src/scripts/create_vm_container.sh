#!/bin/bash

# Script to create a VM container for a machine
# Usage: ./scripts/create_vm_container.sh <machine_id>

set -e  # Exit on error

MACHINE_ID=$1
IMAGE_NAME="smartfactory_vm:latest"
CONTAINER_NAME="vm_${MACHINE_ID}"
NETWORK_NAME="smart_factory_network"
BACKEND_URL="http://backend_api:8000/api/metrics/insert"

# Validate machine ID
if [ -z "$MACHINE_ID" ]; then
    echo "Error: Machine ID is required"
    echo "Usage: $0 <machine_id>"
    exit 1
fi

# Check if image exists, build if not
if ! docker image inspect $IMAGE_NAME >/dev/null 2>&1; then
    echo "Image $IMAGE_NAME not found. Building..."
    docker build -f Dockerfile.vm -t $IMAGE_NAME .
    echo "Image built successfully"
else
    echo "Image $IMAGE_NAME already exists"
fi

# Check if container already exists
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "Container $CONTAINER_NAME already exists. Removing..."
    docker rm -f $CONTAINER_NAME
fi

# Create and start the container
echo "Creating container $CONTAINER_NAME..."
docker run -d \
    --name $CONTAINER_NAME \
    --network $NETWORK_NAME \
    --restart always \
    -e MACHINE_ID=$MACHINE_ID \
    -e METRICS_ENDPOINT=$BACKEND_URL \
    $IMAGE_NAME

echo "✅ Container $CONTAINER_NAME created successfully"
docker ps --filter "name=$CONTAINER_NAME"delete_vm_container.sh