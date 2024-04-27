from requests import get, post, delete
from pprint import pprint

########################
#  User List Resource  #
########################
pprint(get("http://localhost:5000/api/v1/users").json())  # get all users
pprint(post("http://localhost:5000/api/v1/users", json={"name": "Lol", "email": "idrerd@email.com"}).json())
# bad request: no password key
pprint(post("http://localhost:5000/api/v1/users", json={"name": "Lol", "email": "idrerd@email.com", "password":
    "security123456"}).json())  # bad request: user with email idrerd@email.com is already registered
new_user_response = post("http://localhost:5000/api/v1/users", json={"name": "Lol", "email": "lol@omail.lol",
                                                                     "password": "security123456"}).json()
pprint(new_user_response)  # add new user
pprint(get("http://localhost:5000/api/v1/users").json())  # check that new user have been added
########################
#     User Resource    #
########################
pprint(get("http://localhost:5000/api/v1/users/2").json())  # get user with id 2
pprint(delete(f"http://localhost:5000/api/v1/users/{new_user_response.get('id')}", json={"name": "Lol",
                                                                                         "email": "lol@omail.lol",
                                                                                         "password": "security"}).json())
# try to delete a user we just added but wrong password
pprint(delete(f"http://localhost:5000/api/v1/users/{new_user_response.get('id')}",
              json={"name": "Lol", "email": "lol@omail.lol", "password": "security123456"}).json())
# delete a user we just added
pprint(get("http://localhost:5000/api/v1/users").json())  # check that the user is deleted