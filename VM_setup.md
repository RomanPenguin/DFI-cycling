# Introduction
This file contains instructions to create a fresh VM to create csv and shape files from collected data. This instruction is in addition to a pre-made VM for easy setup. 

# VM initial set up 
The following instructions are relevant for a PC user. 

First check if your PC is ready for virtualisation by checking under Task Manager -> CPU -> Virtualization is enabled. If not, consult with manufacturer's manual for instructions to enable. 

Download VirtualBox for Windows hosts from Oracle https://www.virtualbox.org/wiki/Downloads 
Download Ubuntu disk image https://ubuntu.com/download/desktop 

Once VirtualBox is installed, click on New. 

Choose a name and save location for the new virtual machine, ensuring that the type is Linux and version is Ubuntu (64-bit)

The recommended amount of ram is at least 4GB, and more is better. Due to the sizes of some of the video files it is important to have decent amount of ram assigned to the VM. 

Creating a virtual hard disk and select the default option of VDI and dynamically allocated in the next few prompts. Select the location and allocate 50GB or more if processing large amounts of data. It can be expanded later via a more involved process. 

Start the VM and select a start-up disk, via the optical disk selector. Click on add and navigate to your downloads folder where the Ubuntu iso file is saved. 

Install Ubuntu and if required select install third-party software to playback video files. Disk can be safely erased when prompted. Create your own username and password. Follow on-screen instructions, reboot and then log in. 

## when the VM is not running, go to machine -> settings -> system -> processor and increase the number of processors allocated. More processors for the VM will increase the speed of the processing. This step is highly recommended. 

# Ubuntu set up 
Open terminal (ctrl+alt+T) and enter

`sudo apt update`

`sudo apt upgrade`

When prompted for sudo password, enter your Ubuntu log in password. When prompted for do you want to continue, enter y. 

Install the following:

` Sudo apt install gcc make perl curl`

Go to devices -> insert guest additions CD image and select run. Reboot the VM once it is finished. 
## Guest additions enable convenient features such as shared clipboard between Windows host and Ubuntu VM, resizable VM window and more, it is highly recommended to be installed. 
 
# install required software  

**Do all of the following within the VM and NOT in the host Windows machine**

Download and install anaconda (https://www.anaconda.com/products/distribution) 

Navigate to the Downloads folder and right click -> open in terminal, then paste the following into the terminal (check the version numbers, they may be different) 

`chmod +x Anaconda3-2022.05-Linux-x86_64.sh`

`./Anaconda3-2022.05-Linux-x86_64.sh`

Go through the installation prompts and use default options. 

Download and install vscode (https://code.visualstudio.com/docs/setup/linux) (Check version numbers, they may be different) 

`sudo apt install ./code_1.68.1-1655263094_amd64.deb`

Download and install QGIS 

Follow the instructions from the official website (https://qgis.org/en/site/forusers/alldownloads.html#debian-ubuntu)


`sudo apt install gnupg software-properties-common`

`wget -qO - https://qgis.org/downloads/qgis-2021.gpg.key | sudo gpg --no-default-keyring --keyring gnupg-ring:/etc/apt/trusted.gpg.d/qgis-archive.gpg –import`

`sudo chmod a+r /etc/apt/trusted.gpg.d/qgis-archive.gpg`

sudo add-apt-repository "deb https://qgis.org/ubuntu $(lsb_release -c -s) main"`

`sudo apt update`

`sudo apt install qgis qgis-plugin-grass`


Install git 
`sudo apt install git`

# Code set up 
Open VS Code, go to the left sidebar and select extensions. Install Python extension. 
Go to the sidebar and select explorer. Click on Clone repository and paste the following GitHub repo address 

https://github.com/RomanPenguin/DFI-cycling


Select a location to save the project, and wait for the download to finish. 

Once the download is finished, open the cloned repository and select “Yes I trust the authors”. 

# Python environment set up 

Open terminal and type in 

`anaconda-navigator`

When it prompts to update, click on update. 

Go to the environment tab, then click on create. Pick a name (tip: name it somethingsomethingenv to easily distinguish it) and select Python 3.9.12 (do not use 3.10) 

Go to VS Code, select Settings at the bottom left, then extensions -> Python. Find the field for Conda path and put in the path to the Anaconda3 folder. (Default is under /home/[username]/anaconda3).  

Go to view->command palette and type in 

`Python: Select Interpreter` 

Select the newly created environment from above (somethingsomethingenv). 

# Install Python dependencies 

Open a terminal in VS Code, ensure that the name of the new environment is shown in brackets. Type in the following command 

`pip install -r requirements.txt`

`pip install -r newreq.txt `

`pip install deepface==0.0.75 `

If there is an error after newreq install, proceed and ignore the error message. 

Once everything is installed, open Anaconda Navigator and search for the following packages. Make sure to change the drop down from “installed” to “not installed” 

```
Pytorch 
Torchvision
Natsort 
Gdal

```

Then select apply and install the packages. 

# miscellaneous dependencies 

Open a terminal and install NVM 

` curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash`

Close the terminal window and open a new terminal window in VS Code. 

In the new terminal type in 

`nvm install --lts`

Initialise the Django project by typing into the terminal 

` cd bicyclewebsite/`

`python manage.py tailwind install`

```
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
```

create a user for the web interface 

` python manage.py createsuperuser`

follow the on-screen prompts to create an user. 

# set up debug server 

Select debug on the left sidebar and click on create a launch.json file. Replace everything in the new file with the following and save. 

```
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: emotest",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/emotion_detection_emonet.py",
            "console": "integratedTerminal",
            "justMyCode": true
            
        },
        {
            "name": "dev server",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/bicyclewebsite/manage.py",
            "console": "integratedTerminal",
            "args": [
                "runserver",
                "127.0.0.1:8000"
            ]
        }
    ]
}
```

Select the explorer on the left sidebar and navigate to 

`DFI-CYCLING/bicyclewebsite/dataportal/views.py` 

Change the default save location to 

`/home/[username]/Documents/output/`


# AWS set up (no longer used) 

# Run the debug server 

Go to the left sidebar and select debug. Next to the green run button use the drop down menu and select dev server, then press the green button. 
Open the web browser and type into the address bar 

`127.0.0.1:8000/dataportal`

Use the username and password generated above (superuser generation) to log in. 

