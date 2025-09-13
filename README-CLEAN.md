# 🚀 AI-Driven AutoScaling Agent on AWS

A complete demonstration of intelligent auto-scaling using AWS infrastructure with a Python-based monitoring agent.

## 🎯 ONE COMMAND DEPLOYMENT

```bash
git clone https://github.com/auspicious27/AI-Driven-AutoScaling-Agent-on-AWS.git && cd AI-Driven-AutoScaling-Agent-on-AWS && ./deploy-perfect.sh
```

**That's it!** Everything deploys automatically.

## ✅ Prerequisites (One-time setup)

```bash
# 1. Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# 2. Configure AWS credentials
aws configure
# Enter: Access Key ID, Secret Key, Region (ap-south-1), Output format (json)
```

## 📋 Working Commands

### 🔧 Setup Commands

```bash
# Get AWS resources automatically
aws ec2 describe-key-pairs --query 'KeyPairs[].KeyName' --output text
aws ec2 describe-vpcs --filters "Name=is-default,Values=true" --query 'Vpcs[0].VpcId' --output text
aws ec2 describe-subnets --filters "Name=vpc-id,Values=vpc-xxxxxxxxx" --query 'Subnets[?MapPublicIpOnLaunch==`true`].SubnetId' --output text
aws ec2 describe-images --owners amazon --filters "Name=name,Values=amzn2-ami-hvm-*-x86_64-gp2" --query 'Images[0].ImageId' --output text

# Deploy infrastructure
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

### 🎮 Demo Commands

```bash
# Get ALB DNS name
aws cloudformation describe-stacks --stack-name autoscale-demo --query "Stacks[0].Outputs" --output json

# Test ALB
curl http://autoscale-demo-alb-532546048.ap-south-1.elb.amazonaws.com

# Manual scaling
aws autoscaling set-desired-capacity --auto-scaling-group-name autoscale-demo-asg --desired-capacity 2
aws autoscaling set-desired-capacity --auto-scaling-group-name autoscale-demo-asg --desired-capacity 1

# Check current status
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names autoscale-demo-asg --query 'AutoScalingGroups[0].DesiredCapacity' --output text
```

### 📊 Monitoring Commands

```bash
# Live monitoring (install watch first: brew install watch)
watch -n 5 'aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names autoscale-demo-asg --query "AutoScalingGroups[0].DesiredCapacity" --output text'

# Check scaling activities
aws autoscaling describe-scaling-activities --auto-scaling-group-name autoscale-demo-asg

# Get instance details
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names autoscale-demo-asg --query 'AutoScalingGroups[0].Instances[].InstanceId' --output table
```

### 🧪 Testing Commands

```bash
# Install dependencies
pip3 install requests boto3 --break-system-packages

# Run load generator
python3 loadgen.py http://autoscale-demo-alb-532546048.ap-south-1.elb.amazonaws.com 50 --duration 60

# Test different traffic patterns
python3 loadgen.py http://autoscale-demo-alb-532546048.ap-south-1.elb.amazonaws.com 100 --duration 300
python3 loadgen.py http://autoscale-demo-alb-532546048.ap-south-1.elb.amazonaws.com 10 --duration 60
```

### 🛑 Cleanup Commands

```bash
# Delete everything
aws cloudformation delete-stack --stack-name autoscale-demo
aws cloudformation wait stack-delete-complete --stack-name autoscale-demo

# Verify deletion
aws cloudformation describe-stacks --stack-name autoscale-demo
```

## 🎯 Perfect Demo Sequence

```bash
# 1. Deploy everything
git clone https://github.com/auspicious27/AI-Driven-AutoScaling-Agent-on-AWS.git && cd AI-Driven-AutoScaling-Agent-on-AWS && ./deploy-perfect.sh

# 2. Start monitoring
watch -n 5 'aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names autoscale-demo-asg --query "AutoScalingGroups[0].DesiredCapacity" --output text'

# 3. Scale up
aws autoscaling set-desired-capacity --auto-scaling-group-name autoscale-demo-asg --desired-capacity 3

# 4. Scale down
aws autoscaling set-desired-capacity --auto-scaling-group-name autoscale-demo-asg --desired-capacity 1

# 5. Run load generator
python3 loadgen.py http://YOUR-ALB-DNS.ap-south-1.elb.amazonaws.com 50 --duration 60
```

## 🔍 Troubleshooting

### Common Issues:

1. **AWS credentials not configured**: Run `aws configure`
2. **No default VPC**: Create a VPC in AWS Console
3. **Insufficient permissions**: Add CloudFormation, EC2, AutoScaling permissions
4. **Python not found**: Install Python3
5. **502 Bad Gateway**: Normal during instance startup, wait 2-3 minutes

### Debug Commands:

```bash
# Check CloudFormation events
aws cloudformation describe-stack-events --stack-name autoscale-demo

# Check Auto Scaling activities
aws autoscaling describe-scaling-activities --auto-scaling-group-name autoscale-demo-asg
```

## 📁 Project Files

- `autoscale-demo.yml` - CloudFormation template
- `agent.py` - AutoScaling monitoring agent
- `loadgen.py` - HTTP load generator
- `deploy-perfect.sh` - Perfect working deployment script

## 🎯 What This Project Does

- **Monitors** CloudWatch metrics for Application Load Balancer request count
- **Scales** EC2 instances automatically based on traffic patterns
- **Prevents** scaling flapping with intelligent hysteresis logic
- **Logs** all scaling decisions and metrics

### Scaling Logic

- **Scale UP**: When requests/minute > 120 (add 1 instance, max 4)
- **Scale DOWN**: When requests/minute < 60 (remove 1 instance, min 1)

## 🚀 Ready to Deploy?

```bash
git clone https://github.com/auspicious27/AI-Driven-AutoScaling-Agent-on-AWS.git && cd AI-Driven-AutoScaling-Agent-on-AWS && ./deploy-perfect.sh
```

**Total time: 5-10 minutes for complete deployment and testing!** 🚀
