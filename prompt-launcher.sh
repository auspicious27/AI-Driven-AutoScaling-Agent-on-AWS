#!/bin/bash

# AI-Driven AutoScaling Agent - PROMPT-BASED LAUNCHER
# ===================================================
# Usage: Just run this script and follow prompts!

set -e

echo "🤖 AI-Driven AutoScaling Agent - PROMPT-BASED LAUNCHER"
echo "======================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_prompt() {
    echo -e "${PURPLE}[PROMPT]${NC} $1"
}

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

print_ai() {
    echo -e "${CYAN}[AI RESPONSE]${NC} $1"
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check AWS CLI
    if ! command -v aws &> /dev/null; then
        print_error "AWS CLI not found. Please install AWS CLI first."
        print_prompt "Would you like me to install AWS CLI? (y/n)"
        read -p "> " install_aws
        if [[ $install_aws =~ ^[Yy]$ ]]; then
            if [[ "$OSTYPE" == "darwin"* ]]; then
                brew install awscli
            elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
                sudo apt-get update && sudo apt-get install -y awscli
            fi
        else
            exit 1
        fi
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 not found. Please install Python3 first."
        exit 1
    fi
    
    # Check AWS credentials
    if ! aws sts get-caller-identity --output text &> /dev/null; then
        print_warning "AWS credentials not configured."
        print_prompt "Would you like to configure AWS credentials now? (y/n)"
        read -p "> " configure_aws
        if [[ $configure_aws =~ ^[Yy]$ ]]; then
            aws configure
        else
            print_error "AWS credentials required to continue."
            exit 1
        fi
    fi
    
    print_success "All prerequisites met!"
}

# Function to get AWS resources
get_aws_resources() {
    print_status "Fetching AWS resources..."
    
    # Get VPC
    VPC_ID=$(aws ec2 describe-vpcs --filters "Name=is-default,Values=true" --query 'Vpcs[0].VpcId' --output text)
    if [ "$VPC_ID" = "None" ] || [ -z "$VPC_ID" ]; then
        VPC_ID=$(aws ec2 describe-vpcs --query 'Vpcs[0].VpcId' --output text)
    fi
    print_success "VPC ID: $VPC_ID"
    
    # Get Public Subnets
    PUBLIC_SUBNETS=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" "Name=map-public-ip-on-launch,Values=true" --query 'Subnets[*].SubnetId' --output text | tr '\t' ',')
    print_success "Public Subnets: $PUBLIC_SUBNETS"
    
    # Get AMI ID
    AMI_ID=$(aws ec2 describe-images --owners amazon --filters "Name=name,Values=amzn2-ami-hvm-*-x86_64-gp2" "Name=state,Values=available" --query 'Images | sort_by(@, &CreationDate) | [-1].ImageId' --output text)
    print_success "AMI ID: $AMI_ID"
}

# Function to create key pair
create_key_pair() {
    print_status "Creating EC2 key pair..."
    
    if aws ec2 describe-key-pairs --key-names autoscale-demo-key &> /dev/null; then
        print_success "Key pair already exists: autoscale-demo-key"
    else
        aws ec2 create-key-pair --key-name autoscale-demo-key --query 'KeyMaterial' --output text > autoscale-demo-key.pem
        chmod 400 autoscale-demo-key.pem
        print_success "Key pair created: autoscale-demo-key.pem"
    fi
}

# Function to deploy infrastructure
deploy_infrastructure() {
    print_status "Deploying AWS infrastructure..."
    
    aws cloudformation deploy \
        --template-file autoscale-demo.yml \
        --stack-name autoscale-demo \
        --parameter-overrides \
            KeyName=autoscale-demo-key \
            VpcId=$VPC_ID \
            PublicSubnets=$PUBLIC_SUBNETS \
            ImageId=$AMI_ID \
            InstanceType=t3.micro \
        --capabilities CAPABILITY_IAM
    
    print_success "Infrastructure deployed successfully!"
}

# Function to get ALB DNS
get_alb_dns() {
    print_status "Getting ALB DNS name..."
    
    ALB_DNS=$(aws cloudformation describe-stacks \
        --stack-name autoscale-demo \
        --query 'Stacks[0].Outputs[?OutputKey==`ApplicationLoadBalancerDNS`].OutputValue' \
        --output text)
    
    print_success "ALB DNS: $ALB_DNS"
}

# Function to install Python dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    
    pip3 install requests boto3 --break-system-packages &> /dev/null || pip3 install requests boto3 --user &> /dev/null || true
    
    print_success "Python dependencies installed!"
}

# Function to wait for instances
wait_for_instances() {
    print_status "Waiting for instances to be ready..."
    
    sleep 60  # Wait for instances to start
    
    CURRENT_CAPACITY=$(aws autoscaling describe-auto-scaling-groups \
        --auto-scaling-group-names autoscale-demo-asg \
        --query 'AutoScalingGroups[0].DesiredCapacity' \
        --output text)
    
    print_success "Current ASG Capacity: $CURRENT_CAPACITY"
}

# Function to test ALB
test_alb() {
    print_status "Testing ALB connectivity..."
    
    sleep 30  # Wait for ALB to be ready
    
    if curl -s -o /dev/null -w "%{http_code}" http://$ALB_DNS | grep -q "200"; then
        print_success "ALB is responding with HTTP 200!"
    else
        print_warning "ALB not ready yet, but deployment completed."
    fi
}

# Function to show next steps
show_next_steps() {
    echo ""
    echo "🎉 DEPLOYMENT COMPLETE!"
    echo "======================="
    echo "Stack Name: autoscale-demo"
    echo "ALB DNS: $ALB_DNS"
    echo "ASG Name: autoscale-demo-asg"
    echo "Current Capacity: $CURRENT_CAPACITY"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Test ALB: curl http://$ALB_DNS"
    echo "2. Run load generator: python3 loadgen.py http://$ALB_DNS 50 --duration 60"
    echo "3. Monitor scaling: aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names autoscale-demo-asg --query 'AutoScalingGroups[0].DesiredCapacity' --output text"
    echo "4. Manual scaling: aws autoscaling set-desired-capacity --auto-scaling-group-name autoscale-demo-asg --desired-capacity 3"
    echo "5. Cleanup: aws cloudformation delete-stack --stack-name autoscale-demo"
    echo ""
    print_success "AI-Driven AutoScaling Agent is ready! 🚀"
}

# Main execution
main() {
    print_ai "Hello! I'm your AI assistant. I'll help you deploy the AI-Driven AutoScaling Agent on AWS."
    print_ai "Just follow my prompts and I'll handle everything for you!"
    echo ""
    
    check_prerequisites
    get_aws_resources
    create_key_pair
    deploy_infrastructure
    get_alb_dns
    install_dependencies
    wait_for_instances
    test_alb
    show_next_steps
}

# Run main function
main "$@"
