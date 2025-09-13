# 🚀 AI-Driven AutoScaling Agent on AWS - Manual Deployment Guide

A complete step-by-step guide for manual deployment without automation scripts.

## 🎯 Quick Start (Automated)

```bash
git clone https://github.com/auspicious27/AI-Driven-AutoScaling-Agent-on-AWS.git && cd AI-Driven-AutoScaling-Agent-on-AWS && ./deploy-perfect.sh
```

## 📋 Manual Deployment Steps

### Step 1: Prerequisites Setup

```bash
# 1. Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# 2. Configure AWS credentials
aws configure
# Enter: Access Key ID, Secret Key, Region (ap-south-1), Output format (json)

# 3. Install Python dependencies
pip3 install requests boto3 --break-system-packages
```

### Step 2: Get AWS Resources

```bash
# Get VPC ID
aws ec2 describe-vpcs --filters "Name=is-default,Values=true" --query 'Vpcs[0].VpcId' --output text

# Get Public Subnets
aws ec2 describe-subnets --filters "Name=vpc-id,Values=vpc-096e19eeda1c50721" --query 'Subnets[?MapPublicIpOnLaunch==`true`].SubnetId' --output text

# Get Latest AMI ID
aws ec2 describe-images --owners amazon --filters "Name=name,Values=amzn2-ami-hvm-*-x86_64-gp2" --query 'Images[0].ImageId' --output text

# Create Key Pair
aws ec2 create-key-pair --key-name autoscale-demo-key --query 'KeyMaterial' --output text > autoscale-demo-key.pem
chmod 400 autoscale-demo-key.pem
```

### Step 3: Deploy CloudFormation Stack

```bash
aws cloudformation deploy \
  --template-file autoscale-demo.yml \
  --stack-name autoscale-demo \
  --parameter-overrides \
    KeyName=autoscale-demo-key \
    VpcId=vpc-096e19eeda1c50721 \
    PublicSubnets=subnet-0986036a60ddda932,subnet-045fcfbac71b671a8 \
    ImageId=ami-0006460c3ae9e3f07 \
    InstanceType=t3.micro \
  --capabilities CAPABILITY_IAM
```

### Step 4: Get ALB DNS Name

```bash
aws cloudformation describe-stacks --stack-name autoscale-demo --query "Stacks[0].Outputs" --output json
```

### Step 5: Test Deployment

```bash
# Test ALB connectivity
curl http://autoscale-demo-alb-2027287440.ap-south-1.elb.amazonaws.com

# Check ASG status
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names autoscale-demo-asg --query 'AutoScalingGroups[0].DesiredCapacity' --output text
```

### Step 6: Manual Scaling Test

```bash
# Scale UP to 2 instances
aws autoscaling set-desired-capacity --auto-scaling-group-name autoscale-demo-asg --desired-capacity 2

# Wait and check
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names autoscale-demo-asg --query 'AutoScalingGroups[0].DesiredCapacity' --output text

# Scale DOWN to 1 instance
aws autoscaling set-desired-capacity --auto-scaling-group-name autoscale-demo-asg --desired-capacity 1
```

### Step 7: Load Testing

```bash
# Run load generator
python3 loadgen.py http://autoscale-demo-alb-2027287440.ap-south-1.elb.amazonaws.com 50 --duration 60

# Test different traffic patterns
python3 loadgen.py http://autoscale-demo-alb-2027287440.ap-south-1.elb.amazonaws.com 100 --duration 300
python3 loadgen.py http://autoscale-demo-alb-2027287440.ap-south-1.elb.amazonaws.com 10 --duration 60
```

### Step 8: Monitoring

```bash
# Install watch command (macOS)
brew install watch

# Live monitoring
watch -n 5 'aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names autoscale-demo-asg --query "AutoScalingGroups[0].DesiredCapacity" --output text'

# Check scaling activities
aws autoscaling describe-scaling-activities --auto-scaling-group-name autoscale-demo-asg

# Get instance details
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names autoscale-demo-asg --query 'AutoScalingGroups[0].Instances[].InstanceId' --output table
```

### Step 9: Cleanup

```bash
# Delete CloudFormation stack
aws cloudformation delete-stack --stack-name autoscale-demo

# Wait for deletion
aws cloudformation wait stack-delete-complete --stack-name autoscale-demo

# Verify deletion
aws cloudformation describe-stacks --stack-name autoscale-demo
```

## 🔍 Troubleshooting

### Common Issues:

1. **AWS credentials not configured**
   ```bash
   aws configure
   ```

2. **No default VPC**
   ```bash
   # Create VPC in AWS Console or use existing VPC
   aws ec2 describe-vpcs --query 'Vpcs[].VpcId' --output text
   ```

3. **Insufficient permissions**
   ```bash
   # Add CloudFormation, EC2, AutoScaling permissions to IAM user
   ```

4. **Python not found**
   ```bash
   # Install Python3
   brew install python3
   ```

5. **502 Bad Gateway**
   ```bash
   # Normal during instance startup, wait 2-3 minutes
   # Check instance health
   aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names autoscale-demo-asg
   ```

### Debug Commands:

```bash
# Check CloudFormation events
aws cloudformation describe-stack-events --stack-name autoscale-demo

# Check Auto Scaling activities
aws autoscaling describe-scaling-activities --auto-scaling-group-name autoscale-demo-asg

# Check instance status
aws ec2 describe-instances --filters "Name=tag:Name,Values=autoscale-demo-asg" --query 'Reservations[].Instances[].State.Name' --output text
```

## 📁 Project Files

- `autoscale-demo.yml` - CloudFormation template
- `agent.py` - AutoScaling monitoring agent
- `loadgen.py` - HTTP load generator
- `deploy-perfect.sh` - Automated deployment script

## 🎯 What This Project Does

- **Monitors** CloudWatch metrics for Application Load Balancer request count
- **Scales** EC2 instances automatically based on traffic patterns
- **Prevents** scaling flapping with intelligent hysteresis logic
- **Logs** all scaling decisions and metrics

### Scaling Logic

- **Scale UP**: When requests/minute > 120 (add 1 instance, max 4)
- **Scale DOWN**: When requests/minute < 60 (remove 1 instance, min 1)

## 🚀 Ready to Deploy?

### Automated (Recommended):
```bash
git clone https://github.com/auspicious27/AI-Driven-AutoScaling-Agent-on-AWS.git && cd AI-Driven-AutoScaling-Agent-on-AWS && ./deploy-perfect.sh
```

### Manual (Step-by-step):
Follow the manual steps above for complete control.

**Total time: 5-10 minutes for complete deployment and testing!** 🚀
