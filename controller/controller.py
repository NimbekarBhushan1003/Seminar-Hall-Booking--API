from flask import Flask, request, jsonify
from service import service

app = Flask(__name__)

DEFAULT_STATUS = "failure"
SUCCESS_STATUS = "success"

def response_template():
    return {"status": DEFAULT_STATUS, "response": None, "error": ""}

# ---------- HEALTH CHECK ----------
@app.route("/", methods=["GET"])
def health():
    return jsonify({"message": "Seminar Hall Booking API is running"}), 200


# ---------- GET ALL BOOKINGS ----------
@app.route("/bookings", methods=["GET"])
@app.route("/assignment/bookings", methods=["GET"])
def get_bookings():
    resp = response_template()
    try:
        resp["response"] = service.fetch_all_bookings()
        resp["status"] = SUCCESS_STATUS
        return jsonify(resp), 200
    except Exception as e:
        resp["error"] = str(e)
        return jsonify(resp), 500


# ---------- BOOK SEMINAR HALL ----------
@app.route("/book", methods=["POST"])
def book_seminar_hall():
    resp = response_template()
    try:
        data = request.get_json(force=True)

        capacity = int(data.get("capacity"))
        start_time = data.get("startTime")
        end_time = data.get("endTime")

        if not all([capacity, start_time, end_time]):
            raise ValueError("capacity, startTime and endTime are required")

        if capacity > 1000:
            raise ValueError("No hall can accommodate more than 1000 people")

        # calculate availability first
        available_halls = service.get_available_halls(capacity, start_time, end_time)

        if not available_halls:
            resp["response"] = {
                "bookedHall": None,
                "availableHalls": []
            }
            resp["status"] = SUCCESS_STATUS
            return jsonify(resp), 200

        # best-fit hall
        booked_hall = available_halls[0]

        # insert booking
        service.book_best_fit_hall(capacity, start_time, end_time)

        resp["response"] = {
            "bookedHall": booked_hall,
            "availableHalls": available_halls
        }
        resp["status"] = SUCCESS_STATUS

        return jsonify(resp), 200

    except Exception as e:
        resp["error"] = str(e)
        return jsonify(resp), 400
