

Two folders are created - backend and inside it frontend

main.py has all the crud operations get, post, put and delete request . It also includes a simple authentication which uses a token that lasts for 30 minutes 

the database.py file has motor mongodb client that links our backend with with a mongodb database that has url : mongodb://localhost:27017

model.py has schema model Todo from basemodel and User class used in authentication

to run the backend:

1 ) from within the backend folder install fastapi and uvicorn .
2 ) the mongodb should be installed on the machine locally 
3 ) run mongod in powershell as an admin. This starts mongodb.
4 ) from mongodb compass paste the url : mongodb://localhost:27017
5 ) this will open the mongodb local  . Create TodoList database
6 ) write pip install pipenv to install pipenv
7 ) write pipenv shell
8 ) write uvicorn main:app --reload 
9 ) open fastapi swagger with this url : http://127.0.0.1:8000/docs 

--if you are using it for first time or want to create a new user but the authentication is not integrated into the frontend it is done through separate requests through fastapi swagger
-- to use frontend type at first npm i to install node_modules
10 ) click on POST/sign_up Sign Up tab and click Try it out in top right corner
11 ) just replace the values of username and password with your desired values and click on Execute
   note the server response and a new user can be seen in the database TodoList under collections    todo
12 )now click on authorize in top right corner and give the username and password you used for signup
13 )respective post , update , create, get and delete can be made from fastapi swagger
14 ) to use frontend we move into frontend folder typing cd frontend 
15 type npm start and it will show up the frontend listing the values in the database . We can create and delete using the frontend
