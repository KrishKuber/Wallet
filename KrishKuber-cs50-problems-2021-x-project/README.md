#### Walet
#### Video Demo:  https://youtu.be/8lSMjdh_MmI
#### Description:
### General Description

# Wallet is basically a software that helps store and retrieve daily expenses making managing
# home finances easy. It is a clean, modern website which will help users in every step
# It was born out of the chore to maintain daily expenses given to me by my parents.


### The static folder:

## styles.css-
# Styles.css is basically a CSS(Cascading Style Sheets) file used to beautify a website.
# It has modified a lot of aspects of the website visually utilizing different classes
# , ids and tag selectors. Some of the classes have been derived using Bootstrap libraries
# and certain aspects of them have been a bit modified by me because ,no doubt the Bootstrap library
# acts as a good template but it had to fit the nits and pickies of my website. For example the class
# 'form-control' was placing the table in the center and causing a horizontal scrollbar or x-scrollbar to 
# occur causing convienience issues.


### The templates folder: The folder where all the HTML Files are stored 

## layout.html-
# This is where all the basic layout is laid out including the very important nav-bar.
# The JQuery Library and bootstrap library was imported here which is applied to every page
# using Jinja templating(by utilizing {{% block main%}} and {{% endblock %}}), a div contains
# all the rest of the templates. The layout has also been programmed to show menu link if only 
# the user has logged in. 


## index.html
# This is the index of the website where the login and register options are shown along with the
# main motto

## register.html
# This is where a new user is expected to go to signup for the website.
# The credentials are taken from here put into a database and then the user is logged in
# also an option for logging in if already signed up is provided via a link. Leaving anything empty
# gives a warning using 'required' attribute of input tag also if the password , minimum requirement for both fields is 4 using 'minlength' atrribute of input tag and confirm password 
# do not match a warning is given via an alert(JavaScript). Some aesthetics are added. Also an existance
# check for username is done by using an ajax request and returning an alert if username exists

## login.html
# There are two inputs one for username other for password. The input is checked against the data base and
# authentication is carried out for the same and the user is logged in. Option to register if not registered
# yet is provided via a link.

## dashboard.html
# This is the homepage of the website where the user is first greeted then his monthly total along with 
# quaterly average is shown. Also a table displaying last 10 entries is shown using jinja templating.


## table.html
# here a record of all previous epenses are diplayed with a cool search feature implemented using
# AJAX(JQuery) and javascript. Here expenses can be inserted as well as deleted. The date, item, price, 
# category, and mode of payment is displayed.

## texpense
# It is just a shortened but handy version of table where you can insert and delete your daily expenses
# also a cool feature over here is that the daily total is shown.


### application.py

## route(/):
# Just returns the index.html

## route('/register', methods=["POST", "GET"])
# GET method returns register.html page
# POST method is invoked on clicking submit button to register on the page the credentials are obtained.
# The password is hashed and everything is inserted in the table. Then the session is updated with the user id

## route('register/check')
# reacts to the ajax call and returns error code 1 if username is found or otherwise 2

## route('logout')
# clears the session(The notion off logging out) and redirects user to index page.

## route('login')
# clears the session just as a precaution and retrieves data from login page and
# checks if username exists in database and returns error if it does not exist else it redirects to 
# login page

## route('table', methods=["POST", "GET"])
# GET: The db.execute command is used to retreive info from the table and is arraged according to Descending order
# POST: Invoked when insert is performed and inserts data into the table 

## route('table/delete')
# makes use of post function only on the pressing of delete button and removes the item from the list
# by deleting it from the record table

## route('/table/(item, date, category, price,mode (any one))')
# One of the above is invoked in search query for one the following respectively
# Returns filtered records by utilizing the 'where' axiom of SQL

## route('/texpense', methods=["POST", "GET"])
# GET: records of today are retrieved by utilizing the datetime library of python and then using the
# where axiom of SQL to retrieve todays function.
# POST: Invoked on insert query and funtions same as route('/table', method=["POST"])
# but date is automatically set as todays date by utilizing the datetime library of python
# and using the date.today() method from it

## route('/texpense/delete', method=["POST"])
# same as route('/table/delete', method=["POST"]). Another interesting thing to mention is that the 
# records are deleted on the basis of item id because if other quantities were compared using where
# and 2 records are same both the columns would have been deleted causing issues. So a primary key
# was set for records table in wallet.db called "item_id". The item_id was retrieved from the form using hidden input field in the form.
# This is highlighted below under wallet.db
# section

## route("/dashboard")
# If the user has logged in the dashboard is displayed preventing any malicious activity by users by just
# putting in /dashboard in the search bar. Then the user is greeteg by using the session variabke to get
# user id and then the table to get the username.
# then the total for 3 months was used for calculating the average and both were calculated by using
# records['price'] and adding them to an accumulator. At last the last ten entries of the user are 
# retrieved using the 'limit 10' axiom of SQL.


### wallet.db

## users table: Contains the user_id as primary key and then username and hashed password
## records table: Contains date, item, price, mode, category of the expense and then also assigns
## a primary key as record_id to distinguish each record and help with deletion.


### Difficulties
## Honestly there were no 'difficulties' as such it was just a learning process which I think was 
## the aim of the whole final project was to 'learn from experiance' or 'hands-on'
## Overall I learnt a lot of new syntax and a lot of new principals and most importantly
## got my 'introduction to computer science' for a lifetime :) .  









































