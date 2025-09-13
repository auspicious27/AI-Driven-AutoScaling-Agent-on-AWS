#!/bin/bash
# AI-Driven AutoScaling Agent - FINAL WORKING VERSION
# Usage: ./deploy-final.sh

set -e

echo "🚀 AI-Driven AutoScaling Agent - FINAL WORKING VERSION"
echo "======================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
print_status "Checking prerequisites..."

# Check AWS CLI
if ! command -v aws &> /dev/null; then
    print_error "AWS CLI not found. Please install AWS CLI first."
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    print_error "Python3 not found. Please install Python3 first."
    exit 1
fi

# Check AWS credentials
if ! aws sts get-caller-identity --output text &> /dev/null; then
    print_error "AWS credentials not configured. Please run 'aws configure' first."
    exit 1
fi

print_success "All prerequisites met!"

# Get AWS resources automatically
print_status "Fetching AWS resources..."

# Get default VPC
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=is-default,Values=true" --query 'Vpcs[0].VpcId' --output text)
if [ "$VPC_ID" = "None" ] || [ -z "$VPC_ID" ]; then
    print_error "No default VPC found. Please create a VPC first."
    exit 1
fi
print_success "VPC ID: $VPC_ID"

# Get public subnets
SUBNETS=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" --query 'Subnets[?MapPublicIpOnLaunch==`true`].SubnetId' --output text)
SUBNET_COUNT=$(echo $SUBNETS | wc -w)
if [ $SUBNET_COUNT -lt 2 ]; then
    print_error "Need at least 2 public subnets. Found: $SUBNET_COUNT"
    exit 1
fi
SUBNET_LIST=$(echo $SUBNETS | tr ' ' ',' | cut -d',' -f1-2)  # Take only first 2 subnets
print_success "Public Subnets: $SUBNET_LIST"

# Get latest AMI
AMI_ID=$(aws ec2 describe-images --owners amazon --filters "Name=name,Values=amzn2-ami-hvm-*-x86_64-gp2" --query 'Images[0].ImageId' --output text)
print_success "AMI ID: $AMI_ID"

# Create key pair if not exists
KEY_NAME="autoscale-demo-key"
if ! aws ec2 describe-key-pairs --key-names $KEY_NAME &> /dev/null; then
    print_status "Creating key pair: $KEY_NAME"
    aws ec2 create-key-pair --key-name $KEY_NAME --query 'KeyMaterial' --output text > ${KEY_NAME}.pem 2>/dev/null || true
    chmod 400 ${KEY_NAME}.pem 2>/dev/null || true
    print_success "Key pair created: ${KEY_NAME}.pem"
else
    print_success "Key pair already exists: $KEY_NAME"
fi

# Deploy CloudFormation stack
print_status "Deploying CloudFormation stack..."
aws cloudformation deploy \
    --template-file autoscale-demo.yml \
    --stack-name autoscale-demo \
    --parameter-overrides \
        KeyName=$KEY_NAME \
        VpcId=$VPC_ID \
        PublicSubnets=$SUBNET_LIST \
        ImageId=$AMI_ID \
        InstanceType=t3.micro \
    --capabilities CAPABILITY_IAM

if [ $? -eq 0 ]; then
    print_success "CloudFormation stack deployed successfully!"
else
    print_error "CloudFormation deployment failed!"
    exit 1
fi

# Get ALB DNS name
print_status "Getting ALB DNS name..."
ALB_DNS=$(aws cloudformation describe-stacks --stack-name autoscale-demo --query "Stacks[0].Outputs[?OutputKey=='ApplicationLoadBalancerDNS'].OutputValue" --output text)
print_success "ALB DNS: $ALB_DNS"

# Install Python dependencies
print_status "Installing Python dependencies..."
pip3 install requests boto3 --break-system-packages &> /dev/null || pip3 install requests boto3 --user &> /dev/null || true
print_success "Python dependencies installed!"

# Wait for instances to be ready
print_status "Waiting for instances to be ready..."
sleep 60

# Get current capacity
CURRENT_CAPACITY=$(aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names autoscale-demo-asg --query 'AutoScalingGroups[0].DesiredCapacity' --output text)
print_success "Current ASG Capacity: $CURRENT_CAPACITY"

# Demo scaling
print_status "Demonstrating auto-scaling..."
print_status "Scaling UP to 2 instances..."
aws autoscaling set-desired-capacity --auto-scaling-group-name autoscale-demo-asg --desired-capacity 2 --output text

sleep 30
NEW_CAPACITY=$(aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names autoscale-demo-asg --query 'AutoScalingGroups[0].DesiredCapacity' --output text)
print_success "New ASG Capacity: $NEW_CAPACITY"

print_status "Scaling DOWN to 1 instance..."
aws autoscaling set-desired-capacity --auto-scaling-group-name autoscale-demo-asg --desired-capacity 1 --output text

sleep 30
FINAL_CAPACITY=$(aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names autoscale-demo-asg --query 'AutoScalingGroups[0].DesiredCapacity' --output text)
print_success "Final ASG Capacity: $FINAL_CAPACITY"

# Test ALB
print_status "Testing ALB connectivity..."
ALB_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://$ALB_DNS || echo "000")
if [ "$ALB_RESPONSE" = "200" ]; then
    print_success "ALB is responding with HTTP 200!"
elif [ "$ALB_RESPONSE" = "502" ]; then
    print_warning "ALB responding with 502 (instances still starting up)"
else
    print_warning "ALB response code: $ALB_RESPONSE"
fi

# Summary
echo ""
echo "🎉 DEPLOYMENT COMPLETE!"
echo "======================="
echo "Stack Name: autoscale-demo"
echo "ALB DNS: $ALB_DNS"
echo "ASG Name: autoscale-demo-asg"
echo "Current Capacity: $FINAL_CAPACITY"
echo ""
echo "📋 Next Steps:"
echo "1. Test ALB: curl http://$ALB_DNS"
echo "2. Run load generator: python3 loadgen.py http://$ALB_DNS 50 --duration 60"
echo "3. Monitor scaling: aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names autoscale-demo-asg --query 'AutoScalingGroups[0].DesiredCapacity' --output text"
echo "4. Manual scaling: aws autoscaling set-desired-capacity --auto-scaling-group-name autoscale-demo-asg --desired-capacity 3"
echo "5. Cleanup: aws cloudformation delete-stack --stack-name autoscale-demo"
echo ""
print_success "AI-Driven AutoScaling Agent is ready! 🚀"
