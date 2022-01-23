# AWS (Amazon web service)

## Boto3
You use the AWS SDK for Python (Boto3) to create, configure, and manage AWS services, such as Amazon Elastic Compute Cloud (Amazon EC2) and Amazon Simple Storage Service (Amazon S3). The SDK provides an object-oriented API as well as low-level access to AWS services.

The SDK is composed of two key Python packages: 
* <b>Botocore</b> (the library providing the low-level functionality shared between the Python SDK and the AWS CLI) and 
* <b>Boto3</b> (the package implementing the Python SDK itself).
<br><br>

Boto3 adheres to the following lookup order when searching through sources for [configuration values](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#using-the-config-object):

* A `Config` object that's created and passed as the config parameter when creating a client
* Environment variables
* The ~/.aws/config file
<br/><br/>

### Pre-requisite:
* Follow [LinkedIn Learning](https://www.linkedin.com/learning/aws-essential-training-for-architects/s3-and-glacier) to setup your AWS environment
* Configure using `Config` object or environment values
* Set AWS_GATEWAY_BASE_URL environment variable
