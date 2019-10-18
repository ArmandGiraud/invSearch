from flask import Flask

from flask import request
from flask import jsonify
from flask_cors import cross_origin
from use_terms import TermsSearch




def create_app():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False

    ts = TermsSearch("suggest_dict_f.json", "stops.txt")
    @app.route('/inv', methods=['GET'])
    @cross_origin()
    def suggest():  # pylint: disable=unused-variable
        input = request.args.get('q')
        results = ts.predict_use_terms(input)
        return jsonify(results)

    @app.route('/')
    def hello():  # pylint: disable=unused-variable
        return 'invsearch api'

    print("api is ready")
    return app


if __name__ == "__main__":
    app = create_app()

