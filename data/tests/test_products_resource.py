from requests import get, post, delete
from pprint import pprint

new_user_response = post("http://localhost:5000/api/v1/users", json={"name": "Lol", "email": "lol@omail.lol", "password": "security123456"}).json()
# add new test user to make sell orders
#########################
# Product List Resource #
#########################
pprint(get("http://localhost:5000/api/v1/products").json())  # get all products
pprint(post("http://localhost:5000/api/v1/products", json={"name": "TestResourceAPI", "count": 10, "user_id": new_user_response.get("id")}).json())
# try to set sell order but price key is missing
new_product_response = post("http://localhost:5000/api/v1/products", json={"name": "TestResourceAPI", "price": 1, "count": 10, "user_id": new_user_response.get("id")}).json()
pprint(new_product_response)
# sell new product
pprint(get("http://localhost:5000/api/v1/products").json())  # check if product added
#########################
#    Product Resource   #
#########################
pprint(get("http://localhost:5000/api/v1/products/13").json())  # get product with id 13
pprint(delete(f"http://localhost:5000/api/v1/products/{new_product_response.get('id')}", json={"name": "Lol", "email": "lol@omail.lol", "password": "security"}).json())
# try to delete product but wrong password
pprint(delete(f"http://localhost:5000/api/v1/products/{new_product_response.get('id')}", json={"name": "Lol", "email": "lol@omail.lol", "password": "security123456"}).json())
# delete product
pprint(get("http://localhost:5000/api/v1/products").json())  # check if the product is deleted
delete(f"http://localhost:5000/api/v1/users/{new_user_response.get('id')}", json={"name": "Lol", "email": "lol@omail.lol", "password": "security123456"}).json()
# delete a test user
