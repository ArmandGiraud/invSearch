from flask import Flask

from flask import request
from flask import jsonify
from flask_cors import cross_origin
from invSearch import get_related_terms


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/inv', methods=['GET'])
@cross_origin()
def suggest():  # pylint: disable=unused-variable
    input = request.args.get('q')
    results = get_related_terms(input)
    return jsonify(results)

@app.route('/')
def hello():  # pylint: disable=unused-variable
    return 'invsearch api'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3945)

