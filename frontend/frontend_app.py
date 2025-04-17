from flask import Flask, render_template
from flask_swagger_ui import get_swaggerui_blueprint
import datetime


app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")



SWAGGER_URL="/api/docs"  # (1) swagger endpoint e.g. HTTP://localhost:5002/api/docs
API_URL="/static/masterblog.json" # (2) ensure you create this dir and file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Masterblog API' # (3) You can change this if you like
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
