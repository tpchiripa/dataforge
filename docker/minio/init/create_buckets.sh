#!/bin/sh

echo "Waiting for MinIO..."

until mc alias set local http://minio:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"
do
    sleep 2
done

echo "Creating DataForge buckets..."

mc mb local/bronze --ignore-existing
mc mb local/silver --ignore-existing
mc mb local/gold --ignore-existing
mc mb local/staging --ignore-existing
mc mb local/logs --ignore-existing
mc mb local/artifacts --ignore-existing

echo "Buckets created."

mc anonymous set none local/bronze
mc anonymous set none local/silver
mc anonymous set none local/gold
mc anonymous set none local/staging
mc anonymous set none local/logs
mc anonymous set none local/artifacts

echo "Bucket permissions configured."

exit 0
