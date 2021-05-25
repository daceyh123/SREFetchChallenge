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

Go to the front page of the [project](https://github.com/daceyh123/SREFetchChallenge) and click the "Code" button in the top right hand corner and click "Download ZIP" from the drop down. At this point a zip file will be downloaded and the file needs to be extracted. If you need any help extracting the folder please follow this [guide](https://www.softwaretestinghelp.com/how-to-open-a-zip-file/)

After the project is in an unzipped folder, we need to go to the directory via the Command Line for Windows or the Terminal for MacOS. Below is the easiest ways to get to the directory.

### Windows
![image](https://user-images.githubusercontent.com/36930977/119420588-d4878900-bcca-11eb-96ba-981e36fa1569.png)
Click where the arrow is and this will show the file path of the project.
![image](https://user-images.githubusercontent.com/36930977/119420692-13b5da00-bccb-11eb-9948-82391d6843ab.png)
Copy this path and go to your command prompt window and enter in CD *path* like below:
![image](https://user-images.githubusercontent.com/36930977/119421011-b706ef00-bccb-11eb-9041-5b2255b86e20.png)

### MacOS

![image](https://user-images.githubusercontent.com/36930977/119425755-f0dcf300-bcd5-11eb-834c-85a18ee4a8c9.png)
Click get Info to get more information
![image](https://user-images.githubusercontent.com/36930977/119425836-1bc74700-bcd6-11eb-8391-e66c4fd2074e.png)
Copy the "Where" section
![image](https://user-images.githubusercontent.com/36930977/119425931-444f4100-bcd6-11eb-9917-88fba34b53d4.png)
type "cd " into the terminal and paste the path

After you can type "python main.py" to run the command and if everything is setup then it should create your own EC2 instance! The output will also contain the address. Be sure to copy this down as it will be important later. MacOS users might need to run "python3 main.py"depending on their current configuration. If it is saying that it cannot find modules please try running the pip install commands, but use "pip3" instead of "pip".

MacOS users if it says that the dependency cannot be found, try performing "pip3 install [package]" for each of the dependencies.

## Step Five - SSH into Linux EC2 Instance

Now that we have the ec2 instance spun up we can now SSH into the machine. 

### Windows
I Recommend downloading [Termius](https://termius.com/) to connect via ssh. After you download termius and select the basic plan, click "New Host" and here are the fields you will need to fill out:
 1. Label: Anything you want to name it.
 2. Address: the address that was outputted at the end of the script that I told you to keep copied somewhere in the instructions above.
 3. Make sure SSH is turned on (its a switch)
 4. Keep Port 22 as default
 5. Username: user1 or user2 (this can be edited in the YAML to be a different name)
 6. Password: click Keys and click "+Key" in the bottom right hand corner
   6a. Label: can be whatever you want
   6b. Private Key: click "File"
   6c. Select a "user#-keypair" based on whatever user you are trying to sign in as
   6d. Click save
 7. Click the key you just created
 8. Click save in the top right corner
 9. Double click on the host server you just created
 10. If prompted to add and continue, click add and continue
 11. After this you should be SSHd into the EC2 instance!

### MacOS
You can SSH directly from your MacOS environment via the terminal.
 1. You need to be in the directory of the project to reference the pem keys without using the whole directory.
 2. run a command similar to this: ssh -i user#-keypair.pem user#@outputfromscriptfortheaddress
 3. Here is an example: ssh -i user1-keypair.pem user1@ec2-18-189-16-92.us-east-2.compute.amazonaws.com
 4. If it gives you an error about the key not being secure type the command "chmod 400 user#-keypair.pem". This should fix the issue.

