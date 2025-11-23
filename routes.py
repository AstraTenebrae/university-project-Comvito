from flask import render_template

from api_settings import app


@app.route('/')
def index():
    return "Flask работает!"

@app.route('/sketch/', methods=['GET'])
def main_route() -> tuple:
    return render_template('sketch.html'), 200