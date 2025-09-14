#!/bin/bash

# AI-Driven AutoScaling Agent - Installation Script
# =================================================

set -e

echo "🚀 AI-Driven AutoScaling Agent - Installation Script"
echo "===================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on macOS or Linux
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
    PACKAGE_MANAGER="brew"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
    PACKAGE_MANAGER="apt"
else
    print_error "Unsupported operating system: $OSTYPE"
    exit 1
fi

print_status "Detected OS: $OS"

# Function to install AWS CLI
install_aws_cli() {
    print_status "Installing AWS CLI..."
    
    if command -v aws &> /dev/null; then
        print_success "AWS CLI already installed: $(aws --version)"
        return 0
    fi
    
    if [[ "$OS" == "macOS" ]]; then
        if command -v brew &> /dev/null; then
            brew install awscli
        else
            print_error "Homebrew not found. Please install Homebrew first."
            exit 1
        fi
    elif [[ "$OS" == "Linux" ]]; then
        sudo apt-get update
        sudo apt-get install -y awscli
    fi
    
    if command -v aws &> /dev/null; then
        print_success "AWS CLI installed successfully: $(aws --version)"
    else
        print_error "Failed to install AWS CLI"
        exit 1
    fi
}

# Function to install Python dependencies
install_python_deps() {
    print_status "Installing Python dependencies..."
    
    # Check if Python 3 is installed
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 not found. Please install Python 3.8+ first."
        exit 1
    fi
    
    print_success "Python version: $(python3 --version)"
    
    # Install pip if not available
    if ! command -v pip3 &> /dev/null; then
        print_status "Installing pip3..."
        if [[ "$OS" == "macOS" ]]; then
            brew install python3
        elif [[ "$OS" == "Linux" ]]; then
            sudo apt-get install -y python3-pip
        fi
    fi
    
    # Install required packages
    print_status "Installing Python packages..."
    pip3 install boto3 requests urllib3
    
    # Verify installation
    python3 -c "import boto3, requests; print('All Python dependencies installed!')" 2>/dev/null
    if [ $? -eq 0 ]; then
        print_success "Python dependencies installed successfully!"
    else
        print_error "Failed to install Python dependencies"
        exit 1
    fi
}

# Function to install system tools
install_system_tools() {
    print_status "Installing system tools..."
    
    if [[ "$OS" == "macOS" ]]; then
        # Install watch command
        if ! command -v watch &> /dev/null; then
            print_status "Installing watch command..."
            brew install watch
        else
            print_success "watch command already available"
        fi
        
        # Install weasyprint for PDF generation
        if ! command -v weasyprint &> /dev/null; then
            print_status "Installing weasyprint..."
            brew install weasyprint
        else
            print_success "weasyprint already available"
        fi
        
    elif [[ "$OS" == "Linux" ]]; then
        # Install watch command
        if ! command -v watch &> /dev/null; then
            print_status "Installing watch command..."
            sudo apt-get install -y procps
        else
            print_success "watch command already available"
        fi
        
        # Install weasyprint for PDF generation
        if ! command -v weasyprint &> /dev/null; then
            print_status "Installing weasyprint..."
            pip3 install weasyprint
        else
            print_success "weasyprint already available"
        fi
    fi
}

# Function to configure AWS credentials
configure_aws() {
    print_status "Configuring AWS credentials..."
    
    if aws sts get-caller-identity &> /dev/null; then
        print_success "AWS credentials already configured"
        aws sts get-caller-identity --output table
        return 0
    fi
    
    print_warning "AWS credentials not configured. Please run 'aws configure' to set up your credentials."
    print_status "You will need:"
    echo "  - AWS Access Key ID"
    echo "  - AWS Secret Access Key"
    echo "  - Default region (e.g., ap-south-1)"
    echo "  - Default output format (json)"
    
    read -p "Do you want to configure AWS credentials now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        aws configure
        if aws sts get-caller-identity &> /dev/null; then
            print_success "AWS credentials configured successfully!"
        else
            print_error "Failed to configure AWS credentials"
            exit 1
        fi
    else
        print_warning "Skipping AWS configuration. You can run 'aws configure' later."
    fi
}

# Function to make scripts executable
make_executable() {
    print_status "Making scripts executable..."
    
    if [ -f "deploy-perfect.sh" ]; then
        chmod +x deploy-perfect.sh
        print_success "deploy-perfect.sh made executable"
    fi
    
    if [ -f "agent.py" ]; then
        chmod +x agent.py
        print_success "agent.py made executable"
    fi
    
    if [ -f "loadgen.py" ]; then
        chmod +x loadgen.py
        print_success "loadgen.py made executable"
    fi
}

# Main installation process
main() {
    print_status "Starting installation process..."
    
    # Install AWS CLI
    install_aws_cli
    
    # Install Python dependencies
    install_python_deps
    
    # Install system tools
    install_system_tools
    
    # Configure AWS credentials
    configure_aws
    
    # Make scripts executable
    make_executable
    
    print_success "Installation completed successfully!"
    echo
    print_status "Next steps:"
    echo "1. Run: ./deploy-perfect.sh"
    echo "2. Follow the deployment instructions"
    echo "3. Test the auto-scaling system"
    echo
    print_success "Ready to deploy! 🚀"
}

# Run main function
main "$@"
