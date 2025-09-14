# AI-Driven AutoScaling Agent - Complete Setup Guide
# ==================================================

## 🚀 **Quick Setup (One Command)**

```bash
# Clone and setup everything
git clone https://github.com/auspicious27/AI-Driven-AutoScaling-Agent-on-AWS.git
cd AI-Driven-AutoScaling-Agent-on-AWS
chmod +x deploy-perfect.sh
./deploy-perfect.sh
```

## 📋 **Prerequisites**

### 1. **AWS CLI Installation**
```bash
# macOS
brew install awscli

# Linux/Ubuntu
sudo apt-get install awscli

# Windows
# Download from: https://aws.amazon.com/cli/
```

### 2. **AWS Configuration**
```bash
aws configure
# Enter your AWS Access Key ID, Secret Access Key, and Region
```

### 3. **Python Dependencies**
```bash
# Install Python 3.8+ (if not already installed)
# macOS
brew install python3

# Linux/Ubuntu
sudo apt-get install python3 python3-pip

# Install required libraries
pip3 install -r requirements.txt
```

### 4. **System Dependencies**
```bash
# macOS
brew install watch weasyprint

# Linux/Ubuntu
sudo apt-get install procps
pip3 install weasyprint
```

## 📁 **Project Files Structure**

```
AI-Driven-AutoScaling-Agent-on-AWS/
├── autoscale-demo.yml          # CloudFormation template
├── agent.py                    # Auto-scaling agent script
├── loadgen.py                  # Load generator script
├── deploy-perfect.sh           # Automated deployment script
├── requirements.txt            # Python dependencies
├── README-CLEAN.md             # Clean deployment guide
├── README-MANUAL.md            # Manual deployment guide
├── README-PROMPT.md            # Prompt-based deployment
├── DOCUMENTATION.pdf            # Complete documentation
├── DOCUMENTATION.html           # HTML documentation
└── .gitignore                  # Git ignore file
```

## 🔧 **Manual Installation Steps**

### Step 1: Install AWS CLI
```bash
# Check if AWS CLI is installed
aws --version

# If not installed, install it:
# macOS
brew install awscli

# Linux
sudo apt-get install awscli
```

### Step 2: Configure AWS Credentials
```bash
aws configure
# Enter:
# - AWS Access Key ID: [Your Access Key]
# - AWS Secret Access Key: [Your Secret Key]
# - Default region name: ap-south-1
# - Default output format: json
```

### Step 3: Install Python Dependencies
```bash
# Install Python 3.8+ if not already installed
python3 --version

# Install required packages
pip3 install boto3 requests urllib3

# Or install from requirements file
pip3 install -r requirements.txt
```

### Step 4: Install System Tools
```bash
# macOS
brew install watch weasyprint

# Linux/Ubuntu
sudo apt-get install procps
pip3 install weasyprint
```

### Step 5: Clone Repository
```bash
git clone https://github.com/auspicious27/AI-Driven-AutoScaling-Agent-on-AWS.git
cd AI-Driven-AutoScaling-Agent-on-AWS
```

### Step 6: Make Scripts Executable
```bash
chmod +x deploy-perfect.sh
chmod +x agent.py
chmod +x loadgen.py
```

## 🎯 **Deployment Options**

### Option 1: Automated Deployment (Recommended)
```bash
./deploy-perfect.sh
```

### Option 2: Manual Deployment
```bash
# Follow README-MANUAL.md for step-by-step instructions
```

### Option 3: Prompt-Based Deployment
```bash
# Follow README-PROMPT.md for command-by-command instructions
```

## 📚 **Documentation Files**

- **`DOCUMENTATION.pdf`** - Complete project documentation
- **`DOCUMENTATION.html`** - HTML version of documentation
- **`README-CLEAN.md`** - Clean deployment guide
- **`README-MANUAL.md`** - Detailed manual deployment
- **`README-PROMPT.md`** - Prompt-based deployment

## 🔍 **Verification**

### Check AWS CLI
```bash
aws sts get-caller-identity
```

### Check Python Dependencies
```bash
python3 -c "import boto3, requests; print('All dependencies installed!')"
```

### Check System Tools
```bash
watch --version
weasyprint --version
```

## 🚨 **Troubleshooting**

### Common Issues:

1. **AWS Credentials Not Found**
   ```bash
   aws configure
   ```

2. **Python Module Not Found**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Permission Denied**
   ```bash
   chmod +x deploy-perfect.sh
   ```

4. **Command Not Found (watch)**
   ```bash
   # macOS
   brew install watch
   
   # Linux
   sudo apt-get install procps
   ```

## 🎉 **Ready to Deploy!**

Once all prerequisites are installed, run:
```bash
./deploy-perfect.sh
```

This will automatically:
- ✅ Check prerequisites
- ✅ Deploy AWS infrastructure
- ✅ Configure auto-scaling
- ✅ Test the system
- ✅ Provide next steps
