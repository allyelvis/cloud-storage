#!/bin/bash

echo "Starting Deployment..."
docker-compose -f infra/docker-compose.yml up -d --build

echo "Initializing MinIO bucket..."
sleep 5
docker exec $(docker ps -qf "ancestor=minio") mc alias set local http://minio:9000 admin password
docker exec $(docker ps -qf "ancestor=minio") mc mb local/cloud-storage || true

echo "Deployment Complete!"
