#!/usr/bin/env bash
set -euo pipefail

REGION="${AWS_REGION:-us-west-2}"
LAMBDA_NAME="${LAMBDA_NAME:-LogisticsQueryOffers}"
TABLE="${DDB_TABLE:-LogisticsOffers}"

echo "→ Test 1: DynamoDB item count"
COUNT=$(aws dynamodb scan --table-name "$TABLE" --select COUNT \
        --region "$REGION" --query Count --output text)
echo "  Items: $COUNT"
[ "$COUNT" -gt 0 ] || { echo "  ❌ Empty table"; exit 1; }

echo ""
echo "→ Test 2: Lambda invocation (origin=Mombasa)"
aws lambda invoke \
  --function-name "$LAMBDA_NAME" \
  --region "$REGION" \
  --payload '{"origin":"Mombasa"}' \
  --cli-binary-format raw-in-base64-out \
  /tmp/resp.json >/dev/null
python -m json.tool < /tmp/resp.json

echo ""
echo "✓ All checks passed."
