# 🚀 One-Prompt AI-Driven AutoScaling Agent

## Single Command Deployment

### Prerequisites (One-time setup):
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

### 🎯 ONE-PROMPT DEPLOYMENT:

```bash
# Clone and deploy everything in one command:
git clone https://github.com/auspicious27/AI-Driven-AutoScaling-Agent-on-AWS.git && cd AI-Driven-AutoScaling-Agent-on-AWS && ./deploy.sh
```

**That's it!** 🎉

## What the script does automatically:

1. ✅ **Checks prerequisites** (AWS CLI, Python, credentials)
2. ✅ **Fetches AWS resources** (VPC, subnets, AMI)
3. ✅ **Creates key pair** (if not exists)
4. ✅ **Deploys CloudFormation stack** (complete infrastructure)
5. ✅ **Gets ALB DNS name** (load balancer endpoint)
6. ✅ **Installs dependencies** (Python packages)
7. ✅ **Tests auto-scaling** (scales up and down)
8. ✅ **Shows summary** (all important info)

## 🎮 After Deployment - Quick Commands:

```bash
# Test the system
curl http://YOUR-ALB-DNS.ap-south-1.elb.amazonaws.com

# Run load generator
python3 loadgen.py http://YOUR-ALB-DNS.ap-south-1.elb.amazonaws.com 50 --duration 60

# Monitor scaling
watch -n 5 'aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names autoscale-demo-asg --query "AutoScalingGroups[0].DesiredCapacity" --output text'

# Manual scaling
aws autoscaling set-desired-capacity --auto-scaling-group-name autoscale-demo-asg --desired-capacity 3

# Cleanup
aws cloudformation delete-stack --stack-name autoscale-demo
```

## 🎯 Perfect for:

- **Demos**: Show auto-scaling in action
- **Learning**: Understand AWS auto-scaling
- **Testing**: Validate scaling behavior
- **Presentations**: Impress with one-command deployment

## 📱 Share this with anyone:

**"Want to see AI-driven auto-scaling on AWS? Just run this one command:"**

```bash
git clone https://github.com/auspicious27/AI-Driven-AutoScaling-Agent-on-AWS.git && cd AI-Driven-AutoScaling-Agent-on-AWS && ./deploy.sh
```

**That's it! No complex setup, no manual configuration - everything automated!** 🚀
