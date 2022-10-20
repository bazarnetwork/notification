import logging

from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class SnsWrapper:

    def __init__(self, sns_resource):

        self.sns_resource = sns_resource

    def publish_text_message(self, phone_number, message):
        """
        Publishes a text message directly to a phone number without need for a
        subscription.
        :param phone_number: The phone number that receives the message. This must be
                             in E.164 format. For example, a United States phone
                             number might be +12065550101.
        :param message: The message to send.
        :return: The ID of the message.
        """
        try:
            response = self.sns_resource.meta.client.publish(
                PhoneNumber=phone_number, Message=message)
            message_id = response['MessageId']
            logger.info("Published message to %s.", phone_number)
        except ClientError:
            logger.exception("Couldn't publish message to %s.", phone_number)
            raise
        else:
            return message_id


class SesWrapper:

    def __init__(self, ses_resource):
        self.ses_resource =  ses_resource


    def send_email(self, source, destination, message, subject):
        """send Email from ses"""
        self.ses_resource.send_email(
            Source= source,
            Destination = {
                'ToAddresses': destination,
            },


            Message= {
                'Subject': subject,
                'Body': message
            })
