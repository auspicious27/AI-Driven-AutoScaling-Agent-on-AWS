# 🚀 AI-Driven AutoScaling Agent - Prompt-Based Deployment

## 🎯 **Single Prompt Deployment**

Copy and paste this single command to deploy everything:

```bash
git clone https://github.com/auspicious27/AI-Driven-AutoScaling-Agent-on-AWS.git && cd AI-Driven-AutoScaling-Agent-on-AWS && aws ec2 describe-vpcs --filters "Name=is-default,Values=true" --query 'Vpcs[0].VpcId' --output text > vpc.txt && aws ec2 describe-subnets --filters "Name=vpc-id,Values=$(cat vpc.txt)" --query 'Subnets[?MapPublicIpOnLaunch==`true`].SubnetId' --output text > subnets.txt && aws ec2 describe-images --owners amazon --filters "Name=name,Values=amzn2-ami-hvm-*-x86_64-gp2" --query 'Images[0].ImageId' --output text > ami.txt && aws ec2 create-key-pair --key-name autoscale-demo-key --query 'KeyMaterial' --output text > autoscale-demo-key.pem 2>/dev/null || echo "Key pair already exists" && chmod 400 autoscale-demo-key.pem 2>/dev/null || echo "Key permissions set" && aws cloudformation deploy --template-file autoscale-demo.yml --stack-name autoscale-demo --parameter-overrides KeyName=autoscale-demo-key VpcId=$(cat vpc.txt) PublicSubnets=$(cat subnets.txt) ImageId=$(cat ami.txt) InstanceType=t3.micro --capabilities CAPABILITY_IAM && aws cloudformation describe-stacks --stack-name autoscale-demo --query "Stacks[0].Outputs" --output json > alb-output.json && echo "🎉 DEPLOYMENT COMPLETE! Check alb-output.json for ALB DNS"
```

## 🎮 **Testing Prompts**

### **Test ALB Connectivity:**
```bash
curl http://$(aws cloudformation describe-stacks --stack-name autoscale-demo --query "Stacks[0].Outputs[?OutputKey=='ALBDNSName'].OutputValue" --output text)
```

### **Check Current Capacity:**
```bash
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names autoscale-demo-asg --query 'AutoScalingGroups[0].DesiredCapacity' --output text
```

### **Scale UP to 3 instances:**
```bash
aws autoscaling set-desired-capacity --auto-scaling-group-name autoscale-demo-asg --desired-capacity 3
```

### **Scale DOWN to 1 instance:**
```bash
aws autoscaling set-desired-capacity --auto-scaling-group-name autoscale-demo-asg --desired-capacity 1
```

### **Run Load Generator:**
```bash
python3 loadgen.py http://$(aws cloudformation describe-stacks --stack-name autoscale-demo --query "Stacks[0].Outputs[?OutputKey=='ALBDNSName'].OutputValue" --output text) 50 --duration 60
```

### **Monitor Scaling Activities:**
```bash
aws autoscaling describe-scaling-activities --auto-scaling-group-name autoscale-demo-asg --query 'Activities[].{Time:StartTime,Status:StatusCode,Description:Description}' --output table
```

### **Get Instance Details:**
```bash
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names autoscale-demo-asg --query 'AutoScalingGroups[0].Instances[].{InstanceId:InstanceId,State:LifecycleState,Health:HealthStatus}' --output table
```

### **Check CloudFormation Events:**
```bash
aws cloudformation describe-stack-events --stack-name autoscale-demo --query 'StackEvents[].{Time:Timestamp,Status:ResourceStatus,Type:ResourceType,Reason:ResourceStatusReason}' --output table
```

## 🧪 **Complete Demo Sequence**

### **Step 1: Deploy Everything**
```bash
git clone https://github.com/auspicious27/AI-Driven-AutoScaling-Agent-on-AWS.git && cd AI-Driven-AutoScaling-Agent-on-AWS && aws ec2 describe-vpcs --filters "Name=is-default,Values=true" --query 'Vpcs[0].VpcId' --output text > vpc.txt && aws ec2 describe-subnets --filters "Name=vpc-id,Values=$(cat vpc.txt)" --query 'Subnets[?MapPublicIpOnLaunch==`true`].SubnetId' --output text > subnets.txt && aws ec2 describe-images --owners amazon --filters "Name=name,Values=amzn2-ami-hvm-*-x86_64-gp2" --query 'Images[0].ImageId' --output text > ami.txt && aws ec2 create-key-pair --key-name autoscale-demo-key --query 'KeyMaterial' --output text > autoscale-demo-key.pem 2>/dev/null || echo "Key pair already exists" && chmod 400 autoscale-demo-key.pem 2>/dev/null || echo "Key permissions set" && aws cloudformation deploy --template-file autoscale-demo.yml --stack-name autoscale-demo --parameter-overrides KeyName=autoscale-demo-key VpcId=$(cat vpc.txt) PublicSubnets=$(cat subnets.txt) ImageId=$(cat ami.txt) InstanceType=t3.micro --capabilities CAPABILITY_IAM
```

