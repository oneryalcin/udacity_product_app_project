# Udacity Item Catalog Web Application

One of the Full Stack Nanodegree projects is to use python `Flask` and
`SQLAlchemy` as backend and Bootstrap as frontend to build a catalog
web application.

It also needs to use `OAuth` for user to login to the page.

# Important Notes
In this project I didn't use Udacity Vagrant machine, since I use few
extra Flask Libraries. Please use `requirements.txt` file to install
required libraries.


# Installation
As a best practice please create a new virtualenv
```
virtualenv --python=python3 venv
```

Activate it
```
source venv/bin/activate
```

Clone git repo and install required python packages
```
git clone https://github.com/oneryalcin/udacity_product_app_project.git && cd udacity_product_app_project && pip install -r requirements.txt
```

Run the `setup.sh` file. This file do the following:
 - It will set necessary environment variables
 - Do initial flask DB migrations
 - Populate few categories and items
```
chmod +x setup.sh && ./setup.sh
```

Now you can launch the Web App
```
python app.py
```

Go to `http://127.0.0.1:5000` to view app


## Authentication
App uses Google OAuth for authentication and authorization

