# ConcordiaAce Dev Code

# Test docker container website link:

http://138.197.132.31/

- Note, not https secure: do not enter real personal info or password
- Serviced by nginx, up to 4 processors.  

# Licensing
- All python/django code are created by us and available under MIT licence
- html template license was purchased for single app use for Concordia ACE website on http://preview.themeforest.net/item/oficiona-job-board-html-template/full_screen_preview/23042674 License must be re-purchased for other project. Permission to reuse template not under MIT license. 

# Dependencies

See requirements.txt for full list

- Python 3.7
- Django 3.0
- django-file-resubmit==0.5.2
- django-sendfile==0.3.11
- django-sendfile2==0.5.1
- django-tinymce==2.8.0
- Pillow==6.2.1
- pytz==2019.3
- sqlparse==0.3.0
- six
- matching==1.1
- weasyprint
- requests
- psycopg2
- pypdf2


# Dev installation
1) Install git
2) Create a local directory, run:
   - Make a folder for the project
   - git init
   - git remote add upstream  https://github.com/MattYu/ConcordiaAce/.git
   - git fetch upstream
   - Create your own work branch: git checkout -b <name of your workbranch>
3) Install Python 3.7
   - When installing, on Windows, make sure to tick/select "pip", "install for all users" and "Add Python to environment variables"
   - Check that python has been successfully installed by running "python -v" in a console
   - Check that pip has been successfully installed by running "pip freeze" in a console
4) Strongly recommended: Install virtualenv
   - Run a powershell with admin privilege
   - Execute "Set-ExecutionPolicy Unrestricted"
   - Execute "pip install virtualenv"
5) Strongly recommended: Create a virtualenv for the project before installing dependancies 
   - go to project's folder
   - create a folder call cfehome
   - cd cfehome
   - create virtual env virtualenv .
   - run virtualenv ".\cfehome\Script\activate"
6) Install all dependencies, use same version as dependency section of readme
   - pip install django==3
   - pip install django-widget-tweaks
   - python -m pip install Pillow
   - pip install django-tinymce
   - pip install django-sendfile
   - pip install django-sendfile2
   - pip install django-file-resubmit
   - pip install six
   - pip install matching
   - pip install weasyprint
   - pip install requests
   - pip install psycopg2
   - pip install gunicorn

7) Migrate static files. Do this every time you make a change to a static file. You might also need to clear your browser cache or use incognito mode to see the effect of your change. 
   - "python manage.py collectstatic --noinput --clear"
  
8) Run server in debug mode Go to Ace folder.
     - python manage.py makemigrations
     - python manage.py migrate
     - python manage.py createsuperuser
         - User type = 4
     - python manage.py runserver
  

10) Push your branch. When ready to merge, make a pull request. Please never merge directly into master. 

# Deploying to production

To run on a docker environment

- Navigate to prod code
- Set up prod encryption keys in env [not included]
- execute 'docker-compose build'
- 'docker-compose up'
- 'docker-compose -f docker-compose.yml run --rm web python manage.py collectstatic'
- The code is now running on a docker prod environment on localhost
- Export this to a a cloud provider (I use vs code extension to auto migrate to Azure), and add the server's ip to the allow host list in ace/settings.py. 

Useful resources
- https://docs.djangoproject.com/en/3.0/howto/deployment/
- https://www.youtube.com/watch?v=Sa_kQheCnds

Needs to:
- Set up protected file directory, see x-sendfile documentation https://github.com/johnsensible/django-sendfile. Note: media should be serviced by Apache or NGINX. 
- Remove test SQLite db; use postgreSQL instead. 
- Set up prod email notification in settings.py.
- Set up prod encryption keys.
- Set up https and certification.

# Commands

- > pip install virtualenv

-pip install django-widget-tweaks

-python -m pip install Pillow

-pip install django-tinymce

-pip install django-sendfile2

-pip install django-file-resubmit



Note that files upload will be service by Apache and x-file in production, on top of Django
