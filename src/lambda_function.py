import json
from src.main import search_to_broker

def lambda_handler(event, context):
    try:
        target_queue = event.get("target_queue")
        search_term = event.get("search_term")
        date_from = event.get("date_from", None)

        if not target_queue or not search_term:
            return {
                "statusCode": 400,
                "message": "Missing required parameters.",
                "input_received": event  # Show input for debugging
            }

        search_to_broker(target_queue, search_term, date_from)

        return {
            "statusCode": 200,
            "message": "Message sent successfully!",
            "target_queue": target_queue
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "error": str(e),
            "input_received": event
        }
