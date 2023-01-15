import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os


load_dotenv()
AWS_MAIL = os.getenv('AWS_MAIL')


def send_email_alert(reader_mac: str, name:str, card_id: str, date: str):
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    sender = f"Access Dashboard <{AWS_MAIL}>"

    # Replace recipient@example.com with a "To" address. If your account
    # is still in the sandbox, this address must be verified.
    recipient = f"{AWS_MAIL}"


    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    aws_region = "eu-central-1"

    # The subject line for the email.
    subject = "Unauthorized access"


    # The HTML body of the email.
    location = f"{name} ({reader_mac})"

    body_html = """<html>
    <head></head>
    <body>
      <h1>Unauthorized access</h1>
      <p>Reader: %s </p>
      <p>Card ID: %s </p>
      <p>Date: %s </p>
    </body>
    </html>
                """ % (location, card_id, date)

    # The character encoding for the email.
    charset = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses', region_name=aws_region)

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    recipient,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': charset,
                        'Data': body_html,
                    }
                },
                'Subject': {
                    'Charset': charset,
                    'Data': subject,
                },
            },
            Source=sender,
        )

    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
