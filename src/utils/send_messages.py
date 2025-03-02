import boto3
client = boto3.client('sqs')

def create_queue_return_url(name):
        try:
            aws_response = client.create_queue(
                QueueName=name,
                Attributes={
                "MessageRetentionPeriod": "259200" 
            }
            )
            
            queue_url = client.get_queue_url(
                QueueName=name,     
            )

            return queue_url["QueueUrl"] #double check this and its necessity 
        except Exception as e:
             print(f"An error has occured: {e}")
             raise e


def list_all_queues():
    try:
        queue_list_object = client.list_queues()["QueueUrls"]
        list_names_only = [title[title.rfind('/')+1:] for title in queue_list_object]
        return list_names_only
    except Exception as e:
        print(f"Error occurred: {e}")
        return "Something went wrong. Please check if you have queues available."
   
    
    

def send_message_to_queue(queue_url, message_body):
        try:
            aws_message = client.send_message(
                QueueUrl=queue_url,
                MessageBody=message_body
                )
            queue_name = queue_url[queue_url.rfind('/')+1:]
            return f"Message sent to the que named '{queue_name}'!"
        
        except client.exceptions.QueueDoesNotExist:
             return "The specified queue does not exist. Please check the queue URL."
        
        except Exception as e:
            print(f"An error occurred: {e}") 
            return "Failed to send message. Please check the queue and try again."
              
        

