#!/usr/bin/env bash
set -euo pipefail

REGION="${AWS_REGION:-us-west-2}"

echo "→ Deleting Lambda..."
aws lambda delete-function --function-name LogisticsQueryOffers --region "$REGION" 2>/dev/null || true

echo "→ Detaching IAM policies..."
aws iam detach-role-policy --role-name LogisticsLambdaRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole 2>/dev/null || true
aws iam detach-role-policy --role-name LogisticsLambdaRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBReadOnlyAccess 2>/dev/null || true

echo "→ Deleting IAM role..."
aws iam delete-role --role-name LogisticsLambdaRole 2>/dev/null || true

echo "→ Deleting DynamoDB table..."
aws dynamodb delete-table --table-name LogisticsOffers --region "$REGION" 2>/dev/null || true

echo "✓ Teardown complete."
