from flask import Flask
from flask_cors import CORS
import sys

def setup_cors(app: Flask):

    print("!!! KICH HOAT CORS MOI", file=sys.stdout)
    CORS(
        app,
        resources={r"/*": {"origins": "*"}}, 
        supports_credentials=True
    )