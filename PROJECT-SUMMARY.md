# AI-Driven AutoScaling Agent on AWS - Complete Project
# =====================================================

## 🎯 **Project Overview**
This project demonstrates an AI-driven auto-scaling system on AWS that automatically scales EC2 instances based on Application Load Balancer (ALB) request metrics.

## 📁 **Complete File Structure**

### **Core Files**
- **`autoscale-demo.yml`** - CloudFormation template for AWS infrastructure
- **`agent.py`** - Auto-scaling agent script (monitors ALB metrics)
- **`loadgen.py`** - Load generator script (simulates traffic)
- **`deploy-perfect.sh`** - Automated deployment script

### **Documentation Files**
- **`DOCUMENTATION.pdf`** - Complete project documentation (61KB)
- **`DOCUMENTATION.html`** - HTML version of documentation
- **`README-CLEAN.md`** - Clean deployment guide
- **`README-MANUAL.md`** - Detailed manual deployment guide
- **`README-PROMPT.md`** - Prompt-based deployment guide
- **`SETUP-GUIDE.md`** - Complete setup and installation guide

### **Installation Files**
- **`requirements.txt`** - Python dependencies list
- **`install.sh`** - Automated installation script
- **`.gitignore`** - Git ignore patterns

### **Generated Files**
- **`autoscale-demo-key.pem`** - SSH private key for EC2 instances

## 🚀 **Quick Start (One Command)**

```bash
# Clone and deploy everything
git clone https://github.com/auspicious27/AI-Driven-AutoScaling-Agent-on-AWS.git
cd AI-Driven-AutoScaling-Agent-on-AWS
chmod +x install.sh deploy-perfect.sh
./install.sh && ./deploy-perfect.sh
```

## 📋 **Required Dependencies**

### **System Requirements**
- **AWS CLI** - For AWS resource management
- **Python 3.8+** - For running scripts
- **Git** - For version control

### **Python Libraries**
- **`boto3`** - AWS SDK for Python
- **`requests`** - HTTP library for load generation
- **`urllib3`** - HTTP client library

### **System Tools**
- **`watch`** - For real-time monitoring
- **`weasyprint`** - For PDF generation

## 🔧 **Installation Options**

### **Option 1: Automated Installation**
```bash
./install.sh
```

### **Option 2: Manual Installation**
```bash
# Install AWS CLI
brew install awscli  # macOS
sudo apt-get install awscli  # Linux

# Install Python dependencies
pip3 install -r requirements.txt

# Install system tools
brew install watch weasyprint  # macOS
sudo apt-get install procps && pip3 install weasyprint  # Linux
```

## 🎯 **Deployment Options**

### **Option 1: Automated Deployment (Recommended)**
```bash
./deploy-perfect.sh
```

### **Option 2: Manual Deployment**
```bash
# Follow README-MANUAL.md for step-by-step instructions
```

### **Option 3: Prompt-Based Deployment**
```bash
# Follow README-PROMPT.md for command-by-command instructions
```

## 📚 **Documentation**

- **`DOCUMENTATION.pdf`** - Complete project documentation with code explanations
- **`SETUP-GUIDE.md`** - Detailed setup and installation guide
- **`README-CLEAN.md`** - Clean deployment guide
- **`README-MANUAL.md`** - Manual deployment guide
- **`README-PROMPT.md`** - Prompt-based deployment guide

## 🔍 **Verification Commands**

### **Check Prerequisites**
```bash
# AWS CLI
aws --version

# Python dependencies
python3 -c "import boto3, requests; print('All dependencies installed!')"

# System tools
watch --version
weasyprint --version
```

### **Test Deployment**
```bash
# Deploy infrastructure
./deploy-perfect.sh

# Test ALB connectivity
curl http://YOUR-ALB-DNS.ap-south-1.elb.amazonaws.com

# Run load generator
python3 loadgen.py http://YOUR-ALB-DNS.ap-south-1.elb.amazonaws.com 50 --duration 60

# Monitor auto-scaling
watch -n 5 'aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names autoscale-demo-asg --query "AutoScalingGroups[0].DesiredCapacity" --output text'
```

## 🚨 **Troubleshooting**

### **Common Issues**
1. **AWS Credentials Not Found** → Run `aws configure`
2. **Python Module Not Found** → Run `pip3 install -r requirements.txt`
3. **Permission Denied** → Run `chmod +x *.sh`
4. **Command Not Found (watch)** → Install via package manager

### **Support Files**
- **`SETUP-GUIDE.md`** - Complete troubleshooting guide
- **`DOCUMENTATION.pdf`** - Detailed error resolution

## 🎉 **Ready to Use!**

**All files are ready for:**
- ✅ Easy deployment
- ✅ Complete documentation
- ✅ Automated installation
- ✅ Multiple deployment options
- ✅ Comprehensive troubleshooting

**Perfect for workshops, demos, and learning AWS auto-scaling!** 🚀
