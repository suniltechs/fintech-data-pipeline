# server.py
import os
from flask import Flask, jsonify, request
from threading import Thread
from src.pipeline import run_pipeline  # your existing pipeline function

app = Flask(__name__)

# Admin token to protect /run - set this in Railway variables
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN")

def _run_pipeline_thread():
    try:
        run_pipeline()
    except Exception as e:
        # keep logs simple so Railway captures them
        app.logger.exception("Pipeline failed: %s", e)

@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "message": "Fintech Data Pipeline deployed. Use POST /run (with token) to trigger."
    }), 200

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/run", methods=["POST", "GET"])
def run_endpoint():
    # Accept token either as header X-Admin-Token or ?token= in query
    token = request.headers.get("X-Admin-Token") or request.args.get("token")
    if ADMIN_TOKEN and token != ADMIN_TOKEN:
        return jsonify({"error": "unauthorized"}), 401

    # Run pipeline in background thread so HTTP response returns quickly
    t = Thread(target=_run_pipeline_thread, daemon=True)
    t.start()

    return jsonify({
        "status": "started",
        "message": "Pipeline started in background. Check logs for progress."
    }), 202

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    # serve on 0.0.0.0 so Railway can route to it
    app.run(host="0.0.0.0", port=port)
