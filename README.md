# AI-Driven AutoScaling Agent on AWS
# ===================================

## 🚀 **One Command Deployment**

```bash
git clone https://github.com/auspicious27/AI-Driven-AutoScaling-Agent-on-AWS.git && cd AI-Driven-AutoScaling-Agent-on-AWS && chmod +x install.sh deploy-perfect.sh && ./install.sh && ./deploy-perfect.sh
```

## 📋 **Quick Setup**

### **Step 1: Install Prerequisites**
```bash
# Install AWS CLI
brew install awscli  # macOS
sudo apt-get install awscli  # Linux

# Install Python dependencies
pip3 install boto3 requests urllib3

# Install system tools
brew install watch weasyprint  # macOS
sudo apt-get install procps && pip3 install weasyprint  # Linux
```

### **Step 2: Configure AWS**
```bash
aws configure
# Enter your AWS credentials and region (e.g., ap-south-1)
```

### **Step 3: Deploy Infrastructure**
```bash
./deploy-perfect.sh
```

## 🎯 **What This Does**

- **Creates AWS Infrastructure** - VPC, ALB, Auto Scaling Group
- **Deploys Auto-Scaling Agent** - Monitors ALB request metrics
- **Scales Automatically** - Up when requests > 120/min, Down when < 60/min
- **Load Testing** - Generates traffic to test scaling

## 📊 **Monitor Auto-Scaling**

```bash
# Check current capacity
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names autoscale-demo-asg --query 'AutoScalingGroups[0].DesiredCapacity' --output text

# Watch real-time scaling
watch -n 5 'aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names autoscale-demo-asg --query "AutoScalingGroups[0].DesiredCapacity" --output text'
```

## 🧪 **Test Load Generation**

```bash
# Get ALB DNS from deployment output
python3 loadgen.py http://YOUR-ALB-DNS.ap-south-1.elb.amazonaws.com 50 --duration 60
```

## 🧹 **Cleanup**

```bash
aws cloudformation delete-stack --stack-name autoscale-demo
```

## 📚 **Documentation**

- **`DOCUMENTATION.pdf`** - Complete project documentation
- **`SETUP-GUIDE.md`** - Detailed setup guide
- **`README-MANUAL.md`** - Manual deployment guide
- **`README-CLEAN.md`** - Clean deployment guide

## 🎉 **Ready to Deploy!**

**One command to rule them all:**
```bash
git clone https://github.com/auspicious27/AI-Driven-AutoScaling-Agent-on-AWS.git && cd AI-Driven-AutoScaling-Agent-on-AWS && chmod +x install.sh deploy-perfect.sh && ./install.sh && ./deploy-perfect.sh
```

**Perfect for workshops, demos, and learning AWS auto-scaling!** 🚀
