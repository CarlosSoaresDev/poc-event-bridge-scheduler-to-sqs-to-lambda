import json
import requests
import logging

from sqs_service import SqsService

API_URI = 'https://random-data-api.com/api/v2/banks'


def lambda_handler(event, context):
    try:
        process_message(event=event)
    except Exception as ex:
        logging.error(str(ex))


def process_message(event):
    for record in event['Records']:
        body = json.loads(record["body"])
        session = body["StartSession"]
        logging.info(f'Iniciando a Sessão: {session}')

        try:
            response = requests.get(API_URI)
            if response.ok == False:
                raise Exception("Response API failed")

            response_dict = json.loads(response.text)
            value = float(response_dict['routing_number'])

            if session == 'schedule-by-minute':
                set_value_database(f'{session} - value: {value}', "table_consult_1")
            else:
                set_value_database(f'{session} - value: {value}', "table_consult_1")
        except Exception as ex:
            logging.error(str(ex))
            occurence(record)


def occurence(record):
    sqsService = SqsService
    sqsService.send_messager_to_occurence(message_body=record['body'])
    sqsService.delete_current_messager(receipt_handle=record['receiptHandle'])


def set_value_database(value, table):
    logging.info(f'Table: {table} - Value: {value}')
