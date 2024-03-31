<h1 align="center" id="title">Crowd Funding Web App - ITI</h1>

<p id="description">Crowd Funding project aims to create a web platform for starting fundraising projects in Egypt where people can view donate and rate projects. The project is developed using the Python Django framework.</p>
<h2>🚀 Demo</h2>
## User demo
<a href="https://youtu.be/0i51dEKlgeU">
  <img src="https://img.youtube.com/vi/0i51dEKlgeU/0.jpg" alt="Video thumbnail">
</a>



## Admin demo
https://github.com/HudaMohamed22/CrowdFunding-Web-App-Django-ITI/assets/76265525/f631c400-8c20-40d9-bdbb-e33db9f17b3c


<h2>🧐 Features</h2>

Here're some of the project's best features:

where user can 
*   Sign Up & Sign with email verification
*   can view edit and delete his profile data
*   View all his projects and all donations
*   Create projects and donate for projects
*   View project details and rate it
*   Add comments to any project
*   Report inappropriate projects or comments
*   Live search for project by project name or tag
*   Browse projects based on category

From admin view- where admin can:
*   Create, edit, and delete category
*   Choose the featured project to be shown on the home page

You can create an admin user by

```
manage.py createsuperuser
```
Then log in to the application to view the dashboard
<h2>💻 Built with</h2>

Technologies used in the project:

*   Django framework
*   MySQL database
*   HTML and CSS
*   JS and Bootstrap
<h2>🛠️ Installation Steps:</h2>

<p>1. Download or Clone the project</p>

<p>2. Install python with V.3+ and MySQL database on your machine</p>

<p>3. Install and activate VirtualEnvironment in the *window* terminal and write the following </p>

```
- pip install virtualenv        to install virtual environment 

Enter the project folder and write in the terminal 
-  virtualenv .venv                            to create  Venv    
- .venv\Scripts\activate                       to activate it 

```
<p>4. Install requiremental packages</p>

```
pip install -r requirements.txt 
```
<p>5. Make sure that MySQL server is running  </p>

```
Press Win + R, type services.msc, and press Enter and look for a service named something like "MySQL"
```
<p>6. Create .env file in the project path to put your credentials</p>

```
DB_NAME=' Your DB_NAME'
DB_USER='Your DB_USER'
DB_PASSWORD='Your DB_PASSWORD'
EMAIL_HOST = ' Your EMAIL_HOST '
EMAIL_FROM = 'Your EMAIL_FROM '
EMAIL_HOST_USER = 'Your EMAIL_HOST_USER '
EMAIL_HOST_PASSWORD = 'Your EMAIL_HOST_PASSWORD  '
```

<p>7. Run the following to load the project's models into tables in your database</p>

```
python manage.py makemigrations
python manage.py migrate
```
<p>8. Finally, Run the Django Server</p>

```
python3 manage.py runserver
```
<p>Take the link http://127.0.0.1:8000/ and put it into your browser to start browsing the web app </p>

<h2>Contributors</h2>

Huda MuhaMmed: https://github.com/HudaMohamed22

 Noran Zaki: https://github.com/noranzaki

Keroles Nady: https://github.com/Keroles-Nadyy

ArwaHazem: https://github.com/ArwaHazem

DoaaGamal: https://github.com/Doddg10
