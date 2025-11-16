#!/bin/bash
# Build and push Docker image for AMD64 platform (Civo Kubernetes)

set -e

IMAGE_NAME="docker.io/joelofelectronics/llm-agent-app"
TAG="latest"

echo "Building Docker image for linux/amd64 platform..."
echo "Image: ${IMAGE_NAME}:${TAG}"
echo ""

# Build for AMD64 (Civo cluster architecture)
docker buildx build \
  --platform linux/amd64 \
  -t "${IMAGE_NAME}:${TAG}" \
  --push \
  .

echo ""
echo "Image built and pushed successfully!"
echo ""
echo "Image: ${IMAGE_NAME}:${TAG}"
echo ""
echo "To verify the image was pushed:"
echo "  docker pull ${IMAGE_NAME}:${TAG}"
echo ""
echo "To trigger Kubernetes to pull the new image:"
echo "  kubectl rollout restart deployment app -n apps"

