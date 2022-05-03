import json
import boto3
import logging
from .custome_encoder import CustomeEncoder


#setting logger
logger=logging.getLogger()
logger.setLevel(logging.INFO)

#setting dynamodb table
dynamodbTableName= 'Books'
dynamodb= boto3.resource('dynamodb')
table= dynamodb.Table(dynamodbTableName)

#http methods
getMethod='GET'
postMethod='POST'
putMethod='PUT'
deleteMethod='DELETE'

#paths
healthPath='/health'
book='/book'
books='/books'

def lambda_handler(event, context):
   logger.info(event)
   httpMethod=event['httpMethod']
   path=event['path']
   if httpMethod==getMethod and path==healthPath:
       response=buildResponse(200)
   elif httpMethod==getMethod and path==book:
        response=getBook(event['queryStringParameters']['bookId'])
   elif httpMethod==getMethod and path==books:
        response=getBooks()
   elif httpMethod==postMethod and path==books:
        response=createBook(event['body'])
   elif httpMethod==putMethod and path==books:
        response=updateBook(event['body'],event['queryStringParameters']['bookId'])
   elif httpMethod==deleteMethod and path==book:
        response=removeBook(event['queryStringParameters']['bookId'])
   else :
       response=buildResponse(404,'Not found')
   return response

def getBook(bookId):
    try:
        response=table.get_item(
            Key={
                'bookid':bookId
            }
        )
        if 'Item' in response:
            return buildResponse(200,response['Item'])
        else:
            return buildResponse(404,{'Message':'bookid: %s not found' %bookId})
    except:
        logger.exception('error occured while getting book')


def getBooks():
    try:
        response=table.scan()
        result=response['Items']
        while 'LastEvaluatedKey' in response:
            response=table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            result.extend(response['Items'])

        body={
            'books':result
        }
        return buildResponse(200,body)

    except:
        logger.exception('error occured while getting books')


def createBook(requestBody):
    try:
        table.put_item(Item=requestBody)
        body={
            'operation': 'SAVE',
            'Message':'SUCCESS',
            'Item':requestBody
        }
        return buildResponse(201,body)
    except:
        logger.exception('error occured while saving book')


def updateBook(requestBody,bookId):
    #book_name
    try:
        response=table.update_item(
        Key={
            'bookid':bookId
            },
            UpdateExpression="set book_name=:bookName",
            ExpressionAttributeValues={
                ':bookName': requestBody['book_name']
            },
        ReturnValues='UPDATED_NEW'
        )
        body={
            'operation': 'UPDATE',
            'Message':'SUCCESS',
            'Item':response
        }
        return buildResponse(200,body)
    except:
         logger.exception('error occured while updating book')

def removeBook(bookId):
    try:
        response=table.delete_item(
            Key={
                'bookid':bookId
            },
            ReturnValues='ALL_OLD'
        )
        body={
            'operation': 'DELETE',
            'Message':'SUCCESS',
            'Item':response
        }
        return buildResponse(200,body)
    except:
        logger.exception('error occured while deleting book')



def buildResponse(status,body=None):
    response={
        'statusCode':status,
        'headers':{
            'Content-Type':'application/json',
            'Access-Control-Allow-Origin':'*'
        }
    }
    if body is not None:
        response['body']= json.dumps(body,cls=CustomeEncoder)

    return response