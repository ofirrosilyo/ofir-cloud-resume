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
        # Get real visitor IP from Traefik
        visitor_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        current_wan = get_my_current_wan()
        
        # Zero Trust logic: verify if requester is YOU
        is_home = (
            visitor_ip.startswith("192.168.50.") or 
            visitor_ip == "127.0.0.1" or 
            (current_wan and visitor_ip == current_wan)
        )

        if is_home:
            count = r.incr("hits")
            return jsonify({"hits": int(count), "type": "admin"})

        # Rate limiting logic for external traffic
        lock_key = f"limit:{visitor_ip}"
        is_new = r.set(lock_key, "1", ex=86400, nx=True)

        if is_new:
            count = r.incr("hits")
        else:
            count = r.get("hits") or 0
            
        return jsonify({"hits": int(count), "type": "external"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
