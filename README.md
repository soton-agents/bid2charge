# BID2CHARGE SETUP INSTRUCTIONS

Follow these instructions to set up a development environment for running Bid2Charge on your local machine.

To begin with, please ensure you have the prerequisites below installed on your production machine, as well as MySQL (both server and client) and Python2.7. Once that is done, follow the steps below.

1. MySQL
2. Python2.7
3. Pip

Follow the steps below for setting up your environment: 

1. Install virtualenv: 
```
 $ sudo pip install virtualenv
```

2. Create a new directory for the code base and the virtual environment (e.g., ~/bid2charge). From within the new directory, create a virtual environement with the name env: 
> $ virtualenv env

3. Create another folder for the code base, e.g., ev-charging-game. Copy the source code for the game into that directory.

You should now have the following file structure: 
bid2charge/
| - env/
|   | - ...
| - ev-charging-game/
|   | - EVChargingGame/
|   | - webapp/
|   | - db_scripts/ 
|   | - manage.py
|   | - ...

4. Add a username and password to the EVChargingGame/example_local_settings.py file and rename it to local_settings.py (other settings could be added here too). 

5. Install all the necessary python packages under your virtual environment. Change to the ev-charging-game folder (you should have a file called requirements.txt) and run the command below. The requirements file contains all the python packages required. Pip will try and install every one of them if they are not already installed. Also, since we're using the pip from our virtual environment, all the packages will be installed under the virtual environement. 
> $ sudo ../env/bin/pip install -r requirements.txt

6. Create an empty MySQL database named ev_game_db. You can do this using the MySQL command line tool, by following the steps below: 
> $ mysql -u root -p -h localhost
...(enter password if prompted)
>> create database ev_game_db;

7. From the same main directory (which contains the file manage.py) run the command below for synchronizing your django models with the newly created database. 
> $ ../env/bin/python manage.py syncdb


8. Apart from the django default database synchronization tool, we are using South for migrating our models. Run the commands below in order to finish migrating all necessary models. 
> $ sudo ../env/bin/python manage.py schemamigration webapp --initial
> $ sudo ../env/bin/python manage.py migrate webapp
> $ sudo ../env/bin/python manage.py migrate allauth.socialaccount
> $ sudo ../env/bin/python manage.py migrate allauth.socialaccount.providers.facebook


9. Go to the db_scripts folder and import the main db data by running:
> $ sudo mysql -u root -p ev_game_db < prod_data.sql

10. Collect static files. From the main folder (containing the file manage.py) run:
> $ sudo ../env/bin/python manage.py collectstatic

11. Now, you can make sure that everything is set up properly by opening a new terminal window, going to the root directory of your project (the one containing the file manage.py) and run the command
> $ ../env/bin/python manage.py runserver  

If successful, you should see your server up and running. You can test it by accessing http://localhost:8000/jair with your browser. This will show you the game as experienced by our MTurk participants.

You can play a shorter version of the game by accessing http://localhost:8000/orchid

The admin interface is available via http://localhost:8000/admin

To create an admin user, use the following command:
> $ ../env/bin/python manage.py createsuperuser