from flask import jsonify

def success_response(data=None, message="Success", status_code=200):
    """
    Standardized success response format.
    The response maintains the original contract expected by the legacy Java client
    by allowing flat inclusion of specific keys via kwargs if data is a dict.
    """
    response_body = {
        "success": True,
        "message": message
    }
    
    if data is not None:
        if isinstance(data, dict):
            response_body.update(data)
        else:
            response_body["data"] = data
            
    return jsonify(response_body), status_code

def error_response(message="An error occurred", code="ERROR", status_code=500):
    """
    Standardized error response format.
    Ensures 'error' key exists for legacy compatibility.
    """
    response_body = {
        "success": False,
        "error": message,
        "code": code
    }
    return jsonify(response_body), status_code
