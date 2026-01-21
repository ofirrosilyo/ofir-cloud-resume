from flask import Flask, jsonify
from flask_cors import CORS
import redis

app = Flask(__name__)
CORS(app)

# Connect to Redis
r = redis.Redis(host="redis-db", port=6379, decode_responses=True)

@app.route("/health")
def health():
    """Health check route for Kubernetes liveness and readiness probes"""
    return jsonify({"status": "ok"}), 200

@app.route("/visit")
def hit():
    try:
        count = r.incr("hits")
        return jsonify({"hits": count})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
