#!/usr/bin/env python3

import argparse
import os
import requests

# Function to search for Nginx and Apache logs
def search_logs():
    nginx_logs = []
    apache_logs = []
    
    # Search for Nginx logs
    nginx_logs_path = "/var/log/nginx/"
    if os.path.exists(nginx_logs_path):
        nginx_logs = [os.path.join(nginx_logs_path, log) for log in os.listdir(nginx_logs_path) if log.startswith("access.log")]

    # Search for Apache logs
    apache_logs_path = "/var/log/apache2/"
    if os.path.exists(apache_logs_path):
        apache_logs = [os.path.join(apache_logs_path, log) for log in os.listdir(apache_logs_path) if log.startswith("access.log")]

    return nginx_logs, apache_logs

# Function to send logs to Splunk Cloud
def send_to_splunk(splunkurl, splunktoken, logs):
    url = splunkurl
    token = splunktoken
    
    headers = {
        "Authorization": f"Splunk {token}"
    }
    
    data = {
        "sourcetype": "_json",
        "event": logs
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Logs sent successfully to Splunk Cloud")
    else:
        print(f"Failed to send logs to Splunk Cloud. Status code: {response.status_code}")

# Main function
def main():
    parser = argparse.ArgumentParser(description="Splunk finder for Nginx and Apache logs that are sent to Splunk Cloud.")
    parser.add_argument("--splunkurl", help="Splunk URL for Splunk Cloud")
    parser.add_argument("--splunktoken", help="Splunk Token for Splunk Cloud")
    args = parser.parse_args()


    splunkurl = args.splunkrul
    splunktoken = args.splunktoken
    nginx_logs, apache_logs = search_logs()
    
    # Send Nginx logs to Splunk Cloud
    if nginx_logs:
        for log_file in nginx_logs:
            with open(log_file, 'r') as f:
                logs = f.readlines()
                send_to_splunk(splunkurl, splunktoken, logs)

    # Send Apache logs to Splunk Cloud
    if apache_logs:
        for log_file in apache_logs:
            with open(log_file, 'r') as f:
                logs = f.readlines()
                send_to_splunk(splunkurl, splunktoken, logs)

if __name__ == "__main__":
    main()
