import json
import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('LogisticsOffers')


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super().default(o)


def lambda_handler(event, context):
    if 'body' in event and event['body']:
        params = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
    elif event.get('queryStringParameters'):
        params = event['queryStringParameters']
    else:
        params = event

    origin = params.get('origin')
    destination = params.get('destination')
    max_rate = params.get('max_rate')

    try:
        if origin:
            response = table.query(
                IndexName='OriginIndex',
                KeyConditionExpression=Key('origin').eq(origin),
            )
        else:
            response = table.scan()

        items = response.get('Items', [])

        if destination:
            items = [i for i in items if i.get('destination', '').lower() == destination.lower()]
        if max_rate:
            items = [i for i in items if float(i.get('rate_usd', 0)) <= float(max_rate)]

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'count': len(items), 'offers': items}, cls=DecimalEncoder),
        }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}
