from flask import Flask, request
import boto3
APP = Flask(__name__)
CLIENT = boto3.client(
    "sns",
    aws_access_key_id="AKIAY5PDDSHSYXHR5FKK",
    aws_secret_access_key="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",
    region_name="ap-northeast-2"
)
@APP.route('/sendsms', methods=['POST'])
def sendsms():
    numbers = ["8201030056900"]
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
