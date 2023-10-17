import boto3
import pandas as pd

Access_key_ID = "AKIA6KJG2ZM3NM2YWJCK"
Secret_access_key = "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"
region_name = "ap-northeast-2"
bucket_name = "scvfile"
prefix = "backup_product_list"

s3 = boto3.client('s3', aws_access_key_id=Access_key_ID, aws_secret_access_key=Secret_access_key, region_name=region_name)

obj_list = s3.list_objects(Bucket=bucket_name, Prefix=prefix)

try:
    response = s3.get_object(Bucket=bucket_name, Key="backup_product_list/modified_products_list_2023-10-13.csv")
    file_content = response['Body'].read()

    decoded_content = file_content.decode('utf-8')

    # Save the decoded content to a CSV file
    with open('data_from_s3/20231013.csv', 'w', encoding='utf-8') as csv_file:
        csv_file.write(decoded_content)

    print("Data saved to '20231013.csv'")

except Exception as e:
    print(f"Error: {str(e)}")