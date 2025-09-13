# AI-Driven AutoScaling Agent on AWS

A complete demonstration of intelligent auto-scaling using AWS infrastructure with a Python-based monitoring agent that automatically scales EC2 instances based on Application Load Balancer traffic patterns.

[![AWS](https://img.shields.io/badge/AWS-CloudFormation-orange)](https://aws.amazon.com/cloudformation/)
[![Python](https://img.shields.io/badge/Python-3.7+-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🚀 ONE-PROMPT DEPLOYMENT

### Super Simple - Just One Command:

```bash
git clone https://github.com/auspicious27/AI-Driven-AutoScaling-Agent-on-AWS.git && cd AI-Driven-AutoScaling-Agent-on-AWS && ./deploy.sh
```

**That's it!** The script automatically:
- ✅ Checks prerequisites
- ✅ Fetches AWS resources
- ✅ Deploys complete infrastructure
- ✅ Tests auto-scaling
- ✅ Shows you everything

### Prerequisites (One-time setup):
```bash
# 1. Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# 2. Configure AWS credentials
aws configure
# Enter: Access Key ID, Secret Key, Region (ap-south-1), Output format (json)
```

### Manual Deployment (if needed):
```bash
# Clone the repository
git clone https://github.com/auspicious27/AI-Driven-AutoScaling-Agent-on-AWS.git
cd AI-Driven-AutoScaling-Agent-on-AWS

# Deploy infrastructure (replace with your values)
aws cloudformation deploy \
  --template-file autoscale-demo.yml \
  --stack-name autoscale-demo \
  --parameter-overrides \
    KeyName=your-key-pair-name \
    VpcId=vpc-xxxxxxxxx \
    PublicSubnets=subnet-xxxxxxxxx,subnet-yyyyyyyyy \
    ImageId=ami-0c02fb55956c7d316 \
    InstanceType=t3.micro \
  --capabilities CAPABILITY_IAM
```

## ✅ Project Status

**Current Status**: ✅ **WORKING & TESTED**

- ✅ CloudFormation template deployed successfully
- ✅ Auto Scaling Group working (scaled 1→2 instances)
- ✅ Load Balancer created and configured
- ✅ Load Generator tested and functional
- ✅ All AWS resources properly integrated

**Last Tested**: September 12, 2025
**AWS Region**: ap-south-1 (Mumbai)
**Stack Name**: autoscale-demo

## 🎯 Overview

This project demonstrates an AI-driven auto-scaling solution that:

- **Monitors** CloudWatch metrics for Application Load Balancer request count
- **Analyzes** traffic patterns in real-time
- **Scales** EC2 instances automatically based on configurable thresholds
- **Prevents** scaling flapping with intelligent hysteresis logic
- **Logs** all scaling decisions and metrics for observability

### Scaling Logic

- **Scale UP**: When requests/minute > 120 (add 1 instance, max 4)
- **Scale DOWN**: When requests/minute < 60 (remove 1 instance, min 1)
- **Hysteresis**: Requires 2 consecutive high-traffic readings to scale up, 3 consecutive low-traffic readings to scale down

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Load Generator │───▶│ Application Load │───▶│   EC2 Instances │
│   (loadgen.py)  │    │     Balancer     │    │  (Auto Scaling  │
└─────────────────┘    └──────────────────┘    │     Group)      │
                              │                 └─────────────────┘
                              ▼
                       ┌──────────────────┐
                       │   CloudWatch     │
                       │    Metrics       │
                       └──────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │ AutoScaling Agent│
                       │   (agent.py)     │
                       └──────────────────┘
```

## 📁 Project Structure

```
autoscale-demo/
├── autoscale-demo.yml    # CloudFormation template
├── agent.py              # AutoScaling monitoring agent
├── loadgen.py            # HTTP load generator
└── README.md             # This file
```

## 📋 Complete Commands Reference

### 🔧 Setup Commands

```bash
# 1. Get your AWS resources automatically
aws ec2 describe-key-pairs --query 'KeyPairs[].KeyName' --output text
aws ec2 describe-vpcs --filters "Name=is-default,Values=true" --query 'Vpcs[0].VpcId' --output text
aws ec2 describe-subnets --filters "Name=vpc-id,Values=vpc-xxxxxxxxx" --query 'Subnets[?MapPublicIpOnLaunch==`true`].SubnetId' --output text
aws ec2 describe-images --owners amazon --filters "Name=name,Values=amzn2-ami-hvm-*-x86_64-gp2" --query 'Images[0].ImageId' --output text

# 2. Deploy with auto-fetched values
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
# 3. Get ALB DNS name
aws cloudformation describe-stacks --stack-name autoscale-demo --query "Stacks[0].Outputs" --output json

# 4. Test basic connectivity
curl http://autoscale-demo-alb-1064252660.ap-south-1.elb.amazonaws.com

# 5. Manual scaling demo
aws autoscaling set-desired-capacity --auto-scaling-group-name autoscale-demo-asg --desired-capacity 2
aws autoscaling set-desired-capacity --auto-scaling-group-name autoscale-demo-asg --desired-capacity 1

# 6. Check current status
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names autoscale-demo-asg --query 'AutoScalingGroups[0].DesiredCapacity' --output text
```

### 📊 Monitoring Commands

```bash
# 7. Live monitoring
watch -n 5 'aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names autoscale-demo-asg --query "AutoScalingGroups[0].DesiredCapacity" --output text'

# 8. Check scaling activities
aws autoscaling describe-scaling-activities --auto-scaling-group-name autoscale-demo-asg

# 9. Get instance details
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names autoscale-demo-asg --query 'AutoScalingGroups[0].Instances[].InstanceId' --output table

# 10. Check target group health
aws elbv2 describe-target-health --target-group-arn arn:aws:elasticloadbalancing:ap-south-1:ACCOUNT:targetgroup/autoscale-demo-tg/ID
```

### 🧪 Testing Commands

```bash
# 11. Install load generator dependencies
pip3 install requests --break-system-packages

# 12. Run load generator
python3 loadgen.py http://autoscale-demo-alb-1064252660.ap-south-1.elb.amazonaws.com 50 --duration 60

# 13. Test different traffic patterns
python3 loadgen.py http://autoscale-demo-alb-1064252660.ap-south-1.elb.amazonaws.com 100 --duration 300
python3 loadgen.py http://autoscale-demo-alb-1064252660.ap-south-1.elb.amazonaws.com 10 --duration 60
```

### 🛑 Cleanup Commands

```bash
# 14. Delete everything
aws cloudformation delete-stack --stack-name autoscale-demo
aws cloudformation wait stack-delete-complete --stack-name autoscale-demo

# 15. Verify deletion
aws cloudformation describe-stacks --stack-name autoscale-demo
```

### 2. Get ALB DNS Name

After deployment, get the Application Load Balancer DNS name:

```bash
aws cloudformation describe-stacks \
  --stack-name autoscale-demo \
  --query "Stacks[0].Outputs" \
  --output json
```

Look for the `ApplicationLoadBalancerDNS` output value.

### 3. Test the Setup

Verify the infrastructure is working:

```bash
# Test basic connectivity
curl http://your-alb-dns-name.us-east-1.elb.amazonaws.com

# Check Auto Scaling Group status
aws autoscaling describe-auto-scaling-groups \
  --auto-scaling-group-names autoscale-demo-asg
```

### 4. Generate Load

Use the load generator to create traffic and trigger auto-scaling:

```bash
# Generate 50 requests per second (should trigger scale-up)
python3 loadgen.py http://your-alb-dns-name.us-east-1.elb.amazonaws.com 50

# Generate 200 requests per second for 5 minutes
python3 loadgen.py http://your-alb-dns-name.us-east-1.elb.amazonaws.com 200 --duration 300

# Generate 10 requests per second (should trigger scale-down)
python3 loadgen.py http://your-alb-dns-name.us-east-1.elb.amazonaws.com 10
```

### 5. Monitor Auto-Scaling

Watch the Auto Scaling Group capacity change:

```bash
# Monitor ASG capacity
watch -n 10 "aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names autoscale-demo-asg --query 'AutoScalingGroups[0].DesiredCapacity' --output text"

# Check agent logs on EC2 instances
aws ssm start-session --target i-xxxxxxxxx  # Replace with actual instance ID
sudo tail -f /home/ec2-user/agent.log
```

## 📊 Monitoring and Observability

### CloudWatch Metrics

The agent monitors these CloudWatch metrics:
- `AWS/ApplicationELB.RequestCount` - Total requests to the load balancer
- Calculates requests per minute over 5-minute windows

### Agent Logs

The agent logs all activities to `/home/ec2-user/agent.log`:

```bash
# View real-time logs
tail -f /home/ec2-user/agent.log

# View scaling history
grep "Scaling" /home/ec2-user/agent.log
```

### Load Generator Statistics

The load generator provides real-time statistics:
- Total requests sent
- Current requests per second
- Success rate
- Average response time
- Error breakdown

## 🔧 Configuration

### Agent Configuration

The agent can be configured with command-line arguments:

```bash
python3 agent.py \
  --asg-name autoscale-demo-asg \
  --alb-arn arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/autoscale-demo-alb/1234567890abcdef \
  --scale-up-threshold 150 \
  --scale-down-threshold 50 \
  --min-capacity 2 \
  --max-capacity 6 \
  --check-interval 30
```

### Load Generator Configuration

```bash
python3 loadgen.py \
  http://your-alb-dns-name.us-east-1.elb.amazonaws.com \
  100 \
  --duration 600 \
  --threads 20 \
  --timeout 10
```

## 🛠️ Advanced Usage

### Custom Scaling Policies

Modify the agent thresholds in the CloudFormation template or run with custom parameters:

```bash
# More aggressive scaling
python3 agent.py --asg-name autoscale-demo-asg --alb-arn <arn> --scale-up-threshold 80 --scale-down-threshold 40

# More conservative scaling
python3 agent.py --asg-name autoscale-demo-asg --alb-arn <arn> --scale-up-threshold 200 --scale-down-threshold 100
```

### Load Testing Scenarios

Test different traffic patterns:

```bash
# Gradual ramp-up
python3 loadgen.py http://your-alb.us-east-1.elb.amazonaws.com 10 --duration 60
python3 loadgen.py http://your-alb.us-east-1.elb.amazonaws.com 50 --duration 60
python3 loadgen.py http://your-alb.us-east-1.elb.amazonaws.com 100 --duration 60

# Burst traffic
python3 loadgen.py http://your-alb.us-east-1.elb.amazonaws.com 300 --duration 300

# Sustained high load
python3 loadgen.py http://your-alb.us-east-1.elb.amazonaws.com 150 --duration 1800
```

### Monitoring Commands

```bash
# Get current ASG status
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names autoscale-demo-asg

# Get ALB metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/ApplicationELB \
  --metric-name RequestCount \
  --dimensions Name=LoadBalancer,Value=app/autoscale-demo-alb/1234567890abcdef \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-01T01:00:00Z \
  --period 300 \
  --statistics Sum

# Get instance health
aws elbv2 describe-target-health --target-group-arn <target-group-arn>
```

## 🔍 Troubleshooting

### Common Issues

1. **Agent not scaling**
   - Check CloudWatch metrics are available
   - Verify IAM permissions
   - Check agent logs for errors

2. **Load generator not working**
   - Verify ALB DNS name is correct
   - Check security group allows HTTP traffic
   - Ensure ALB is healthy

3. **Instances not launching**
   - Check subnet availability
   - Verify AMI ID is valid
   - Check security group configuration

### Debug Commands

```bash
# Check CloudFormation stack status
aws cloudformation describe-stacks --stack-name autoscale-demo

# Check ASG events
aws autoscaling describe-scaling-activities --auto-scaling-group-name autoscale-demo-asg

# Check instance logs
aws logs describe-log-groups --log-group-name-prefix /aws/ec2/autoscale-demo

# Test ALB health
curl -v http://your-alb-dns-name.us-east-1.elb.amazonaws.com/health
```

## 🧹 Cleanup

To avoid AWS charges, clean up all resources:

```bash
# Delete the CloudFormation stack
aws cloudformation delete-stack --stack-name autoscale-demo

# Wait for deletion to complete
aws cloudformation wait stack-delete-complete --stack-name autoscale-demo

# Verify deletion
aws cloudformation describe-stacks --stack-name autoscale-demo
```

## 📈 Performance Considerations

### Scaling Behavior

- **Scale-up**: Triggered after 2 consecutive high-traffic readings
- **Scale-down**: Triggered after 3 consecutive low-traffic readings
- **Cooldown**: AWS Auto Scaling cooldown periods are honored
- **Health checks**: ELB health checks prevent scaling unhealthy instances

### Cost Optimization

- Uses `t3.micro` instances by default (free tier eligible)
- Minimum capacity of 1 instance
- Maximum capacity of 4 instances
- Automatic cleanup capabilities

## 🔒 Security

### IAM Permissions

The EC2 instances have minimal required permissions:
- CloudWatch read access for metrics
- Auto Scaling read/write access for capacity changes
- No unnecessary permissions granted

### Network Security

- ALB security group allows HTTP (port 80) from anywhere
- Instance security group allows HTTP from ALB and SSH from anywhere
- Instances are in public subnets for ALB access

## 📚 Additional Resources

- [AWS Auto Scaling Groups Documentation](https://docs.aws.amazon.com/autoscaling/ec2/userguide/AutoScalingGroup.html)
- [Application Load Balancer Documentation](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/)
- [CloudWatch Metrics Documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/working_with_metrics.html)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is provided as-is for educational and demonstration purposes.
