#!/usr/bin/env bash
set -euo pipefail

REGION="${AWS_REGION:-us-west-2}"
MODEL_ID="us.anthropic.claude-sonnet-4-6"

echo "→ Checking AWS credentials..."
CALLER_ARN=$(aws sts get-caller-identity --query Arn --output text)
echo "  Calling as: $CALLER_ARN"

if [[ "$CALLER_ARN" == *":root" ]]; then
  echo "  ❌ STOP. You are using root credentials. Switch to an IAM user."
  exit 1
fi

echo ""
echo "→ Test-invoking Bedrock ($MODEL_ID in $REGION)..."
if aws bedrock-runtime converse \
     --region "$REGION" \
     --model-id "$MODEL_ID" \
     --messages '[{"role":"user","content":[{"text":"Say OK"}]}]' \
     --inference-config 'maxTokens=10' \
     --output json > /tmp/bedrock_test.json 2>&1; then
  echo "  ✓ Bedrock invocation succeeded."
else
  echo ""
  echo "  ❌ Bedrock invocation failed. Likely causes:"
  echo "     1. Model access not yet enabled (Phase 0.3)"
  echo "     2. Wrong region (expected: us-west-2)"
  echo ""
  echo "  Fix: Console → Bedrock (us-west-2) → Model access → enable Claude Sonnet 4.6"
  echo ""
  echo "  Raw error:"
  cat /tmp/bedrock_test.json
  exit 1
fi

echo ""
echo "✓ All pre-flight checks passed."
