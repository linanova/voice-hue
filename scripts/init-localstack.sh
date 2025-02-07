#!/bin/bash

echo "Initializing DynamoDB tables in LocalStack"

aws --endpoint-url=http://localhost:4566 dynamodb create-table \
    --table-name voice-hue-api-keys \
    --attribute-definitions \
        AttributeName=api_key,AttributeType=S \
    --key-schema \
        AttributeName=api_key,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
    --no-cli-pager

aws --endpoint-url=http://localhost:4566 dynamodb put-item \
    --table-name voice-hue-api-keys \
    --item \
        '{"api_key": {"S": "1234567890"}, "client_id": {"S": "client123"}}'

aws --endpoint-url=http://localhost:4566 dynamodb create-table \
    --table-name voice-hue-commands \
    --attribute-definitions \
        AttributeName=pk,AttributeType=S \
        AttributeName=sk,AttributeType=S \
    --key-schema \
        AttributeName=pk,KeyType=HASH \
        AttributeName=sk,KeyType=RANGE \
    --provisioned-throughput \
        ReadCapacityUnits=5,WriteCapacityUnits=5 \
    --no-cli-pager

echo "Tables initialized"
