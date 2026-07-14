#!/bin/sh

mc alias set local http://minio:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD" >/dev/null 2>&1

mc ls local >/dev/null 2>&1

exit $?
