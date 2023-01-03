import json


def custom_response(json_data, custom_response, custom_status_code):
    message = None
    if custom_response is not None:
        message = { "message": custom_response, "body": json_data }
    else:
        message = json_data
    response = {
        "statusCode": custom_status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(message)
    }
    return response

def success_response(json_data):
    return custom_response(json_data, None, 200)

def bad_request_error(json_data):
    return custom_response(json_data, None, 400)

def not_found_error(json_data):
    return custom_response(json_data, None, 404)

def invalid_request_error(json_data):
    return custom_response(json_data, None, 422)

def conflict_request_error(json_data):
    return custom_response(json_data, None, 409)