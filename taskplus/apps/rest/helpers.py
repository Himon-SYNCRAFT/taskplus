import json
from flask import Response


def json_response(data, encoder, status=200):
    """ Return flask.Response based on data and it's encoder """
    return Response(json.dumps(data, cls=encoder),
                    mimetype='application/json',
                    status=status)
