from datetime import datetime
import logging
import os

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import boto3
from botocore.exceptions import ClientError

TTL_TIME_SECONDS = 60 * 60 * 24 * 5

app = FastAPI()
logger = logging.getLogger()

endpoint_url = os.getenv('DYNAMODB_ENDPOINT_URL', None)
dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)


class Command(BaseModel):
    command: str
    data: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/commands")
def store_command(command: Command,
                  authorization: str | None = Header(default=None)) -> Command:
    logger.info(
        f"Storing command: {command.command} with data: {command.data}"
    )
    ddb_table = dynamodb.Table('voice-hue-commands')
    try:
        timestamp = int(datetime.now().timestamp())
        client_id = get_client_id(authorization)
        ddb_table.put_item(
            Item={
                'pk': client_id,
                'sk': f"command#{timestamp}",
                'command': command.command,
                'data': command.data,
                'timestamp': timestamp,
                'expires_at': timestamp + TTL_TIME_SECONDS,
            }
        )
        return command
    except Exception as e:
        logger.error(f"Error storing command: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def get_client_id(api_key: str) -> str:
    table = dynamodb.Table('voice-hue-api-keys')
    try:
        response = table.get_item(Key={'api_key': api_key})

        if 'Item' in response:
            client_id = response['Item']['client_id']
            return client_id
        else:
            raise Exception('Could not find client id')

    except ClientError as e:
        raise Exception(f'Error getting client id: {e}')
