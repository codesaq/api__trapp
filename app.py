from flask import Flask, request
from collections import defaultdict
import time

app = Flask(__name__)
ip_tracker = defaultdict(list)

TRAPS = ["/admin", "/debug", "/config", "/internal", "/logs"]
THRESHOLD = 5
TIME_WINDOW = 30

@app.before_request
def track_trap_activity():
    ip = request.remote_addr
    path = request.path
    now = time.time()

    if path in TRAPS:
        ip_tracker[ip].append((path, now))
        ip_tracker[ip] = [(p, t) for p, t in ip_tracker[ip] if now - t <= TIME_WINDOW]
        accessed = set(p for p, t in ip_tracker[ip])
        if len(accessed) >= THRESHOLD:
            print(f"[ALERT] 🚨 Suspicious activity from IP: {ip} - Accessed traps: {accessed}")

@app.route('/')
def home():
    return "Welcome to the public API!"

@app.route('/users')
def users():
    return {"message": "Hello from /users"}

@app.route('/posts')
def posts():
    return {"message": "Hello from /posts"}

@app.route('/admin')
@app.route('/debug')
@app.route('/config')
@app.route('/internal')
@app.route('/logs')
def trap():
    return {"message": "This page does not exist."}, 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
