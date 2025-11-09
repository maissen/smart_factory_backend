#!/bin/bash

# Script to delete a VM container
# Usage: ./scripts/delete_vm_container.sh <machine_id>

set -e

MACHINE_ID=$1
CONTAINER_NAME="vm_${MACHINE_ID}"

if [ -z "$MACHINE_ID" ]; then
    echo "Error: Machine ID is required"
    echo "Usage: $0 <machine_id>"
    exit 1
fi

if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "Stopping and removing container $CONTAINER_NAME..."
    docker kill $CONTAINER_NAME 2>/dev/null || true
    docker rm -f $CONTAINER_NAME
    echo "✅ Container $CONTAINER_NAME removed successfully"
else
    echo "⚠️  Container $CONTAINER_NAME not found"
fi