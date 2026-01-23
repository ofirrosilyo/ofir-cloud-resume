from flask import Flask, jsonify, request
from flask_cors import CORS
import redis
import requests
import os

app = Flask(__name__)
CORS(app)

# Pulls Redis host from Env Var, defaults to your StatefulSet name
REDIS_HOST = os.getenv("REDIS_HOST", "redis-db")
r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

def get_my_current_wan():
    """Dynamically identifies your home IP for Zero Trust bypass"""
    try:
        return requests.get('https://api.ipify.org', timeout=2).text
    except:
        return None

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/visit")
def hit():
    try:
        # 1. Get IP safely
        x_forwarded = request.headers.get('X-Forwarded-For')
        if x_forwarded:
            visitor_ip = x_forwarded.split(',')[0].strip()
        else:
            visitor_ip = request.remote_addr

        # Log it so we can see it in 'kubectl logs'
        print(f"Processing visit from: {visitor_ip}")

        # 2. WAN check with a 'None' fallback so it never crashes
        current_wan = None
        try:
            current_wan = get_my_current_wan()
        except:
            print("Warning: Could not fetch WAN IP")

        # 3. Admin Check
        is_home = (
            visitor_ip.startswith("192.168.50.") or 
            visitor_ip == "127.0.0.1" or 
            (current_wan and visitor_ip == current_wan)
        )

        if is_home:
            count = r.incr("hits")
            return jsonify({"hits": int(count), "type": "admin"})

        # 4. External visitor logic
        lock_key = f"limit:{visitor_ip}"
        is_new = r.set(lock_key, "1", ex=86400, nx=True)

        # Safely get count from Redis
        raw_count = r.get("hits")
        current_count = int(raw_count) if raw_count else 0

        if is_new:
            current_count = r.incr("hits")
        
        return jsonify({"hits": int(current_count), "type": "external"})

    except Exception as e:
        # This will print the EXACT error to your 'kubectl logs'
        print(f"CRITICAL ERROR: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500
