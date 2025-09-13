# 🚀 AI-Driven AutoScaling Agent on AWS - FINAL WORKING VERSION

[![AWS](https://img.shields.io/badge/AWS-CloudFormation-orange)](https://aws.amazon.com/cloudformation/)
[![Python](https://img.shields.io/badge/Python-3.7+-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 ONE COMMAND DEPLOYMENT

### **Super Simple - Just One Command:**

```bash
git clone https://github.com/auspicious27/AI-Driven-AutoScaling-Agent-on-AWS.git && cd AI-Driven-AutoScaling-Agent-on-AWS && ./deploy-final.sh
```

**That's it!** The script automatically:
- ✅ Checks prerequisites
- ✅ Fetches AWS resources
- ✅ Deploys complete infrastructure
- ✅ Tests auto-scaling
- ✅ Shows you everything

## ✅ Project Status

**Current Status**: ✅ **100% WORKING & TESTED**

- ✅ CloudFormation template deployed successfully
- ✅ Auto Scaling Group working (scaled 1→2→1 instances)
- ✅ Load Balancer created and configured
- ✅ Load Generator tested and functional
- ✅ All AWS resources properly integrated
- ✅ All issues fixed and resolved

**Last Tested**: September 12, 2025
**AWS Region**: ap-south-1 (Mumbai)
**Stack Name**: autoscale-demo

## 🎯 What This Project Does

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
├── deploy-final.sh       # FINAL working deployment script
├── deploy.sh             # Original deployment script
├── ONE-PROMPT-GUIDE.md   # Simple guide
└── README.md             # This file
```

## 🚀 Prerequisites (One-time setup)

```bash
# 1. Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# 2. Configure AWS credentials
aws configure
# Enter: Access Key ID, Secret Key, Region (ap-south-1), Output format (json)

# 3. Install Python3 (if not installed)
sudo yum install python3 -y  # Amazon Linux
# OR
sudo apt install python3 -y  # Ubuntu
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
curl http://autoscale-demo-alb-532546048.ap-south-1.elb.amazonaws.com

# 5. Manual scaling demo
aws autoscaling set-desired-capacity --auto-scaling-group-name autoscale-demo-asg --desired-capacity 2
aws autoscaling set-desired-capacity --auto-scaling-group-name autoscale-demo-asg --desired-capacity 1

# 6. Check current status
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names autoscale-demo-asg --query 'AutoScalingGroups[0].DesiredCapacity' --output text
```

### 📊 Monitoring Commands

```bash
# 7. Live monitoring (install watch first: brew install watch)
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
pip3 install requests boto3 --break-system-packages

# 12. Run load generator
python3 loadgen.py http://autoscale-demo-alb-532546048.ap-south-1.elb.amazonaws.com 50 --duration 60

# 13. Test different traffic patterns
python3 loadgen.py http://autoscale-demo-alb-532546048.ap-south-1.elb.amazonaws.com 100 --duration 300
python3 loadgen.py http://autoscale-demo-alb-532546048.ap-south-1.elb.amazonaws.com 10 --duration 60
```

### 🛑 Cleanup Commands

```bash
# 14. Delete everything
aws cloudformation delete-stack --stack-name autoscale-demo
aws cloudformation wait stack-delete-complete --stack-name autoscale-demo

# 15. Verify deletion
aws cloudformation describe-stacks --stack-name autoscale-demo
```

## 🎯 Perfect Demo Sequence

```bash
# 1. Deploy everything
git clone https://github.com/auspicious27/AI-Driven-AutoScaling-Agent-on-AWS.git && cd AI-Driven-AutoScaling-Agent-on-AWS && ./deploy-final.sh

# 2. Start monitoring
watch -n 5 'aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names autoscale-demo-asg --query "AutoScalingGroups[0].DesiredCapacity" --output text'

# 3. In another terminal, scale up
aws autoscaling set-desired-capacity --auto-scaling-group-name autoscale-demo-asg --desired-capacity 3

# 4. Watch the capacity change in real-time!

# 5. Scale down
aws autoscaling set-desired-capacity --auto-scaling-group-name autoscale-demo-asg --desired-capacity 1

# 6. Run load generator
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

# Check instance logs
aws logs describe-log-groups --log-group-name-prefix /aws/ec2/autoscale-demo
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

---

**🎉 Ready to deploy? Just run this one command:**

```bash
git clone https://github.com/auspicious27/AI-Driven-AutoScaling-Agent-on-AWS.git && cd AI-Driven-AutoScaling-Agent-on-AWS && ./deploy-final.sh
```

**Total time: 5-10 minutes for complete deployment and testing!** 🚀
