#!/usr/bin/env python3
"""
Load Generator for AI-Driven AutoScaling Demo

This script generates HTTP traffic to test the auto-scaling functionality
of the AI-Driven AutoScaling Agent on AWS.

Usage:
    python3 loadgen.py <ALB_URL> <requests_per_second> [options]

Example:
    python3 loadgen.py http://my-alb-123456789.us-east-1.elb.amazonaws.com 50

Author: AI-Driven AutoScaling Demo
"""

import requests
import time
import threading
import argparse
import sys
import signal
import statistics
from datetime import datetime
from typing import List, Dict, Optional
import urllib.parse


class LoadGenerator:
    """HTTP Load Generator for testing auto-scaling"""
    
    def __init__(self, target_url: str, requests_per_second: int, 
                 duration: Optional[int] = None, 
                 concurrent_threads: int = 10,
                 timeout: int = 30):
        """
        Initialize the Load Generator
        
        Args:
            target_url: Target URL to send requests to
            requests_per_second: Target requests per second
            duration: Duration in seconds (None for infinite)
            concurrent_threads: Number of concurrent threads
            timeout: Request timeout in seconds
        """
        self.target_url = target_url.rstrip('/')
        self.requests_per_second = requests_per_second
        self.duration = duration
        self.concurrent_threads = concurrent_threads
        self.timeout = timeout
        
        # Statistics tracking
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'response_times': [],
            'start_time': None,
            'end_time': None,
            'errors': {}
        }
        
        # Control flags
        self.running = False
        self.stop_event = threading.Event()
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        print(f"🎯 Load Generator initialized")
        print(f"Target URL: {self.target_url}")
        print(f"Target RPS: {self.requests_per_second}")
        print(f"Concurrent threads: {self.concurrent_threads}")
        print(f"Duration: {'Infinite' if duration is None else f'{duration}s'}")
        print(f"Timeout: {self.timeout}s")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\n🛑 Received signal {signum}, shutting down gracefully...")
        self.stop()
    
    def _make_request(self) -> Dict:
        """
        Make a single HTTP request
        
        Returns:
            Dictionary with request results
        """
        start_time = time.time()
        
        try:
            response = requests.get(
                self.target_url,
                timeout=self.timeout,
                headers={
                    'User-Agent': 'LoadGenerator/1.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                }
            )
            
            response_time = time.time() - start_time
            
            return {
                'success': True,
                'status_code': response.status_code,
                'response_time': response_time,
                'content_length': len(response.content),
                'error': None
            }
            
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'status_code': None,
                'response_time': time.time() - start_time,
                'content_length': 0,
                'error': 'Timeout'
            }
        except requests.exceptions.ConnectionError:
            return {
                'success': False,
                'status_code': None,
                'response_time': time.time() - start_time,
                'content_length': 0,
                'error': 'Connection Error'
            }
        except Exception as e:
            return {
                'success': False,
                'status_code': None,
                'response_time': time.time() - start_time,
                'content_length': 0,
                'error': str(e)
            }
    
    def _worker_thread(self, thread_id: int):
        """
        Worker thread that makes requests
        
        Args:
            thread_id: Thread identifier
        """
        requests_per_thread = self.requests_per_second // self.concurrent_threads
        extra_requests = self.requests_per_second % self.concurrent_threads
        
        # Distribute extra requests among first few threads
        if thread_id < extra_requests:
            requests_per_thread += 1
        
        interval = 1.0 / requests_per_thread if requests_per_thread > 0 else 1.0
        
        while self.running and not self.stop_event.is_set():
            # Make requests for this thread
            for _ in range(requests_per_thread):
                if not self.running or self.stop_event.is_set():
                    break
                
                result = self._make_request()
                
                # Update statistics
                with threading.Lock():
                    self.stats['total_requests'] += 1
                    
                    if result['success']:
                        self.stats['successful_requests'] += 1
                        self.stats['response_times'].append(result['response_time'])
                    else:
                        self.stats['failed_requests'] += 1
                        error_type = result['error']
                        self.stats['errors'][error_type] = self.stats['errors'].get(error_type, 0) + 1
            
            # Sleep for the remainder of the second
            if interval > 0:
                time.sleep(interval)
    
    def _stats_thread(self):
        """Thread that prints statistics every 10 seconds"""
        while self.running and not self.stop_event.is_set():
            time.sleep(10)
            
            if self.stats['total_requests'] > 0:
                elapsed = time.time() - self.stats['start_time']
                current_rps = self.stats['total_requests'] / elapsed
                success_rate = (self.stats['successful_requests'] / self.stats['total_requests']) * 100
                
                avg_response_time = 0
                if self.stats['response_times']:
                    avg_response_time = statistics.mean(self.stats['response_times'])
                
                print(f"📊 Stats: {self.stats['total_requests']} requests, "
                      f"{current_rps:.1f} RPS, "
                      f"{success_rate:.1f}% success, "
                      f"{avg_response_time:.3f}s avg response")
    
    def start(self):
        """Start the load generator"""
        print(f"🚀 Starting load generation...")
        
        self.running = True
        self.stats['start_time'] = time.time()
        
        # Start worker threads
        threads = []
        for i in range(self.concurrent_threads):
            thread = threading.Thread(target=self._worker_thread, args=(i,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        # Start stats thread
        stats_thread = threading.Thread(target=self._stats_thread)
        stats_thread.daemon = True
        stats_thread.start()
        
        # Wait for duration or until stopped
        if self.duration:
            print(f"⏱️  Running for {self.duration} seconds...")
            time.sleep(self.duration)
            self.stop()
        else:
            print(f"♾️  Running indefinitely (Ctrl+C to stop)...")
            try:
                while self.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.stop()
        
        # Wait for threads to finish
        for thread in threads:
            thread.join(timeout=5)
        
        self._print_final_stats()
    
    def stop(self):
        """Stop the load generator"""
        self.running = False
        self.stop_event.set()
        self.stats['end_time'] = time.time()
    
    def _print_final_stats(self):
        """Print final statistics"""
        print(f"\n📈 Final Statistics:")
        print(f"=" * 50)
        
        if self.stats['start_time'] and self.stats['end_time']:
            total_time = self.stats['end_time'] - self.stats['start_time']
            avg_rps = self.stats['total_requests'] / total_time
            
            print(f"Total time: {total_time:.1f} seconds")
            print(f"Total requests: {self.stats['total_requests']}")
            print(f"Average RPS: {avg_rps:.1f}")
            print(f"Successful requests: {self.stats['successful_requests']}")
            print(f"Failed requests: {self.stats['failed_requests']}")
            
            if self.stats['successful_requests'] > 0:
                success_rate = (self.stats['successful_requests'] / self.stats['total_requests']) * 100
                print(f"Success rate: {success_rate:.1f}%")
            
            if self.stats['response_times']:
                avg_response_time = statistics.mean(self.stats['response_times'])
                min_response_time = min(self.stats['response_times'])
                max_response_time = max(self.stats['response_times'])
                
                print(f"Response times:")
                print(f"  Average: {avg_response_time:.3f}s")
                print(f"  Min: {min_response_time:.3f}s")
                print(f"  Max: {max_response_time:.3f}s")
            
            if self.stats['errors']:
                print(f"Errors:")
                for error_type, count in self.stats['errors'].items():
                    print(f"  {error_type}: {count}")


def validate_url(url: str) -> str:
    """
    Validate and normalize URL
    
    Args:
        url: URL to validate
        
    Returns:
        Normalized URL
        
    Raises:
        ValueError: If URL is invalid
    """
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    try:
        parsed = urllib.parse.urlparse(url)
        if not parsed.netloc:
            raise ValueError("Invalid URL: no hostname")
        return url
    except Exception as e:
        raise ValueError(f"Invalid URL: {e}")


def main():
    """Main function with command line argument parsing"""
    parser = argparse.ArgumentParser(
        description='Load Generator for AI-Driven AutoScaling Demo',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate 50 requests per second indefinitely
  python3 loadgen.py http://my-alb-123456789.us-east-1.elb.amazonaws.com 50
  
  # Generate 100 requests per second for 5 minutes
  python3 loadgen.py http://my-alb-123456789.us-east-1.elb.amazonaws.com 100 --duration 300
  
  # Generate 200 requests per second with 20 concurrent threads
  python3 loadgen.py http://my-alb-123456789.us-east-1.elb.amazonaws.com 200 --threads 20
  
  # Test with HTTPS
  python3 loadgen.py https://my-alb-123456789.us-east-1.elb.amazonaws.com 75
        """
    )
    
    parser.add_argument('url', help='Target URL (ALB DNS name)')
    parser.add_argument('rps', type=int, help='Requests per second')
    parser.add_argument('--duration', type=int, 
                       help='Duration in seconds (default: infinite)')
    parser.add_argument('--threads', type=int, default=10,
                       help='Number of concurrent threads (default: 10)')
    parser.add_argument('--timeout', type=int, default=30,
                       help='Request timeout in seconds (default: 30)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.rps <= 0:
        print("Error: requests per second must be positive")
        sys.exit(1)
    
    if args.threads <= 0:
        print("Error: number of threads must be positive")
        sys.exit(1)
    
    if args.timeout <= 0:
        print("Error: timeout must be positive")
        sys.exit(1)
    
    try:
        validated_url = validate_url(args.url)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    # Create and run load generator
    try:
        generator = LoadGenerator(
            target_url=validated_url,
            requests_per_second=args.rps,
            duration=args.duration,
            concurrent_threads=args.threads,
            timeout=args.timeout
        )
        
        generator.start()
        
    except KeyboardInterrupt:
        print("\n🛑 Load generation interrupted by user")
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
