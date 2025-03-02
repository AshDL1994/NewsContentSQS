import requests
import boto3
import json
from utils.key import the_key
from utils.term_search import article_search
from utils.send_messages import list_all_queues, send_message_to_queue, create_queue_return_url


client = boto3.client('sqs')

def search_to_broker(target_queue, search_term, date_from=None):

    message = article_search(search_term, date_from)
    message_body = json.dumps(message, indent=4, ensure_ascii=False)
    # list of queues 
    queue_list = list_all_queues()
    
    #if name is list then get url and send message
    if target_queue in queue_list:
        queue_url = client.get_queue_url(QueueName=target_queue)['QueueUrl']
        send_message_to_queue(queue_url, message_body)

    #if name is not in list then create new queue then send message
    else:
        new_queue_url = create_queue_return_url(target_queue)
        send_message_to_queue(new_queue_url, message_body)
        





