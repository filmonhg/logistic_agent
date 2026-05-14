# Install AWS CLI
brew install awscli

# Configure your profile (only the credentials part needs interaction)
aws configure --profile logistics-dev
#   AWS Access Key ID:     <from IAM Console>
#   AWS Secret Access Key: <from IAM Console>
#   Default region:        us-west-2
#   Output format:         json

# Pin profile + region for this shell
export AWS_PROFILE=logistics-dev
export AWS_REGION=us-west-2

# Verify
aws sts get-caller-identity
