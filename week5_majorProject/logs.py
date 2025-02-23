import os
import subprocess

# Function to collect system logs
def collect_system_logs():
    # Collecting syslog
    syslog_output = subprocess.check_output(['cat', '/var/log/syslog']).decode('utf-8')
    
    # Collecting dmesg logs
    dmesg_output = subprocess.check_output(['dmesg']).decode('utf-8')
    
    # Collecting auth logs
    authlog_output = subprocess.check_output(['cat', '/var/log/auth.log']).decode('utf-8')

    # Saving logs to files
    with open('syslog.txt', 'w') as f:
        f.write(syslog_output)
    
    with open('dmesg.txt', 'w') as f:
        f.write(dmesg_output)
        
    with open('authlog.txt', 'w') as f:
        f.write(authlog_output)

if __name__ == '__main__':
    collect_system_logs()
