import time
import paramiko
import boto3
import yaml
from botocore.exceptions import ClientError
# Script that runs on startup to create the users, sets up RSA key, and moves the information to authorized_keys
script = '''#!/bin/sh
sudo mkfs.{0} {1}
sudo mkdir {2}
sudo mount -o defaults {1} {2}
# adding users
sudo adduser {3}
sudo adduser {4}
# creating rsa key for user and setting security settings
sudo su - {3} -c ' mkdir .ssh ; chmod 700 .ssh ; touch .ssh/authorized_keys ; chmod 600 .ssh/authorized_keys ; ssh-keygen -q -N "" -f ~/.ssh/id_rsa ; cat .ssh/id_rsa ; cat .ssh/id_rsa.pub ; cat .ssh/id_rsa.pub >> .ssh/authorized_keys ;' exit
# creating rsa Key for user and setting security settings
sudo su - {4} -c ' mkdir .ssh ; chmod 700 .ssh ; touch .ssh/authorized_keys ; chmod 600 .ssh/authorized_keys ; ssh-keygen -q -N "" -f ~/.ssh/id_rsa ; cat .ssh/id_rsa ; cat .ssh/id_rsa.pub ; cat .ssh/id_rsa.pub >> .ssh/authorized_keys ;' exit
'''
# Brings in the Yaml Configuration
config={}
print("Importing Yaml File...\n")
with open('testConfig.yml') as f:
    # use safe_load instead load
    config = yaml.safe_load(f)
print("Imported Yaml File.\n")

#adds in any configuration needs to the startup script at the top
script = script.format(config['server']['volumes'][1]['type'], config['server']['volumes'][1]['device'], config['server']['volumes'][1]['mount'], config['server']['users'][0]['login'], config['server']['users'][1]['login'])
# Determines if it is Arm or x86_64 and sets the imageType
imageType = ""
if "arm" in config['server']['architecture']:
    imageType = "ami-07a3e3eda401f8caa"
else:
    imageType = config['server']['ami_type']
print("Generating EC2 Key Pair...\n")

# creates keypair to associate with ec2-user
ec2 = boto3.resource('ec2')
outfile = open('ec2-keypair.pem', 'w')
key_pair = ec2.create_key_pair(KeyName='ec2-keypair')
KeyPairOut = str(key_pair.key_material)
outfile.write(KeyPairOut)
outfile.close()
print("Generated EC2 Key Pair.\n")

# Creates ec2 instance based on yaml file inputs
print("Creating EC2 Instance...")
client = boto3.client('ec2', region_name='us-east-2')

#creates a new security group
secGroupID = ""
response = client.describe_vpcs()
vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

try:
    response = client.create_security_group(GroupName='testGroup',
                                         Description='DESCRIPTION',
                                         VpcId=vpc_id)
    security_group_id = response['GroupId']
    secGroupID = response['GroupId']
    print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

    data = client.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 80,
             'ToPort': 80,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 22,
             'ToPort': 22,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ])
    print('Ingress Successfully Set %s' % data)
except ClientError as e:
    print(e)

# Creates the Instance
response = client.run_instances(
    BlockDeviceMappings=[
        {
            'DeviceName': config['server']['volumes'][0]["device"],
            'Ebs': {
                'DeleteOnTermination': True,
                'VolumeSize': config['server']['volumes'][0]["size_gb"],
                'VolumeType': 'gp2'
            },
        },
        {
            'DeviceName': config['server']['volumes'][1]["device"],
            'Ebs': {
                'DeleteOnTermination': True,
                'VolumeSize': config['server']['volumes'][1]["size_gb"],
                'VolumeType': 'gp2'
            },

        }
    ],
    ImageId=imageType,
    InstanceType=config['server']['instance_type'],
    MaxCount=config['server']['max_count'],
    MinCount=config['server']['min_count'],
    KeyName='ec2-keypair',
    Monitoring={
        'Enabled': False
    },
    # sends script above to ec2 instance to run on startup, creating the users.
    UserData=script,
    SecurityGroupIds= [secGroupID]
)
print("EC2 Instance created. Sleeping for 100 seconds so instance can initialize. DO NOT EXIT...\n")
time.sleep(100)
print("EC2 Instance is up, grabbing private keys for user1 and user2...\n")
#code to get the public dns name
def getInstanceDns():
    ec2client = boto3.client('ec2')
    response = ec2client.describe_instances()
    activeInstance = ""
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            if instance["PublicDnsName"] != "":
                activeInstance = instance["PublicDnsName"]
                print("The address for the EC2 instance is: " + activeInstance)
    return activeInstance

#creates pem files for user 1 and user 2
def grabKeyFromEc2(yamlDict):
    config = yamlDict
    k = paramiko.RSAKey.from_private_key_file("ec2-keypair.pem")
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(hostname=getInstanceDns(), username="ec2-user", pkey=k)
    commands = ['''sudo su - user1 -c ' cat .ssh/id_rsa ;' exit''', '''sudo su - user1 -c ' cat .ssh/id_rsa.pub ;' exit''', '''sudo su - user2 -c ' cat .ssh/id_rsa ;' exit''', '''sudo su - user2 -c ' cat .ssh/id_rsa.pub ;' exit''']
    x = ""
    user1=[]
    user2=[]
    for command in commands:
        if "user1" in command:
            stdin, stdout, stderr = c.exec_command(command)
            user1.append(stdout.read().decode('utf-8').rstrip("\n"))
        else:
            stdin, stdout, stderr = c.exec_command(command)
            user2.append(stdout.read().decode('utf-8').rstrip("\n"))
    c.close()
    outfile = open('user1-keypair.pem', 'w')
    user1key = user1[0]
    outfile.write(user1key)
    outfile = open('user2-keypair.pem', 'w')
    user2key = user2[0]
    outfile.write(user2key)
    config['server']['users'][0]['ssh_key'] = user1[1]
    config['server']['users'][1]['ssh_key'] = user2[1]
    with open('testConfig.yml', 'w') as outfile:
        yaml.dump(config, outfile, default_flow_style=False)


grabKeyFromEc2(config)
print("RSA keys have been acquired. Please view github documentation for instructions on how to ssh into the ec2 instance.\n Thanks!\n")
