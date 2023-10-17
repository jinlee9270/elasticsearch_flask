import boto3
import pandas as pd
from datetime import datetime

Access_key_ID = "AKIA6KJG2ZM3NM2YWJCK"
Secret_access_key = "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"
region_name = "ap-northeast-2"
bucket_name = "scvfile"
prefix = "backup_product_list"

s3 = boto3.client('s3', aws_access_key_id=Access_key_ID, aws_secret_access_key=Secret_access_key, region_name=region_name)
obj_list = s3.list_objects(Bucket=bucket_name, Prefix=prefix)
s3_format_current_date = datetime.now().strftime('%Y-%m-%d')
print(s3_format_current_date)
# csv_filename = f"backup_product_list/modified_products_list_{s3_format_current_date}.csv"
csv_filename = "backup_product_list/modified_products_list_2023-10-15.csv"
current_date = datetime.now().strftime('%Y%m%d')

try:
    response = s3.get_object(Bucket=bucket_name, Key=csv_filename)
    print(response)
    file_content = response['Body'].read()

    decoded_content = file_content.decode('utf-8')

    # Save the decoded content to a CSV file
    with open(f'data_from_s3/{current_date}.csv', 'w', encoding='utf-8') as csv_file:
        csv_file.write(decoded_content)

    print(f"Data saved to '{current_date}.csv'")

except Exception as e:
    print(f"Error: {str(e)}")