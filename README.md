# NewsContentSQS

Hello!

This repo will allow a user to input a search term and optional "date from" into either the Lambda console page or AWS Cli, and quickly retrieve relevant articles via The Guardian API.

This project assumes the user already has an AWS account and has configured their CLI with the command "aws configure"

You must also obtain an API key from the link below, and store this key in an AWS Secret. 

https://open-platform.theguardian.com/access/

Please name the key "guardian_key"

Please open a new terminal and ensure you are in a fresh Venv.

Please set the Pythonpath to the root directory.

At this point you can Terraform init, Terraform plan and Terraform apply.

At this point you can run the following command...

$ aws lambda invoke --function-name searchBrokerFunction --payload '{"target_queue": "hello-world", "search_term": "machine learning"}' response.json --cli-binary-format raw-in-base64-out

This should create a json file with the content "{"statusCode": 200, "message": "Message sent successfully!", "target_queue": "hello-world"}".

You can also open the AWS Console, go to the SQS Queues and verify the prescence of a newly created queue with at least one message!

You can replace "hello-world" to specify or create a new queue, and you can adjust the "search_term" to whatever you find interesting. You can also add "date_from" to ensure you only obtain articles after a certain date.

IMPORTANT - if using the additonal "date_from" please input dates in the following format.

$ aws lambda invoke --function-name searchBrokerFunction --payload '{"target_queue": "hello-world", "search_term": "machine learning", "date_from": 01012025}' response.json --cli-binary-format raw-in-base64-out

The above will return articles from after the first day of the year 2025.

Please do not input 01/01/2025 or any other variation. 