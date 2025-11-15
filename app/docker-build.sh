#!/bin/bash

# Docker build and test script for AI Agent App

set -e

IMAGE_NAME="llm-agent-app"
IMAGE_TAG="latest"
CONTAINER_NAME="llm-agent-test"
ENV_FILE=".env"

echo "Building Docker image..."
docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .

echo "Build complete!"
echo ""
echo "   Environment Setup:"
if [ ! -f "${ENV_FILE}" ]; then
    echo "   ${ENV_FILE} not found!"
    echo "   Copy env.example to ${ENV_FILE} and update with your values:"
    echo "   cp env.example ${ENV_FILE}"
    echo ""
    echo "   Or run without env file (will use defaults):"
    echo "      docker run -d --name ${CONTAINER_NAME} -p 8080:80 ${IMAGE_NAME}:${IMAGE_TAG}"
else
    echo "   Found ${ENV_FILE}"
    echo ""
    echo "   To test the container with environment variables:"
    echo "   docker run -d --name ${CONTAINER_NAME} -p 8080:80 --env-file ${ENV_FILE} ${IMAGE_NAME}:${IMAGE_TAG}"
fi
echo ""
echo "   Then visit: http://localhost:8080"
echo ""
echo "   To view logs:"
echo "   docker logs -f ${CONTAINER_NAME}"
echo ""
echo "   To stop and remove:"
echo "   docker stop ${CONTAINER_NAME} && docker rm ${CONTAINER_NAME}"
