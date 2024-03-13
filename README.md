# Bills-Reminder-App-Using-Flask

It's a web application based on flask framework(including Celery and Redis for background Functions) which 
helps you in reminding your bill's payment by sending you an email before its due date to avoid extra fee.
[Website Link](https://priceless-johnson-639019.netlify.app/)

## Description

What a user can do:
1.First the user have to register.
2.After registration process user can add bill reminde
- Enter Bill name (Eg-Electricity) and Bill Category (Eg-HouseHold)
- Amount of bill to be paid
- Due date of the bill
- User can choose when he/she want's to be notified before the due date (Ex- 1day beforehand/2days beforehand etc)
- User can repeat that reminder every week/month/year.
- User can enter a note with the reminder which will be shown in the E-mail.


## Home Page
![Website Image](app/static/img/g1.png?raw=true "Title")

## Add Reminder Page
![Website Image](app/static/img/g10.png?raw=true "Title")

## Search Reminder Page
![Website Image](app/static/img/g11.png?raw=true "Title")

## Community Page
![Website Image](app/static/img/g3.png?raw=true "Title")


## Account Page
![Website Image](app/static/img/profile.png?raw=true "Title")

## Login Page
![Website Image](app/static/img/g6.png?raw=true "Title")

## Register Page
![Website Image](app/static/img/g7.png?raw=true "Title")

## User Databse
![Website Image](app/static/img/readme_pic5.jpg?raw=true "Title")


## Bills Databse
![Website Image](static/img/readme_pic6.jpg?raw=true "Title")


## Set Up

Take These Steps to configure the Project :

* Clone The Repository
```
git clone https://github.com/apoorva-01/Bills-Reminder-Using-Flask-and-Celery
```

* Create a virtual environment(Code is for Windows Only)
```
python -m virtualenv venv
```
* Activate virtual environment(Code is for Windows Only)
```
venv\Scripts\activate.bat
```

* Download all required modules using
```
pip install -r requirements.txt
```

* Configure Email id and Password in config.json File

* Run Redis Server at 6379 port

* Open command Prompt in the Project Directory and run Celery Worker Using :(We have used eventlet module to run celery on windows because it is not supported on windows)
```
celery -A app.celery worker -l info -P eventlet
```

*  Again open command Prompt in the Project Directory and run the app.py file :
```
python bills.py
```


*  Again open command Prompt in the Project Directory and run the app.py file :
```
pip install itsdangerous==2.0.1
pip install mysqlclient
```

*  Make a local database of name "bills_app" with 2 tables named "entry" and "user" respectively 
## Entry
![Website Image](app/static/img/readme_pic5.jpg?raw=true "Title")<br>
## User
![Website Image](app/static/img/readme_pic6.jpg?raw=true "Title")<br>


*  Now Head on to ['http://127.0.0.1:5000/'](http://127.0.0.1:5000/)

