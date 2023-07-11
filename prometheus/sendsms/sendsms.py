from flask import Flask, request
import boto3
APP = Flask(__name__)
CLIENT = boto3.client(
    "sns",
    aws_access_key_id="",
    aws_secret_access_key="",
    region_name=""
)
@APP.route('/sendsms', methods=['POST'])
def sendsms():
    numbers = ["82"]
    message = request.json["message"]
    print(message)
    for number in numbers:
        response = CLIENT.publish(
            PhoneNumber=number,
            Message=message,
            MessageAttributes={
                'AWS.SNS.SMS.SenderID':
                {
                    'DataType': 'String',
                    'StringValue': 'Grafana'
                }
            }
        )
    return response
    print("Message has been sent to" + number)
APP.run(host="0.0.0.0", port=5000)
