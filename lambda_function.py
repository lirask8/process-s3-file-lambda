import boto3

from process_file import ProcessFile

s3_client = boto3.client("s3")
S3_BUCKET_NAME = 'public-images-ols3'


def lambda_handler(event, context):
    object_key = "transactions.csv"
    file_content = s3_client.get_object(
        Bucket=S3_BUCKET_NAME, Key=object_key)['Body'].read().split(b'\n')

    file_processor = ProcessFile(file_content)
    file_processor.process_rows()
    summary = file_processor.get_summary_data()

    print(summary)
    # send email SES

    return {
        'statusCode': 200,
        'body': summary,
    }

# RUN FUNCTION
lambda_handler("event", {})
