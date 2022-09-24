# Guider
Guider is a service for creating and searching for guides for all occasions, based on DRF.

User can register there with login and password, add extra information about him/herself after registration.
Then user can create a guide with text and picture. Unregistered user can only see guides without creation or leaving comments. 

After creation the guide should be checked by moderators.
Without moderation nobody, besides the moderators and administrator, will be able to see the guide.
After moderation a guide may be seen by everybody, even by unregistered users.

When the user offers changes in moderated guide, it becomes non-moderated again and requires moderation.

Registered user can write text comments to guides.

Registered user can rate a guide with either like or dislike. Guides can be ordered by their rating.
___
The first thing to do is to clone the repository:
```sh
$ git clone https://github.com/alexhlobel/Guider.git
$ cd guider
```
***There is a Makefile in the project, some commands can be done with it's help***
___
Create a virtual environment to install dependencies in and activate it:

If you want to continue with python3.9, it is enough to use virtualenv.
Environment activation should be performed in the projects root folder.
```sh
$ pip install virtualenv
$ virtualenv -p /usr/bin/python3.9 <your_env_name>
$ source <your_env_name>/bin/activate
```
or just
```sh
$ make venv
```
For python3.10 it is possible to use pyenv.
Installation process is described in several sources:
https://github.com/pyenv/pyenv#installation

Environment activation should be performed in the projects root folder.
```sh
$ pyenv install 3.10.4
$ pyenv virtualenv 3.10.4 <your_env_name>
$ pyenv local <your_env_name>
```
___
Then install the dependencies:
```sh
(<your_env_name>)$ pip install -r requirements.txt
```
or just
```sh
(<your_env_name>)$ make install
```
___
In order to connect to your PostgreSQL database write your database credentials as environment variables in .env file.
You can use existing .env.example file, rename it and change the values of the variables.

If something goes wrong, replace DATABASES value in config/settings.py to default:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
In case if you want to create Django configuration in PyCharm, that works with .env file, follow these steps:
1. Install plugin: envfile plugin from jetbrains.com
2. In PyCharm: Edit Configurations -> Press '+' -> Find Django Server
3. Name it (like 'run django')
4. Enable Django support for the project (Press 'Fix') -> Mark 'Enable Django support'
5. Django project root: Add full path to project (it is called the same, as the main folder of your django project, but inside and contains 'settings.py'. This folder may be renamed in 'project'
6. Check if the paths to Settings (settings.py) and Manage script (manage.py) are ok
7. Then just Apply -> Ok
8. Once again Apply -> Ok
9. Edit Configurations -> check if paths in Environment variables in your 'run django' (or how you named it) are correct. If not (f.e. for settings), correct it (f.e. from DJANGO_SETTINGS_MODULE=settings to DJANGO_SETTINGS_MODULE=project.settings) 
10. Edit Configurations -> EnvFile -> Enable EnvFile
11. Press '+' -> Choose .env file -> Press icon with an eye to see hidden files -> find the path to .env file

In the end .env must be in the same folder with manage.py.
___
At this point you can check, if everything launches. Let's start the project:
```sh
(<your_env_name>)$ python manage.py runserver
```
or just
```sh
(<your_env_name>)$ make run
```
___
Make initial migrations:
```sh
(<your_env_name>)$ python manage.py makemigrations
(<your_env_name>)$ python manage.py migrate
```
or just
```sh
(<your_env_name>)$ make migrate
```
___
Don't forget to create superuser:
```sh
(<your_env_name>)$ python manage.py createsuperuser
```
or just
```sh
(<your_env_name>)$ make superuser
```
---
Navigate to `http://127.0.0.1:8000/`.

List of possible urls may be seen in config/urls.py in config and guider_app/urls.py
or with the help of Debug tips.
___
If you want to use already existing example DB objects, load fixtures:
```sh
(<your_env_name>)$ python manage.py loaddata fixture.json
```
___
Following commands will help you to create docker container and bind the container and the host machine to the exposed port.
Do it from the project's root folder:
```sh
(<your_env_name>)$ docker-compose build
(<your_env_name>)$ docker-compose up -d
```
or just
```sh
(<your_env_name>)$ make deploy
```

Have fun! :)