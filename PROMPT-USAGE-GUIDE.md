# AI-Driven AutoScaling Agent - PROMPT USAGE GUIDE
# ================================================

## 🤖 **How to Use Prompts for Complete Deployment**

### **🚀 One Command Deployment:**

```bash
chmod +x prompt-launcher.sh && ./prompt-launcher.sh
```

### **📋 Available Prompts and Responses:**

#### **1. Prerequisites Check Prompt:**
```
[PROMPT] Would you like me to install AWS CLI? (y/n)
> y
[AI RESPONSE] Installing AWS CLI...
[SUCCESS] AWS CLI installed successfully!
```

#### **2. AWS Credentials Prompt:**
```
[PROMPT] Would you like to configure AWS credentials now? (y/n)
> y
[AI RESPONSE] Please enter your AWS credentials:
AWS Access Key ID: [Your Access Key]
AWS Secret Access Key: [Your Secret Key]
Default region name: ap-south-1
Default output format: json
[SUCCESS] AWS credentials configured successfully!
```

#### **3. Automatic Resource Detection:**
```
[AI RESPONSE] Fetching AWS resources automatically...
[SUCCESS] VPC ID: vpc-096e19eeda1c50721
[SUCCESS] Public Subnets: subnet-0986036a60ddda932,subnet-045fcfbac71b671a8
[SUCCESS] AMI ID: ami-0059e0da390478151
```

#### **4. Infrastructure Deployment:**
```
[AI RESPONSE] Deploying AWS infrastructure...
[SUCCESS] Infrastructure deployed successfully!
[SUCCESS] ALB DNS: autoscale-demo-alb-590301696.ap-south-1.elb.amazonaws.com
```

#### **5. Final Setup:**
```
[AI RESPONSE] Setting up Python dependencies...
[SUCCESS] Python dependencies installed!
[SUCCESS] Current ASG Capacity: 1
[SUCCESS] ALB is responding with HTTP 200!
```

## 🎯 **Complete Prompt Flow:**

### **Step 1: Launch**
```bash
./prompt-launcher.sh
```

### **Step 2: Follow AI Prompts**
- **Install AWS CLI?** → Type `y` or `n`
- **Configure AWS credentials?** → Type `y` or `n`
- **Enter credentials** → Follow AWS CLI prompts

### **Step 3: AI Handles Everything**
- ✅ **Automatic VPC detection**
- ✅ **Automatic subnet detection**
- ✅ **Automatic AMI selection**
- ✅ **Key pair creation**
- ✅ **Infrastructure deployment**
- ✅ **ALB setup**
- ✅ **Python dependencies**
- ✅ **Testing and verification**

## 🚀 **Advanced Prompts:**

### **Custom Deployment Prompt:**
```bash
# Deploy with custom instance type
./prompt-launcher.sh --instance-type t3.small

# Deploy with custom region
./prompt-launcher.sh --region us-east-1

# Deploy with custom stack name
./prompt-launcher.sh --stack-name my-autoscale-demo
```

### **Load Testing Prompt:**
```bash
# After deployment, run load generator
python3 loadgen.py http://YOUR-ALB-DNS.ap-south-1.elb.amazonaws.com 50 --duration 60
```

### **Monitoring Prompt:**
```bash
# Monitor auto-scaling
watch -n 5 'aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names autoscale-demo-asg --query "AutoScalingGroups[0].DesiredCapacity" --output text'
```

### **Cleanup Prompt:**
```bash
# Cleanup everything
aws cloudformation delete-stack --stack-name autoscale-demo
```

## 🎭 **Interactive Prompts:**

### **1. Installation Prompts:**
```
[PROMPT] Would you like me to install AWS CLI? (y/n)
[PROMPT] Would you like to configure AWS credentials now? (y/n)
[PROMPT] Would you like to install Python dependencies? (y/n)
```

### **2. Configuration Prompts:**
```
[PROMPT] Enter your AWS Access Key ID:
[PROMPT] Enter your AWS Secret Access Key:
[PROMPT] Enter your default region (e.g., ap-south-1):
[PROMPT] Enter your default output format (json/yaml/text):
```

### **3. Deployment Prompts:**
```
[PROMPT] Would you like to deploy the infrastructure now? (y/n)
[PROMPT] Enter instance type (t3.micro/t3.small/t3.medium):
[PROMPT] Enter stack name (default: autoscale-demo):
```

### **4. Testing Prompts:**
```
[PROMPT] Would you like to test the ALB connectivity? (y/n)
[PROMPT] Would you like to run load generator? (y/n)
[PROMPT] Enter load generator requests per second (default: 50):
```

## 🎉 **Complete Prompt Example:**

```bash
$ ./prompt-launcher.sh

🤖 AI-Driven AutoScaling Agent - PROMPT-BASED LAUNCHER
======================================================

[AI RESPONSE] Hello! I'm your AI assistant. I'll help you deploy the AI-Driven AutoScaling Agent on AWS.
[AI RESPONSE] Just follow my prompts and I'll handle everything for you!

[INFO] Checking prerequisites...
[SUCCESS] All prerequisites met!
[INFO] Fetching AWS resources...
[SUCCESS] VPC ID: vpc-096e19eeda1c50721
[SUCCESS] Public Subnets: subnet-0986036a60ddda932,subnet-045fcfbac71b671a8
[SUCCESS] AMI ID: ami-0059e0da390478151
[INFO] Creating EC2 key pair...
[SUCCESS] Key pair already exists: autoscale-demo-key
[INFO] Deploying AWS infrastructure...
[SUCCESS] Infrastructure deployed successfully!
[INFO] Getting ALB DNS name...
[SUCCESS] ALB DNS: autoscale-demo-alb-590301696.ap-south-1.elb.amazonaws.com
[INFO] Installing Python dependencies...
[SUCCESS] Python dependencies installed!
[INFO] Waiting for instances to be ready...
[SUCCESS] Current ASG Capacity: 1
[INFO] Testing ALB connectivity...
[SUCCESS] ALB is responding with HTTP 200!

🎉 DEPLOYMENT COMPLETE!
=======================
Stack Name: autoscale-demo
ALB DNS: autoscale-demo-alb-590301696.ap-south-1.elb.amazonaws.com
ASG Name: autoscale-demo-asg
Current Capacity: 1

📋 Next Steps:
1. Test ALB: curl http://autoscale-demo-alb-590301696.ap-south-1.elb.amazonaws.com
2. Run load generator: python3 loadgen.py http://autoscale-demo-alb-590301696.ap-south-1.elb.amazonaws.com 50 --duration 60
3. Monitor scaling: aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names autoscale-demo-asg --query 'AutoScalingGroups[0].DesiredCapacity' --output text
4. Manual scaling: aws autoscaling set-desired-capacity --auto-scaling-group-name autoscale-demo-asg --desired-capacity 3
5. Cleanup: aws cloudformation delete-stack --stack-name autoscale-demo

[SUCCESS] AI-Driven AutoScaling Agent is ready! 🚀
```

## 🎯 **Perfect for:**

- ✅ **Workshops** - Interactive deployment
- ✅ **Demos** - Show AI capabilities
- ✅ **Learning** - Step-by-step guidance
- ✅ **Automation** - Complete hands-off deployment
- ✅ **Troubleshooting** - Guided error resolution

**Just run one command and follow the AI prompts!** 🚀🤖
