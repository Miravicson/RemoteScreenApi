from flask import render_template, request, jsonify
from app import db
from . import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    """Return a custom 404 Http response message for missing or not found routes"""

    code = 404
    message = 'PAGE NOT FOUND'
    return jsonify({
        "message": message,
        "code": code
    }), code


@bp.app_errorhandler(405)
def method_not_found(error):
    """
    Custom response for methods not allowed for the requested URLs
    """
    code = 405
    message = 'METHOD NOT FOUND'
    return jsonify({
        "message": message,
        "code": code
    }), code
