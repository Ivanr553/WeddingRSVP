import json
from typing import Optional
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
    children: str
    attending: str
    partner: Optional[str] = None
    
    def __str__(self):
        return f"Name:{self.name},partner:{self.partner},Email:{self.email},Children:{self.children},Attending:{self.attending}"

def validate_rsvp_data(rsvp_data):
    if not rsvp_data.name or not rsvp_data.email or rsvp_data.attending is None:
        return False
    return True

@app.route("/rsvp", methods=["POST"])
def add_rsvp():
    try:
        data = request.json
        rsvp_data = RSVPData(**data)
        if not validate_rsvp_data(rsvp_data):
            return "Invalid data", 400
    except Exception as e:
        print(e)
        return "Invalid data", 400
    try:
        stringified_data = str(rsvp_data)
        with open("rsvp.txt", "a") as f:
            f.write(stringified_data + "\n")
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
