### Lambda function

This function gets a file from AWS S3 and process the transactions

You need to have installed `git`, `aws-cli`, `ssh`.

#### Basic commands for running project locally
  * `git clone git@github.com:lirask8/process-s3-file-lambda.git` Clone the project.
  * `cd process-s3-file-lambda`
  * `python3 -m venv .venv` create a virtualenv.
  * `source .venv/bin/activate` activate virtualenv.
  * `pip install -r requirements.txt` install requirements
  * `python lambda_function.py` run the function


##### This code was deployed and tested in AWS
![lambda](https://public-images-ols3.s3.us-east-2.amazonaws.com/aws_lambda.png)