# MuZakkir Saifi
# import logging for get the logs in  execution
import logging
# import the boto3 which will use to interact  with the aws
import boto3
from botocore.exceptions import ClientError
import json

REGION = input("Please enter the REGION: ")

# this is the configration for the logger_for

logger_for = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

response = boto3.client("ec2", region_name=REGION)


def describe(tag, tag_values, maximum_items):
    try:
        pag = response.get_paginator('describe_subnets')

        res_iterator = pag.paginate(
            Filters=[{
                'Name': f'tag:{tag}',
                'Values': tag_values
            }],
            PaginationConfig={'MaxItems': maximum_items})

        full_result = res_iterator.build_full_result()

        list = []

        for page in full_result['Subnets']:
            list.append(page)

    except ClientError:
        logger_for.exception('It can not describe subnets.')
        raise
    else:
        return list


if __name__ == '__main__':
    TAG = input("Enter the tag name: ")
    TAG_VAL=['custom-subnet'] # enter he tag value 
    MAXIMUM_ITEMS = int(input("Enter the limit of items: "))
    sub = describe(TAG, TAG_VAL, MAXIMUM_ITEMS)
    logger_for.info('Subnet Details: ')
    for subnet in sub:
        logger_for.info(json.dumps(subnet, indent=4) + '\n')