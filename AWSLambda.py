import boto3
import json
import urllib3
import re
import urllib.request

def lambda_handler(event, context):
    # TODO implement
    client = boto3.client('s3', 'eu-west-2')
    ec2 = boto3.client('ec2', 'eu-west-2')
    
### Get Download link and JSON filename from URL ###
    url = 'https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519'
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent': user_agent, }
    request = urllib.request.Request(url, None, headers)
    page = urllib.request.urlopen(request)
    html = page.read().decode("utf-8")
    # Aplying Filter [Get only urls]
    lista = []
    lista = re.findall(r'(https?://\S+)', html)
    # Aplying Filter [Get only urls .json]
    matching = [s for s in lista if ".json" in s]
    url=matching[1][:-1]
    # Getting filename
    filename = url.split("/")[len(url.split("/")) - 1]
### Get Download link and JSON filename from URL ###
    

    
### DOWNLOAD json to S3 ###
    bucket = 'bucket-directory' #your s3 bucket
    key = 'azuredevops/' + str(filename) #your desired s3 path or filename
    
    http=urllib3.PoolManager()
    client.upload_fileobj(http.request('GET', url,preload_content=False), bucket, key)
### DOWNLOAD json to S3 ###

    
### GET IP from json ###
    response = client.get_object(Bucket='bucket-directory', Key='azuredevops/'+str(filename),)
    res = response["Body"].read().decode()
    json_content = json.loads(res)
    
    for values in json_content["values"]:
      if (values["name"] == 'AzureDevOps.WestEurope'):    
        azure_ips = values['properties']['addressPrefixes']
### GET IP from json ###



### ADD Azure IP to Security Group GreenAfrica ###
    groupid = 'sg-hash'
    for ips in azure_ips:
      #check if IP is already added to sg  
      response = ec2.describe_security_groups(Filters=[{'Name':'ip-permission.cidr', 'Values':[ips,],},], GroupIds=[groupid,],)
      if not (response['SecurityGroups']):
        ec2.authorize_security_group_ingress(GroupId=groupid, IpPermissions=[{'FromPort':443, 'IpProtocol':'tcp', 'IpRanges':[{'CidrIp':ips, 'Description':'Azure Devops IP'},], 'ToPort':443,}])
### ADD Azure IP to Security Group GreenAfrica ###


### ADD Azure IP to Security Group Jambojet ###
    groupid = 'sg-05e17e0fb83adce6c'
    for ips in azure_ips:
      #check if IP is already added to sg  
      response = ec2.describe_security_groups(Filters=[{'Name':'ip-permission.cidr', 'Values':[ips,],},], GroupIds=[groupid,],)
      if not (response['SecurityGroups']):
        ec2.authorize_security_group_ingress(GroupId=groupid, IpPermissions=[{'FromPort':443, 'IpProtocol':'tcp', 'IpRanges':[{'CidrIp':ips, 'Description':'Azure Devops IP'},], 'ToPort':443,}])
### ADD Azure IP to Security Group Jambojet ###

    return {
        'statusCode': 200,
        'body': json.dumps('The AzureDevOps-WestEurope IP is:' + str(azure_ips))
    }
