# SREFetchChallenge
 
 Hello There,
 below you will find directions on how to prepare your environment as well as install the correct packages needed to run this program that will create an EC2 instance in Amazon Web Services (AWS). I will break each down into steps then at the end we will have you run the program and ssh into the linux machine with one of the user accounts. Also, this project will allow you to make configuration changes based on the YAML file in this repo. All you will have to do is change the yaml file and run the program after the environment has been setup correctly.
 
 ## Step One - Download Python (Skip if this is already done)
 
 Please head over to https://www.python.org/downloads/ and download the latest version of python (as of writing this, it is Python 3.9.5). Go through the setup selecting Install Now as well as checking off the box "Add Python to Path" at the bottom of the setup window. If you want to make sure that it installed correctly you can follow the steps below:
 ### Windows
 
 1. Hit the windows button on your keyboard and type in "cmd" and hit enter.
 2. Type in "python" and you should see something similar to this output: Python 3.7.4 (tags/v3.7.4:e09359112e, Jul  8 2019, 19:29:22) [MSC v.1916 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license" for more information.
 3. If this is the ouput that you get then type in "exit()" to exit python.

### MacOS

 1. Press Command + spacebar to open spotlight search and type in "Terminal" and select Terminal.
 2. type in "python" into the terminal and hit enter. You should see similar output to the windows example.
 3. If this is the ouput that you get then type in "exit()" to exit python.

## Step Two - Pip Install all dependencies (Skip if this is already done)

In either your Windows Command Line or MacOS Terminal type in the following commands:
 1. pip install boto3
 2. pip install pyyaml
 3. pip install paramiko

## Step Three - Setup AWS CLI & Credential Settings (Skip if this is already done)

Ensure that you already have an AWS account setup. If you need to setup an AWS account go to this [link](https://portal.aws.amazon.com/billing/signup#/start)

For detailed instruction on installing AWS CLI go to this [page](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) and select your Operating System that you are currently using. The next page will have indepth installating information.

After CLI is downloaded create a new user through the IAM portal and follow these [instructions](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console)

After you create a user and gather the Access Key ID and the Secret Access Key, go to your terminal and type in "aws configure". This will prompt for 4 inputs (one at a time):
 1. AWS Access Key ID [None]: --YOUR ACCESS KEY ID--
 2. AWS Secret Access Key [None]: --YOUR SECRET ACCESS KEY--
 3. Default region name [None]: [Choose your region code](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html)
 4. Default output format [None]: json

After this is set then your CLI environment should be successfully setup.

## Step Four - Download the project

