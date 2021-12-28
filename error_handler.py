from functools import wraps
from flask.json import jsonify
from get_db import app
from flask import jsonify,abort

@app.errorhandler(404)
def handle_404_error(error):
    app.logger.error("Called 404 error handler")
    return jsonify({"Error":"Requested data not found"}),404

@app.errorhandler(403)
def handle_403_error(error):
    app.logger.error("Called 403 error handler")
    return jsonify({"Error":"'Forbidden' You are not permitted to use requested url"}),403

@app.errorhandler(500)
def handle_500_error(error):
    app.logger.error("Called 500 error handler")
    return jsonify({"Error":"Internal server error"}),500

class NotFoundError(Exception):
    pass

def Not_Found_Error(func):
    @wraps(func)
    def Inner_Function(*args, **kwargs):
        try:
            fun=func(*args, **kwargs)
        except NotFoundError as e:
            print("inside error handler")
            app.logger.error("Record not found exception occured")
            abort(404,"Record not found")
        return fun
    return Inner_Function