### **Step 2: Test ALB**
```bash
curl http://$(aws cloudformation describe-stacks --stack-name autoscale-demo --query "Stacks[0].Outputs[?OutputKey=='ALBDNSName'].OutputValue" --output text)
```

### **Step 3: Scale UP**
```bash
aws autoscaling set-desired-capacity --auto-scaling-group-name autoscale-demo-asg --desired-capacity 3
```

### **Step 4: Scale DOWN**
```bash
aws autoscaling set-desired-capacity --auto-scaling-group-name autoscale-demo-asg --desired-capacity 1
```

### **Step 5: Load Test**
```bash
python3 loadgen.py http://$(aws cloudformation describe-stacks --stack-name autoscale-demo --query "Stacks[0].Outputs[?OutputKey=='ALBDNSName'].OutputValue" --output text) 50 --duration 60
```

### **Step 6: Monitor**
```bash
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names autoscale-demo-asg --query 'AutoScalingGroups[0].DesiredCapacity' --output text
```

## 🛑 **Cleanup Prompt**

```bash
aws cloudformation delete-stack --stack-name autoscale-demo && aws cloudformation wait stack-delete-complete --stack-name autoscale-demo && echo "✅ Cleanup Complete!"
```

## 🎯 **Workshop Demo Prompts**

### **"Show Single Prompt Deployment"**
```bash
git clone https://github.com/auspicious27/AI-Driven-AutoScaling-Agent-on-AWS.git && cd AI-Driven-AutoScaling-Agent-on-AWS && aws ec2 describe-vpcs --filters "Name=is-default,Values=true" --query 'Vpcs[0].VpcId' --output text > vpc.txt && aws ec2 describe-subnets --filters "Name=vpc-id,Values=$(cat vpc.txt)" --query 'Subnets[?MapPublicIpOnLaunch==`true`].SubnetId' --output text > subnets.txt && aws ec2 describe-images --owners amazon --filters "Name=name,Values=amzn2-ami-hvm-*-x86_64-gp2" --query 'Images[0].ImageId' --output text > ami.txt && aws ec2 create-key-pair --key-name autoscale-demo-key --query 'KeyMaterial' --output text > autoscale-demo-key.pem 2>/dev/null || echo "Key pair already exists" && chmod 400 autoscale-demo-key.pem 2>/dev/null || echo "Key permissions set" && aws cloudformation deploy --template-file autoscale-demo.yml --stack-name autoscale-demo --parameter-overrides KeyName=autoscale-demo-key VpcId=$(cat vpc.txt) PublicSubnets=$(cat subnets.txt) ImageId=$(cat ami.txt) InstanceType=t3.micro --capabilities CAPABILITY_IAM
```

### **"Show AI Agent Monitoring"**
```bash
aws autoscaling describe-scaling-activities --auto-scaling-group-name autoscale-demo-asg --query 'Activities[].{Time:StartTime,Status:StatusCode,Description:Description}' --output table
```

### **"Show Auto-scaling in Action"**
```bash
aws autoscaling set-desired-capacity --auto-scaling-group-name autoscale-demo-asg --desired-capacity 3 && sleep 30 && aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names autoscale-demo-asg --query 'AutoScalingGroups[0].DesiredCapacity' --output text
```

### **"Show Load Testing"**
```bash
python3 loadgen.py http://$(aws cloudformation describe-stacks --stack-name autoscale-demo --query "Stacks[0].Outputs[?OutputKey=='ALBDNSName'].OutputValue" --output text) 100 --duration 60
```

## 🎉 **Perfect for Workshop!**

- **✅ Single Prompt Deployment** - No shell scripts
- **✅ Direct AWS CLI Commands** - Pure prompt-based
- **✅ Live Demo Ready** - Copy-paste commands
- **✅ Real-time Results** - Immediate feedback
- **✅ Workshop Perfect** - Exactly what you promised!

**Now you have pure prompt-based deployment!** 🚀✨
