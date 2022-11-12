# linkedin-challenge

* Create a free email account use python. For example - https://github.com/jinxx0/ProtonMail-Account-Creator
* Register a new account in LinkedIn use this email.
* For the challenge - make a screenshoot for quiz, save it a file and read answer from command line
* Complete registration
* Submit link from email account

## Limitation

* Please work with mail system and LinkedIn use web (no API, no mail protocols)
* Your code should work under Linux system in a docker container
* For start challenge - please fork this repo at your git account

## linkedin-challenge
Project for creating a LinkedIn account using a randomly created email account.

Content
- [Installation](#Installation)
  - [Clone](#Clone)
  - [Required to install](#Required-to-install)
  - [How to run Docker](#How-to-run-Docker)


----

## Installation

### Clone or Download

-  Clone this repo to your local machine using   
```
git clone https://github.com/Misha86/linkedin-challenge.git
```
  or download the project archive: https://github.com/Misha86/linkedin-challenge/archive/refs/heads/main.zip


### Required to install

- [![Python](https://docs.python.org/3.10/_static/py.svg)](https://www.python.org/downloads/release/python-3912/) 3.10
- Project reqirements:
```
requirements.txt
```

### How to run Docker

- Start the terminal.
- Go to the directory "your way to the project" /linkedin-challenge
- Run the following commands
```
docker build -t getEmailImage .
docker run --name getEmailContainer --rm -ti  getEmailImage
```
- During the execution of the last command fill some data in the terminal
- After all you get file with email address and password in the working directory
```
list.csv
```
