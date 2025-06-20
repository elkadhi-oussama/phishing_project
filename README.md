# 🛡️ Educational Phishing Page Simulation

This project simulates a fake login page using Flask, for **educational and ethical hacking training purposes only**.

## 📂 Project Structure

- `app.py` – Flask server to collect fake login data
- `templates/login.html` – HTML for fake login page
- `static/style.css` – Basic CSS styling
- `log.txt` – Stores captured data (not used maliciously!)

## ⚠️ Legal Warning

> **This project is for educational use only. Do not use it against any real systems, users, or organizations without explicit, written permission. Unauthorized use may violate laws and regulations.**

## 🚀 Run Locally

### 🧱 1. Install dependencies

```bash
sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate
pip install flask waitress user_agents


## Run the Server

- Basic usage (defaults to Facebook):

```bash
python app.py

- Advanced options:

```bash
python app.py \
  --platform [facebook|instagram|linkedin] \
  --redirect "https://your-redirect-url.com"

- Example:

```bash
python app.py --platform instagram --redirect "https://instagram.com"