#!/usr/bin/env python3
"""
AI-Driven AutoScaling Agent

This script monitors CloudWatch metrics for Application Load Balancer request count
and automatically scales EC2 instances up or down based on traffic patterns.

Scaling Logic:
- Scale UP: When requests/min > 120 (add 1 instance, max 4)
- Scale DOWN: When requests/min < 60 (remove 1 instance, min 1)

Author: AI-Driven AutoScaling Demo
"""

import boto3
import time
import logging
import argparse
import sys
from datetime import datetime, timedelta
from typing import Optional, Tuple


class AutoScalingAgent:
    """AI-Driven AutoScaling Agent for AWS EC2 instances"""
    
    def __init__(self, asg_name: str, alb_arn: str, 
                 scale_up_threshold: int = 120, 
                 scale_down_threshold: int = 60,
                 min_capacity: int = 1, 
                 max_capacity: int = 4,
                 log_file: str = '/home/ec2-user/agent.log'):
        """
        Initialize the AutoScaling Agent
        
        Args:
            asg_name: Name of the Auto Scaling Group
            alb_arn: ARN of the Application Load Balancer
            scale_up_threshold: Requests per minute threshold to scale up
            scale_down_threshold: Requests per minute threshold to scale down
            min_capacity: Minimum number of instances
            max_capacity: Maximum number of instances
            log_file: Path to log file
        """
        self.asg_name = asg_name
        self.alb_arn = alb_arn
        self.scale_up_threshold = scale_up_threshold
        self.scale_down_threshold = scale_down_threshold
        self.min_capacity = min_capacity
        self.max_capacity = max_capacity
        
        # Initialize AWS clients
        try:
            self.cloudwatch = boto3.client('cloudwatch')
            self.autoscaling = boto3.client('autoscaling')
        except Exception as e:
            print(f"Error initializing AWS clients: {e}")
            sys.exit(1)
        
        # Configure logging
        self._setup_logging(log_file)
        
        # Extract ALB name from ARN for CloudWatch metrics
        self.alb_name = self._extract_alb_name_from_arn(alb_arn)
        
        self.logger.info("AutoScaling Agent initialized")
        self.logger.info(f"ASG: {self.asg_name}")
        self.logger.info(f"ALB: {self.alb_name}")
        self.logger.info(f"Scale up threshold: {self.scale_up_threshold} req/min")
        self.logger.info(f"Scale down threshold: {self.scale_down_threshold} req/min")
        self.logger.info(f"Capacity range: {self.min_capacity} - {self.max_capacity}")
    
    def _setup_logging(self, log_file: str):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _extract_alb_name_from_arn(self, alb_arn: str) -> str:
        """Extract ALB name from ARN"""
        try:
            # ALB ARN format: arn:aws:elasticloadbalancing:region:account:loadbalancer/app/name/id
            parts = alb_arn.split('/')
            if len(parts) >= 3:
                return f"app/{parts[2]}/{parts[3]}"
            else:
                # Fallback: try to extract from the end of ARN
                return alb_arn.split('/')[-1]
        except Exception as e:
            self.logger.error(f"Error extracting ALB name from ARN: {e}")
            return alb_arn
    
    def get_request_count(self) -> float:
        """
        Get request count per minute from CloudWatch
        
        Returns:
            Average requests per minute over the last 5 minutes
        """
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(minutes=5)
            
            response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/ApplicationELB',
                MetricName='RequestCount',
                Dimensions=[
                    {
                        'Name': 'LoadBalancer',
                        'Value': self.alb_name
                    }
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,  # 5 minutes
                Statistics=['Sum']
            )
            
            if response['Datapoints']:
                # Calculate average requests per minute
                total_requests = sum(point['Sum'] for point in response['Datapoints'])
                avg_requests_per_minute = total_requests / len(response['Datapoints'])
                return avg_requests_per_minute
            else:
                self.logger.warning("No CloudWatch datapoints found")
                return 0.0
                
        except Exception as e:
            self.logger.error(f"Error getting request count: {e}")
            return 0.0
    
    def get_current_capacity(self) -> int:
        """
        Get current desired capacity of Auto Scaling Group
        
        Returns:
            Current desired capacity
        """
        try:
            response = self.autoscaling.describe_auto_scaling_groups(
                AutoScalingGroupNames=[self.asg_name]
            )
            
            if response['AutoScalingGroups']:
                asg = response['AutoScalingGroups'][0]
                desired_capacity = asg['DesiredCapacity']
                actual_capacity = len(asg['Instances'])
                self.logger.debug(f"Desired: {desired_capacity}, Actual: {actual_capacity}")
                return desired_capacity
            else:
                self.logger.error(f"Auto Scaling Group '{self.asg_name}' not found")
                return 0
                
        except Exception as e:
            self.logger.error(f"Error getting current capacity: {e}")
            return 0
    
    def scale_up(self) -> bool:
        """
        Scale up by 1 instance
        
        Returns:
            True if scaling was successful, False otherwise
        """
        try:
            current_capacity = self.get_current_capacity()
            
            if current_capacity >= self.max_capacity:
                self.logger.info(f"Cannot scale up: already at max capacity ({self.max_capacity})")
                return False
            
            new_capacity = current_capacity + 1
            
            self.autoscaling.set_desired_capacity(
                AutoScalingGroupName=self.asg_name,
                DesiredCapacity=new_capacity,
                HonorCooldown=True
            )
            
            self.logger.info(f"✅ Scaling UP: {current_capacity} -> {new_capacity} instances")
            return True
            
        except Exception as e:
            self.logger.error(f"Error scaling up: {e}")
            return False
    
    def scale_down(self) -> bool:
        """
        Scale down by 1 instance
        
        Returns:
            True if scaling was successful, False otherwise
        """
        try:
            current_capacity = self.get_current_capacity()
            
            if current_capacity <= self.min_capacity:
                self.logger.info(f"Cannot scale down: already at min capacity ({self.min_capacity})")
                return False
            
            new_capacity = current_capacity - 1
            
            self.autoscaling.set_desired_capacity(
                AutoScalingGroupName=self.asg_name,
                DesiredCapacity=new_capacity,
                HonorCooldown=True
            )
            
            self.logger.info(f"✅ Scaling DOWN: {current_capacity} -> {new_capacity} instances")
            return True
            
        except Exception as e:
            self.logger.error(f"Error scaling down: {e}")
            return False
    
    def get_scaling_recommendation(self, requests_per_minute: float) -> Tuple[str, str]:
        """
        Get scaling recommendation based on current metrics
        
        Args:
            requests_per_minute: Current requests per minute
            
        Returns:
            Tuple of (action, reason)
        """
        if requests_per_minute > self.scale_up_threshold:
            return "SCALE_UP", f"High traffic: {requests_per_minute:.1f} req/min > {self.scale_up_threshold}"
        elif requests_per_minute < self.scale_down_threshold:
            return "SCALE_DOWN", f"Low traffic: {requests_per_minute:.1f} req/min < {self.scale_down_threshold}"
        else:
            return "NO_ACTION", f"Normal traffic: {requests_per_minute:.1f} req/min"
    
    def run(self, check_interval: int = 60):
        """
        Main monitoring loop
        
        Args:
            check_interval: Seconds between checks
        """
        self.logger.info("🚀 Starting AutoScaling Agent monitoring loop...")
        self.logger.info(f"Check interval: {check_interval} seconds")
        
        consecutive_high_traffic = 0
        consecutive_low_traffic = 0
        
        while True:
            try:
                # Get current metrics
                requests_per_minute = self.get_request_count()
                current_capacity = self.get_current_capacity()
                
                # Log current status
                self.logger.info(f"📊 Status: {requests_per_minute:.1f} req/min, Capacity: {current_capacity}")
                
                # Get scaling recommendation
                action, reason = self.get_scaling_recommendation(requests_per_minute)
                
                # Implement scaling logic with hysteresis to prevent flapping
                if action == "SCALE_UP":
                    consecutive_high_traffic += 1
                    consecutive_low_traffic = 0
                    
                    # Scale up after 2 consecutive high traffic readings
                    if consecutive_high_traffic >= 2:
                        self.logger.info(f"🔥 {reason}")
                        self.scale_up()
                        consecutive_high_traffic = 0
                    else:
                        self.logger.info(f"⚠️  High traffic detected, waiting for confirmation... ({consecutive_high_traffic}/2)")
                        
                elif action == "SCALE_DOWN":
                    consecutive_low_traffic += 1
                    consecutive_high_traffic = 0
                    
                    # Scale down after 3 consecutive low traffic readings (more conservative)
                    if consecutive_low_traffic >= 3:
                        self.logger.info(f"❄️  {reason}")
                        self.scale_down()
                        consecutive_low_traffic = 0
                    else:
                        self.logger.info(f"⚠️  Low traffic detected, waiting for confirmation... ({consecutive_low_traffic}/3)")
                        
                else:
                    consecutive_high_traffic = 0
                    consecutive_low_traffic = 0
                    self.logger.info(f"✅ {reason}")
                
                # Wait before next check
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                self.logger.info("🛑 Agent stopped by user")
                break
            except Exception as e:
                self.logger.error(f"💥 Unexpected error in monitoring loop: {e}")
                time.sleep(check_interval)


