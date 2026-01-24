from flask import Flask, jsonify, request
from flask_cors import CORS
import redis
import requests
import os
import sys
import time

app = Flask(__name__)
CORS(app)

# Use REDIS_HOST from Env
REDIS_HOST = os.getenv("REDIS_HOST", "redis-db")

# Industry Standard: Retry connection loop
r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

def connect_redis():
    retry_count = 5
    while retry_count > 0:
        try:
            r.ping()
            print("Successfully connected to Redis")
            return True
        except Exception as e:
            print(f"Redis not ready... retrying in 2s ({retry_count} attempts left). Error: {e}")
            time.sleep(2)
            retry_count -= 1
    return False

if not connect_redis():
    print("CRITICAL: Could not connect to Redis after retries.")
    # We don't exit(1) here so the health check can still report 'ok' 
    # but the logs will show us the truth.

def get_my_current_wan():
    try:
        # Short timeout to prevent the "Loading..." delay
        return requests.get('https://api.ipify.org', timeout=1).text
    except:
        return None

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/visit")
def hit():
    try:
        # Extract IP
        x_forwarded = request.headers.get('X-Forwarded-For')
        visitor_ip = x_forwarded.split(',')[0].strip() if x_forwarded else request.remote_addr
        
        print(f"ACTIVITY: Visit from {visitor_ip}")

        current_wan = get_my_current_wan()
        
        is_home = (
            visitor_ip.startswith("192.168.50.") or 
            visitor_ip == "127.0.0.1" or 
            (current_wan and visitor_ip == current_wan)
        )

        if is_home:
            count = r.incr("hits")
            return jsonify({"hits": int(count), "type": "admin"})

        # Rate limiting logic
        lock_key = f"limit:{visitor_ip}"
        is_new = r.set(lock_key, "1", ex=86400, nx=True)

        if is_new:
            count = r.incr("hits")
        else:
            val = r.get("hits")
            count = int(val) if val else 0
            
        return jsonify({"hits": count, "type": "external"})

    except Exception as e:
        # THIS IS THE CRITICAL PART: It will print why it's failing to your logs
        print(f"!!! ROUTE ERROR: {e}")
        import traceback
        traceback.print_exc() 
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # PRODUCTION SETTINGS: debug=False, use_reloader=False
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
