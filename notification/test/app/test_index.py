from unittest import TestCase
from unittest.mock import patch, MagicMock

from app.index import createNotification



class TestIndex(TestCase):




    """happy path"""
    @patch("app.index.create_notification")
    def test_create_notification(self, mock: MagicMock):
        event = {
            'body': '{\"user_id\":\"123456\", \"noti_data\": { \"location_code\": \"+57\", \"timezone\":\"GMT+5\", \"phone_numbers\":[3505784483], \"message\":\"PAGAME\",\"status\":\"immediately\"}}',
            'headers': {'Content-Type': 'application/json', 'Content-Length': '153', 'Host': 'localhost:3000',
                        'Connection': 'Keep-Alive', 'User-Agent': 'Apache-HttpClient/4.5.13 (Java/11.0.15)',
                        'Accept-Encoding': 'gzip,deflate'}, 'httpMethod': 'POST', 'isBase64Encoded': False,
            'multiValueHeaders': {'Content-Type': ['application/json'], 'Content-Length': ['153'],
                                  'Host': ['localhost:3000'], 'Connection': ['Keep-Alive'],
                                  'User-Agent': ['Apache-HttpClient/4.5.13 (Java/11.0.15)'],
                                  'Accept-Encoding': ['gzip,deflate']}, 'multiValueQueryStringParameters': None,
            'path': '/create', 'pathParameters': None, 'queryStringParameters': None,
            'requestContext': {'accountId': 'offlineContext_accountId', 'apiId': 'offlineContext_apiId',
                               'authorizer': {'principalId': 'offlineContext_authorizer_principalId'},
                               'domainName': 'offlineContext_domainName', 'domainPrefix': 'offlineContext_domainPrefix',
                               'extendedRequestId': 'cl659m5ag0000hwn5d5hr8qpf', 'httpMethod': 'POST',
                               'identity': {'accessKey': None, 'accountId': 'offlineContext_accountId',
                                            'apiKey': 'offlineContext_apiKey', 'apiKeyId': 'offlineContext_apiKeyId',
                                            'caller': 'offlineContext_caller',
                                            'cognitoAuthenticationProvider': 'offlineContext_cognitoAuthenticationProvider',
                                            'cognitoAuthenticationType': 'offlineContext_cognitoAuthenticationType',
                                            'cognitoIdentityId': 'offlineContext_cognitoIdentityId',
                                            'cognitoIdentityPoolId': 'offlineContext_cognitoIdentityPoolId',
                                            'principalOrgId': None, 'sourceIp': '127.0.0.1',
                                            'user': 'offlineContext_user',
                                            'userAgent': 'Apache-HttpClient/4.5.13 (Java/11.0.15)',
                                            'userArn': 'offlineContext_userArn'}, 'path': '/create',
                               'protocol': 'HTTP/1.1',
                               'requestId': 'cl659m5ah0001hwn59mwt0bdh', 'requestTime': '28/Jul/2022:11:43:40 -0500',
                               'requestTimeEpoch': 1659026620732, 'resourceId': 'offlineContext_resourceId',
                               'resourcePath': '/dev/create', 'stage': 'dev'}, 'resource': '/create'}
        expected = {'PK': 'USER#123456', 'SK': 'FORM#OFBiopLMhD', 'user_id': '123456',
                    'noti_data': {'location_code': '+57', 'timezone': 'GMT+5', 'phone_numbers': [3505784483],
                                  'message': 'PAGAME', 'status': 'immediately'}, 'created_at': '07/28/2022, 11:45:28',
                    'updated_at': '07/28/2022, 11:45:28'}
        mock.return_value = expected
        result = createNotification(event, None)
        self.assertEqual(result, expected)