def main():
    """Main function with command line argument parsing"""
    parser = argparse.ArgumentParser(description='AI-Driven AutoScaling Agent')
    parser.add_argument('--asg-name', required=True, help='Auto Scaling Group name')
    parser.add_argument('--alb-arn', required=True, help='Application Load Balancer ARN')
    parser.add_argument('--scale-up-threshold', type=int, default=120, 
                       help='Requests per minute threshold to scale up (default: 120)')
    parser.add_argument('--scale-down-threshold', type=int, default=60,
                       help='Requests per minute threshold to scale down (default: 60)')
    parser.add_argument('--min-capacity', type=int, default=1,
                       help='Minimum number of instances (default: 1)')
    parser.add_argument('--max-capacity', type=int, default=4,
                       help='Maximum number of instances (default: 4)')
    parser.add_argument('--check-interval', type=int, default=60,
                       help='Check interval in seconds (default: 60)')
    parser.add_argument('--log-file', default='/home/ec2-user/agent.log',
                       help='Log file path (default: /home/ec2-user/agent.log)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.scale_up_threshold <= args.scale_down_threshold:
        print("Error: scale-up-threshold must be greater than scale-down-threshold")
        sys.exit(1)
    
    if args.min_capacity >= args.max_capacity:
        print("Error: min-capacity must be less than max-capacity")
        sys.exit(1)
    
    # Create and run agent
    try:
        agent = AutoScalingAgent(
            asg_name=args.asg_name,
            alb_arn=args.alb_arn,
            scale_up_threshold=args.scale_up_threshold,
            scale_down_threshold=args.scale_down_threshold,
            min_capacity=args.min_capacity,
            max_capacity=args.max_capacity,
            log_file=args.log_file
        )
        
        agent.run(check_interval=args.check_interval)
        
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
