# Slot-machine

Bringing the sizzle of '20 Super Hot' to life with Django REST API: a dynamic and immersive casino gaming experience at your fingertips.

## About the project

### Introduction

The project aims to develop a captivating and entertaining slot machine game inspired by the popular casino game "20 Super Hot" Leveraging the appeal and mechanics of the original game, our objective is to create an engaging digital experience that captivates players with its vibrant visuals, exciting gameplay, and potential for lucrative rewards.

### Technical details

This project is implementation of Slot machine using Django REST API at the server side, for handaling all the logic.
For the client side i am using pygame for all the vizualization and animations.
The project is simulatoin of the famous slot machine casino game "20 Super Hot".

The project implement the following functionalities:

* Creating an account
* Login to account
* Depositing money to account
* History of user spins
* Statistics of user history
* Getting the leaderboard of users in the system (ordared by profit, bigest win, etc)
* Spining the slot machine
* Auto spin the slot machine
* Changeing the bet amount
* Cool animations and audio
  
## Project preview
https://github.com/SashoVas/Slot-machine/assets/98760930/221f9b98-3961-4562-b3f5-3b9386ba818b


## How to use it

1. Clone the repository to your local machine using the command
```bash
 git clone https://github.com/SashoVas/Slot-machine.git.
```
2. Navigate to the project directory using the command
```bash
 cd Slot-machine.
```
3. Install the required dependencies by running
```bash
 pip install -r requirements.txt.
```
4. Create a virtual environment for the project using
```bash
 python -m venv venv.
```
5. Activate the virtual environment with the command source ```bash venv/bin/activate``` (for Linux/Mac) or ```bashvenv\Scripts\activate``` (for Windows).

6. Set up the database by running
```bash
python manage.py migrate.
```
7. Start the development server with
 ```bash
python manage.py runserver.
```
8. Open your web browser and go to http://localhost:8000 to access the Slot-machine application.
Make sure you have Python and Django installed on your machine before starting the setup process.

## Build with
* Python 
* Django
* Django REST API
* Pygame
* requests