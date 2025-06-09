import json
from typing import List, Optional
from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
from dataclasses import dataclass

app = Flask(__name__)
CORS(app, resources={r"/rsvp": {"origins": ["https://www.jennaivan.wedding"]}})

@dataclass
class RSVPData:
    name: str
    email: str
    number_of_guests: int
    attending: str
    meals: List[str]

    def __str__(self):
        return f"Name:{self.name},Email:{self.email},Number Of Guests:{self.number_of_guests},Attending:{self.attending},Meals:{self.meals}"

def validate_rsvp_data(rsvp_data):
    if not rsvp_data.name or rsvp_data.attending is None:
        return False
    return True

@app.route("/rsvp", methods=["POST", "OPTIONS"])
def add_rsvp():
    if request.method == "OPTIONS":
        return "", 200
    try:
        data = request.json
        rsvp_data = RSVPData(**data)
        if not validate_rsvp_data(rsvp_data):
            return "Invalid data", 400
    except Exception as e:
        print(e)
        return "Invalid data", 400
    try:
        with open("rsvp.txt", "a") as f:
            json.dump(data, f)
            f.write("\n")
    except Exception as e:
        print(e)
        return "Error writing to file", 500
    return "OK"


def create_app():
    load_dotenv()
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=2000, debug=True)
