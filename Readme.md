Mike Creatives with Hilmus Admin
--------------------------------
--------------------------------


**This is an app that is responsible for rendering the mike Creatives site**

**The site is live at [This url](mikecreatives.com)**

<br />

The site runs on a python web framework that is django and that is the webframework for the perfectionists with deadline.

To use the app, that is 100% dynamic.
###### First ensure that python is installed in your computer
You can download that from [python's official Website](www.python.com)[python Installation]

###### Secondly Clone the repository
```bash 
    git clone https://mikecreatives.com/jetsstarpus/hilmus_mike.git
```

###### Create a virtual environment
A virtual environment will help to make your apps workon independent packages that can be reused and deployed alongsite with the app.
To create a virtual environment, install *virtualenvwrapper* following this <a href="https://virtualenvwrapper.readthedocs.io/en/latest/install.html">tutorial.</a>
Get to the environment that you just created
```python 
    workon yourenv
```

###### Install the dependencies for the app
```python
    pip install -r requirements.txt
 ```

###### Configure the Database
<pre><code>Navigate to `hilmus-mike/settings/local.py` and configure the database as per django's specification</code></pre>

###### Run migrations
```python
    python manage.py migrate
```

###### Start the development server
```python 
    python manage.py runserver
```

You are up, the site is running
