from app import app
from apps.products.models import Brand
import json
import time
from flask import request


@app.route('/')
def index():
    return json.dumps([brand.to_dict() for brand in Brand.query.all()]), 200


@app.route('/post/', methods=['POST'])
def post():
    time.sleep(2)
    print(request.get_json(force=True))
    return "Good", 201
