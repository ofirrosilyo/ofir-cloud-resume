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
        # 1. Properly extract the FIRST IP from the forwarded header
        x_forwarded = request.headers.get('X-Forwarded-For')
        if x_forwarded:
            # Splits "IP1, IP2" and takes "IP1"
            visitor_ip = x_forwarded.split(',')[0].strip()
        else:
            visitor_ip = request.remote_addr

        # DEBUG: Add this so you can see the real IP in 'kubectl logs'
        print(f"Request from: {visitor_ip}")

        current_wan = get_my_current_wan()
        
        # 2. Zero Trust check
        is_home = (
            visitor_ip.startswith("192.168.50.") or 
            visitor_ip == "127.0.0.1" or 
            (current_wan and visitor_ip == current_wan)
        )

        if is_home:
            count = r.incr("hits")
            return jsonify({"hits": int(count), "type": "admin"})

        # 3. Rate limiting for external traffic
        lock_key = f"limit:{visitor_ip}"
        is_new = r.set(lock_key, "1", ex=86400, nx=True)

        if is_new:
            count = r.incr("hits")
        else:
            # Handle case where Redis might return None
            val = r.get("hits")
            count = int(val) if val else 0
            
        return jsonify({"hits": count, "type": "external"})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
