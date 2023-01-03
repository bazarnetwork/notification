import json
import os
import time

import boto3

from .notification_helper import SnsWrapper, SesWrapper
from ....layers.common import api_responses, dynamo_client
from ....layers.entities.notification.general_notification import Notification

def create_notification(event, context):
    # Get the JSON data from the request
    print(event)
    if 'body' in event:
        message = json.loads(event["body"])
    else:
        message = event
    print(message)
    # Create a class notification to check if is sms or email
    notification = Notification(message["user_id"], message["noti_data"])
    if 'phone_numbers' in notification.noti_data and notification.noti_data['status'] == "immediately":
        send_text_message(notification)
    if 'phone_numbers' in notification.noti_data and notification.noti_data['status'] == "schedule":
        schedule_text_message(notification)
    if 'email' in notification.noti_data:
        send_email(notification)
    try:
        dynamo_client.put_item(notification.to_json())
    except Exception as e:
        print(e)
    # Return the notification data
    return api_responses.success_response(notification.to_json())


def send_text_message(notification: Notification):
    notification_sns_wrapper = SnsWrapper(boto3.resource('sns'))
    for phone_number in notification.noti_data['phone_numbers']:
        notification_sns_wrapper.publish_text_message(
        notification.noti_data['location_code'] + str(phone_number),
        notification.noti_data['message'])


def schedule_text_message(notification: Notification):
    notification.noti_data['status'] = 'immediately'
    eventclient = boto3.client('events')
    name = 'cron_notification-' + str(int(time.time() * 1000.0))
    response = eventclient.put_rule(
        Name=name,
        ScheduleExpression=notification.noti_data['cron'],
        State='ENABLED',
        Description='cron lambda start'
    )
    response_target = eventclient.put_targets(
        Rule=name,
        Targets=[
            {
                'Id': 'StartInstance',
                'Arn': os.environ['LAMBDA_NOTIFICATION_ARN'],
                'Input': json.dumps(notification.__dict__)
            }
        ]
    )
    print(response_target)


def send_email(notification: Notification):
    notification_ses_wrapper = SesWrapper(boto3.client('ses'))
    notification_ses_wrapper.send_email(notification.noti_data['source'], notification.noti_data['destination'],
                                        notification.noti_data['message'], notification.noti_data['subject'])

