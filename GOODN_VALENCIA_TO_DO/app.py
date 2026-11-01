import os
import psycopg
from flask import Flask, render_template, jsonify
from psycopg.rows import dict_row

app = Flask(__name__, template_folder="templates")

DATABASE_URL = os.environ.get("DATABASE_URL")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/location")
def get_location():
    try:
        with psycopg.connect(
            DATABASE_URL,
            row_factory=dict_row,
            connect_timeout=10
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        imei,
                        latitude,
                        longitude,
                        speed,
                        battery,
                        received_at
                    FROM tracker_packets
                    WHERE latitude IS NOT NULL
                      AND longitude IS NOT NULL
                    ORDER BY received_at DESC NULLS LAST, id DESC
                    LIMIT 1
                """)

                location = cur.fetchone()

        if not location:
            return jsonify({
                "success": False,
                "message": "No GPS location available"
            })

        location["received_at"] = (
            location["received_at"].isoformat()
            if location["received_at"] else None
        )

        return jsonify({
            "success": True,
            "location": location
        })

    except Exception:
        app.logger.exception("Database read failed")
        return jsonify({
            "success": False,
            "message": "Unable to retrieve GPS location"
        }), 500
