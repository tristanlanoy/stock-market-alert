import json
from yahooquery import Ticker
import boto3

#Connexion DynamoDB et SNS
dynamodb = boto3.client('dynamodb')
ddb_table = 'stock_db'
sns = boto3.client('sns')
sns_arn = 'arn:aws:sns:eu-west-2:136245050755:stock_topic'


def get_tickeryahoo(ticker_namee):
    d = dict();
    ticker_yahoodata = Ticker(ticker_namee).price
    d['price'] = ticker_yahoodata[ticker_namee]["regularMarketPrice"]
    d['shortname'] = ticker_yahoodata[ticker_namee]["shortName"]
    return d


def sns_notify(sns_message):
    response = sns.publish(
        TopicArn=sns_arn,   
        Message=sns_message,   
    )
    return response


def is_tickerdownpercentage(ticker_actualprice,ticker_baseprice,ticker_downpercentage):
    ticker_downlimit = ticker_baseprice*(1-(ticker_downpercentage/100))
    if ticker_actualprice <= ticker_downlimit:
        return True
    else:
        return False 


def get_tickerdb(ticker_name,alert_type):
    d = dict();
    ticker_row = dynamodb.get_item(TableName=ddb_table,Key={'ticker': {'S': ticker_name},'alert': {'S': alert_type}})
    d['baseprice'] = float(ticker_row['Item']['baseprice']['N'])
    d['down-percentage'] = float(ticker_row['Item']['down-percentage']['N'])
    return d


def update_tickerbaseprice(ticker_name,ticker_actualprice,alert_type):
    response = dynamodb.update_item(
        TableName= ddb_table,
        Key={
            'ticker': {'S': ticker_name},
            'alert': {'S': alert_type}
        },
        UpdateExpression="set baseprice = :p",
        ExpressionAttributeValues={
            ':p': {'N': str(ticker_actualprice)},
        },
        ReturnValues="UPDATED_NEW"
    )
    return response



def check_downpercentage(ticker_name):
    alert_type = "down-percentage"
    ticker_yahoodata = get_tickeryahoo(ticker_name)
    ticker_dbdata = get_tickerdb(ticker_name,alert_type)
    if is_tickerdownpercentage(ticker_yahoodata['price'],ticker_dbdata['baseprice'],ticker_dbdata['down-percentage']):
        msg = "Attention l'action "+ticker_yahoodata['shortname']+" a baisé de "+str(ticker_dbdata['down-percentage'])+"%. Son prix actuel est maintenant de "+str(ticker_yahoodata['price'])+"€ . Plus d'infos : stocks://?symbol="+ticker_name.upper()
        sns_notify(msg)
        update_tickerbaseprice(ticker_name,ticker_yahoodata['price'],alert_type)




def main_func():
    response = dynamodb.scan(TableName=ddb_table)
    data = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    for one_row in data:
        if (one_row['alert']['S']) == "down-percentage":
            check_downpercentage(one_row['ticker']['S'])








def lambda_handler(event, context):
    # TODO implement 
    #ticker_provided_name = event['ticker']
    main_func()
    
    return {
        'statusCode': 200,
        'body': json.dumps("Function executed")
    }






    
    
    


