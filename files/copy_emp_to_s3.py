import boto3
import pandas as pd
import re



s3_resource = boto3.resource('s3')
first_bucket_name = 'moovit-general'
first_file_name =  'employees.xlsx'
my_bucket = s3_resource.Bucket(first_bucket_name)
dest_bucket = 'erez-shindelman-filtered-images'

def get_emp_names(s3_resource, first_bucket_name, first_file_name):
    s3_resource.Object(first_bucket_name, first_file_name).download_file(f'{first_file_name}')
    df = pd.read_excel(f'{first_file_name}')
    emp_lst = df['Name'].values.tolist()
    #print(emp_lst)
    return emp_lst

empfromxl = get_emp_names(s3_resource, first_bucket_name, first_file_name) # return employees names from employees.xlsx in moovit-general s3 bucket
def convert_emp_to_lower(empfromxl):
    empfromxl_lower = [ re.sub(' ', '',name).lower() for name in empfromxl ] # convert name to lower case and remove spaces
    return empfromxl_lower

emp_lower_list = convert_emp_to_lower(empfromxl)
print(emp_lower_list)

def normelizing_names(file_name):
    #file_name_striped = file_name.strip('.png')
    file_name_striped = re.sub('[^A-Za-z]', '', file_name)
    return file_name_striped.lower()


def get_s3_emp_list():
    emp_l = []
    for file in my_bucket.objects.all():
        if str(file.key).endswith('.png'):
            file_name = normelizing_names(file.key)
            if file_name not in emp_l:
                emp_l.append(file_name)
    return emp_l

def get_s3_emp_list_filtered(emp_lower_list, source_bucket, dest_bucket):
    for name in emp_lower_list:
        print(f" looking to match {name}")
        for file in my_bucket.objects.all():
            file_name = normelizing_names(file.key)
            if name in file_name:
                print(f"{name} found in s3 copping source {file.key} to bucket as {name}.png")
                #copy_source = {'Bucket': source_bucket, 'Key': file.key}
                #s3_resource.copy_object(CopySource = copy_source, Bucket = dest_bucket, Key = name)
                copy_source = { 'Bucket': source_bucket, 'Key': file.key }
                bucket = s3_resource.Bucket(dest_bucket)
                bucket.copy(copy_source, name + '.png')

get_s3_emp_list_filtered(emp_lower_list, first_bucket_name, dest_bucket)
