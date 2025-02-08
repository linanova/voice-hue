from datetime import datetime
import json
import logging
import os
from typing import Optional, List

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import boto3
from botocore.exceptions import ClientError

TTL_TIME_SECONDS = 60 * 60 * 24 * 5
DDB_COMMAND_TABLE_NAME = 'voice-hue-commands'
DDB_API_KEY_TABLE_NAME = 'voice-hue-api-keys'
PREFERENCE_PREFIX = 'preference#'
COMMAND_PREFIX = 'command#'

app = FastAPI()
logger = logging.getLogger()

endpoint_url = os.getenv('DYNAMODB_ENDPOINT_URL', None)
dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)


class DataModel(BaseModel):
    text: str
    data: List


@app.post("/commands")
def store_command(command: DataModel,
                  authorization: str | None = Header(default=None)) -> DataModel:
    logger.info(
        f"Storing command: {command.text} with data: {command.data}"
    )
    ddb_table = dynamodb.Table(DDB_COMMAND_TABLE_NAME)
    try:
        timestamp = int(datetime.now().timestamp())
        client_id = get_client_id(authorization)
        ddb_table.put_item(
            Item={
                'pk': client_id,
                'sk': f"{COMMAND_PREFIX}{timestamp}",
                'command': command.text,
                'data': json.dumps(command.data),
                'timestamp': timestamp,
                'expires_at': timestamp + TTL_TIME_SECONDS,
            }
        )
        return command
    except Exception as e:
        logger.error(f"Error storing command: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/preferences")
def store_preference(preference: DataModel,
                     authorization: str | None = Header(default=None)) -> DataModel:
    ddb_table = dynamodb.Table(DDB_COMMAND_TABLE_NAME)
    try:
        timestamp = int(datetime.now().timestamp())
        client_id = get_client_id(authorization)
        ddb_table.put_item(
            Item={
                'pk': client_id,
                'sk': f'{PREFERENCE_PREFIX}{timestamp}',
                'preference': preference.text,
                'data': json.dumps(preference.data),
                'timestamp': timestamp,
            },
        )
        return preference
    except ClientError as e:
        logger.error(f"Error storing preference: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/preferences")
def get_preference(name: str,
                   authorization: str | None = Header(default=None)) -> Optional[DataModel]:
    ddb_table = dynamodb.Table(DDB_COMMAND_TABLE_NAME)
    try:
        client_id = get_client_id(authorization)
        response = ddb_table.query(
            KeyConditionExpression='pk = :client_id and begins_with(sk, :preference_prefix)',
            FilterExpression="preference = :preference",
            ExpressionAttributeValues={
                ':client_id': client_id,
                ':preference_prefix': PREFERENCE_PREFIX,
                ':preference': name
            },
            ScanIndexForward=False,
            Limit=1
        )

        if 'Items' in response and len(response['Items']) > 0:
            return DataModel(text=response['Items'][0]['preference'],
                             data=json.loads(response['Items'][0]['data']))
        else:
            raise HTTPException(status_code=404, detail="Preference not found")
    except ClientError as e:
        logger.error(f"Error getting preferences: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def get_client_id(api_key: str) -> str:
    table = dynamodb.Table(DDB_API_KEY_TABLE_NAME)
    try:
        response = table.get_item(Key={'api_key': api_key})

        if 'Item' in response:
            client_id = response['Item']['client_id']
            return client_id
        else:
            raise Exception("Could not find client id")

    except ClientError as e:
        raise Exception(f"Error getting client id: {e}")
