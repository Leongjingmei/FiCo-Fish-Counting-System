# FiCo-Fish-Counting-System
A image-based fish larvae counting system using trained YOLOv5

## Instructions To Use
#### Requirements : Python 3.8 or above.

1. Open Command Prompt, type \
`cd path_you_save_the_folder`

2. Create virtual environment following the instructions include in the website: https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/

3. In command prompt, type \
`your_virtual_environment_name\Scripts\activate`

You will now see your virtual environment name with a bracket at the front of current path.

4. Install the requirements.txt in the virtual environment. \
`pip install -r requirements.txt`

5. Download and Install PostgreSQL server. \
PostgreSQL: https://www.postgresql.org/   \
Please remember the password set in the postgreSQL installation. It will be used later. \
![alt text](https://github.com/Leongjingmei/FiCo-Fish-Counting-System/blob/main/images/postgres_pw.jpeg)
 \
6. Set Up PostgreSQL Database \
Open SQL Shell. 

#### In SQL Shell,
Click four times enter to connect to the database. Enter the password you set when you install postgreSQL.

Create a user in PostgreSQL, type \
`create user ficopostgres with password '123456';`
\
Alter the role of the user. \
`alter user ficopostgres with superuser;
alter user ficopostgres with createdb;`

\
Check the role of your user. \
`\du`
\
It should be look like this: 
 \
![alt text](https://github.com/Leongjingmei/FiCo-Fish-Counting-System/blob/main/images/user_role.PNG)
\
To create a database, type \
`create database ficodatabase2;`

\
Connect postgres user to database, type \
`\c ficodatabase2 ficopostgres;`

#### In the ficoflask\ __init__.py line 10, 
Make sure the database url follow the format `postgresql://postgres_user_name:postgres_user_passsword@localhost:5432/postgres_database_name`

#### In command prompt,
To create the tables in ficoflask\models.py
\
`python` \
`from ficoflask import db`
\
`db.create_all()` \
\
To check the database is connected,  \
`from ficoflask.models import User` \
`User.query.all()` 


It should appear `[]` if the database is connected.

\
7. Change the weight path in 'ficoflask\routes.py' in line 22  \
`weight = 'D:/XAMPP/htdocs/Fico1/weights/best.pt' -> change it to the path of your best.pt`

\
8. In command prompt, type  \
`python run.py`

\
You will be able to access to system by typing in your browser 'localhost:5000'.
