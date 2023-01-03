from app.lambdas.sms.create.index_service import create_notification



def createNotification(event, context):
    # example email notification
    # {"user_id":"123456", "noti_data": { "location_code": "+57", "timezone":"GMT+5", "phone_number":3505784483, "message":"prueba sns","status":"awaiting"}}
    """
    Create a new notification
    """
    # TODO: ADD SCHEMA WRAPPER HANDLER
    # - Validate the request body in the schema
    # add customResponseErrorManager in api_responses.py in try-catch block
    # - If error, return the error message
    # add generalResponse when success_response
    # add DTO and cerberus validation
    return create_notification(event, context)

