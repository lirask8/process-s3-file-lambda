import boto3
from botocore.exceptions import ClientError

from process_file import ProcessFile

s3_client = boto3.client("s3")
S3_BUCKET_NAME = 'public-images-ols3'
SENDER = "Sender Name <lira.sk8.182@gmail.com>"
AWS_REGION = "us-east-2"
SUBJECT = "Stori transactions summary"
BODY_TEXT = ("Summary transactions")
RECIPIENT = "lira.sk8.182@gmail.com"
CHARSET = "UTF-8"


def lambda_handler(event, context):
    object_key = "transactions.csv"
    file_content = s3_client.get_object(
        Bucket=S3_BUCKET_NAME, Key=object_key)['Body'].read().split(b'\n')

    file_processor = ProcessFile(file_content)
    file_processor.process_rows()
    summary = file_processor.get_summary_data()

    print(summary)

    send_email_ses(summary)

    return {
        'statusCode': 200,
        'body': summary,
    }


def send_email_ses(summary: dict):
    BODY_HTML = f"<html><head></head><body><h1>Summary Transactions</h1>" \
                f"<p>Balance: {summary['balance']}</p>" \
                f"<p>Debit Avg: {summary['debit_avg']}</p>" \
                f"<p>Credit Avg: {summary['credit_avg']}</p>" \
                f"</body></html>"

    client = boto3.client('ses', region_name=AWS_REGION)

    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    except ClientError as e:
        print("Error>>>>>>>>>>>>>>>")
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

# RUN FUNCTION
lambda_handler("event", {})
