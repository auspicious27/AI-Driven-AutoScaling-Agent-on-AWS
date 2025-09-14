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

## 🤖 **Gen AI Project - Gemini AI Assistant Used**

This project was created using **Google Gemini AI** assistant prompts for:

- **Infrastructure Design** - AWS CloudFormation template creation
- **Code Generation** - Python scripts for auto-scaling agent and load generator
- **Documentation** - Complete project documentation and guides
- **Automation** - Shell scripts for deployment and installation
- **Troubleshooting** - Error resolution and debugging

**Gemini AI Prompts Used:**

1. **"Create a complete demo project named AI-Driven AutoScaling Agent on AWS"**
   - **Gemini Usage:** Initial project creation with AWS infrastructure
   - **Generated:** CloudFormation template, Python scripts, deployment scripts
   - **AI Model:** Google Gemini Pro

2. **"Add all required files and libraries"**
   - **Gemini Usage:** Dependencies and requirements management
   - **Generated:** requirements.txt, install.sh, system dependencies
   - **AI Model:** Google Gemini Pro

3. **"Create comprehensive documentation explaining the code in simple English"**
   - **Gemini Usage:** Documentation creation and code explanation
   - **Generated:** DOCUMENTATION.md, DOCUMENTATION.pdf, DOCUMENTATION.html
   - **AI Model:** Google Gemini Pro

4. **"Make it simple with one prompt deployment"**
   - **Gemini Usage:** Simplification and automation
   - **Generated:** deploy-perfect.sh, one-command deployment
   - **AI Model:** Google Gemini Pro

5. **"Fix all code and provide final working version"**
   - **Gemini Usage:** Error resolution and code finalization
   - **Generated:** Fixed CloudFormation template, corrected Python scripts
   - **AI Model:** Google Gemini Pro

6. **"okie abb mai isko execute kaise kar sakta"**
   - **Gemini Usage:** Execution guidance in Hindi/English
   - **Generated:** Step-by-step deployment instructions
   - **AI Model:** Google Gemini Pro

7. **"wait mujhai issmai new crenndatial add karna haii so easiky run hoo jaye"**
   - **Gemini Usage:** AWS credentials setup assistance
   - **Generated:** AWS configuration guides and scripts
   - **AI Model:** Google Gemini Pro

8. **"okie so plz run this project soo i am show the outputs"**
   - **Gemini Usage:** Project execution and testing guidance
   - **Generated:** Testing commands and output verification
   - **AI Model:** Google Gemini Pro

9. **"okie so plz guide me mai isko kaise use karsakta huu or kisi koo batana hoo toh kaise batai gaa"**
   - **Gemini Usage:** Usage guidance and presentation materials
   - **Generated:** Workshop guides and presentation materials
   - **AI Model:** Google Gemini Pro

10. **"okie so plz remove all extra file"**
    - **Gemini Usage:** Project cleanup and optimization
    - **Generated:** Cleaned project structure, removed unused files
    - **AI Model:** Google Gemini Pro

**Gemini AI Capabilities Demonstrated:**
- ✅ **Multi-language Support** - Hindi and English prompts
- ✅ **Code Generation** - Complete Python and CloudFormation code
- ✅ **Infrastructure Design** - AWS architecture and deployment
- ✅ **Documentation Creation** - Comprehensive guides and PDFs
- ✅ **Error Resolution** - Debugging and fixing issues
- ✅ **Automation Scripts** - Shell scripts for deployment
- ✅ **Project Management** - Complete project lifecycle

**This is a Gen AI Project demonstrating:**
- ✅ **AI-Assisted Development** - Complete project created with AI
- ✅ **Infrastructure as Code** - AWS resources defined programmatically
- ✅ **Automated Deployment** - One-command setup and deployment
- ✅ **Intelligent Scaling** - AI-driven auto-scaling based on metrics
- ✅ **Complete Documentation** - AI-generated comprehensive guides

## 🎉 *Ready to Deploy!*

**One command to rule them all:**
```bash
git clone https://github.com/auspicious27/AI-Driven-AutoScaling-Agent-on-AWS.git && cd AI-Driven-AutoScaling-Agent-on-AWS && chmod +x install.sh deploy-perfect.sh && ./install.sh && ./deploy-perfect.sh
```

**Perfect for workshops, demos, and learning AWS auto-scaling!** 🚀
