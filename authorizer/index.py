import os
import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.getenv('API_KEYS_TABLE'))

def handler(event, context):
    headers = event['headers']
    api_key = headers.get('authorization')

    if not api_key:
        raise Exception('Unauthorized')

    try:
        response = table.get_item(Key={'api_key': api_key})

        if 'Item' in response:
            client_id = response['Item']['client_id']
            return generatePolicy(client_id, 'Allow', event['routeArn'])
        else:
            raise Exception('Unauthorized')

    except ClientError as e:
        print(f"Error checking API key: {e}")
        raise Exception('Internal Server Error')


def generatePolicy(principalId, effect, resource):
    authResponse = {}
    authResponse['principalId'] = principalId
    if (effect and resource):
        policyDocument = {}
        policyDocument['Version'] = '2012-10-17'
        policyDocument['Statement'] = []
        statementOne = {}
        statementOne['Action'] = 'execute-api:Invoke'
        statementOne['Effect'] = effect
        statementOne['Resource'] = resource
        policyDocument['Statement'] = [statementOne]
        authResponse['policyDocument'] = policyDocument

    authResponse['context'] = {
        "clientId": principalId
    }

    return authResponse
