# Password Manager and Generator

This is a simple application that allows you to create strong random passwords, save login credentials securely using encryption, and search for saved credentials by website name. It is built with Python and uses a graphical user interface (GUI) for ease of use.

## Files in this Project

main.py  
This is the main program file. Run this file to start the password manager application.

key.key  
This file contains the secret encryption key used to lock and unlock your saved passwords. It is automatically generated the first time you run the program. Do not delete this file. If it is removed, you will not be able to decrypt or access any saved passwords in the application.

data/passwords.enc  
This file stores all of your saved login credentials. It is fully encrypted and cannot be read without the key.key file. If you open this file in a text editor, it will display random characters instead of your actual passwords.

requirements.txt  
This file lists all Python libraries that the application needs to run. These include cryptography for encryption and tk for the graphical interface. To install these libraries, use the following command in your terminal:  

pip install -r requirements.txt  

## How to Run

Download the project folder and open a terminal in the folder location. Install the required libraries using the command:  

pip install -r requirements.txt  

Once the libraries are installed, start the application by running:  

python main.py  

## Important

Keep both key.key and passwords.enc safe in the same folder as main.py. If you lose the key.key file, you will not be able to unlock or retrieve any of your saved credentials. The key.key file is required to decrypt the encrypted data stored in passwords.enc.

