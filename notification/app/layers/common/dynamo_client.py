import os
import boto3

main_table = os.environ['DYNAMODB_TABLE']

dynamodb = boto3.resource('dynamodb')

def put_item(item):
    table = dynamodb.Table(main_table)
    table.put_item(Item=item)

def delete_item(key):
    table = dynamodb.Table(main_table)
    table.delete_item(Key=key)

def get_item(key):
    table = dynamodb.Table(main_table)
    response = table.get_item(Key=key)
    return response['Item']

def update_single_item(key, value):
    table = dynamodb.Table(main_table)
    table.update_item(Key=key, UpdateExpression="set #v = :val", ExpressionAttributeValues={':val': value}, ExpressionAttributeNames={'#v': 'value'})

def batch_write(items):
    table = dynamodb.Table(main_table)
    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)