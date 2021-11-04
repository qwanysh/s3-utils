import argparse
import os

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

s3_client = boto3.client(
    service_name='s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'action', type=action,
        help=f"action({', '.join(actions)}) to perform",
    )
    parser.add_argument('file_name', type=file_name, help='file to upload')
    parser.add_argument(
        '-k', '--key',
        help='S3 key to upload. If not specified then file_name is used',
    )
    return parser.parse_args()


def upload(args):
    try:
        s3_client.upload_file(
            args.file_name, os.getenv('AWS_BUCKET'),
            args.key or args.file_name,
        )
    except ClientError as e:
        print(e)


actions = {'upload': upload}


def action(value):
    if value in actions:
        return value
    raise argparse.ArgumentTypeError(
        f"use one of ({', '.join(actions)})",
    )


def file_name(value):
    if os.path.isfile(value):
        return value
    raise argparse.ArgumentTypeError(f'"{value}" file does not exist')


def main():
    args = get_args()
    actions[args.action](args)


if __name__ == '__main__':
    main()