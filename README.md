# Grocery expiry tracker

### API Endpoints
GET, POST `/api/food`
- CRUD on the list of food.
- When inserting new food into the api, the api will give an estimated expiry date based on the food inserted. 

Examples:

POST
```python
import requests
import json

url = 'http://localhost:1337/api/food/'
headers = {'Content-Type': 'application/json'}
data = {'name': 'Banana'}
data = json.dumps(data)

response = requests.post(url, data=data, headers=headers)
print(response.status_code)  # 201 Created
print(response.json())       # dict of the new object    

```

DELETE
```python
import requests
import urllib.parse


url = 'http://localhost:1337/api/food/'

# Get the id of the food
params = {'search': 'Banana'}
response = requests.get(url, params=params)

print(response.json())        # [{'id': 2, 'name': 'Banana', 'expiry_date': '2020-03-25', 'image': None}, {'id': 4, 'name': 'Banana', 'expiry_date': '2020-03-25', 'image': None}]
id = response.json()[0]['id']

# Delete using the id
delete_url = urllib.parse.urljoin(url, str(id))
response = requests.delete(delete_url)

print(response.status_code)  # 204 No Content
```


### Tunneling with ngrok
Download [ngrok](https://ngrok.com) to host the api from your computer.
```shell script
./ngrok http 1337 -host-header='localhost:1337'
```

### Notification using crontab
```shell script
$ crontab -e

# Noify users of food expiring in the next 3 days
0 8 * * * python manage.py notify_users
```


### Development

Uses the default Django development server.

1. Rename *.env.dev-sample* to *.env.dev*.
1. Update the environment variables in the *docker-compose.yml* and *.env.dev* files.
1. Build the images and run the containers:

    ```sh
    $ docker-compose up -d --build
    ```

    Test it out at [http://localhost:8000](http://localhost:8000). The "app" folder is mounted into the container and your code changes apply automatically.

### Production

Uses gunicorn + nginx.

1. Rename *.env.prod-sample* to *.env.prod* and *.env.prod.db-sample* to *.env.prod.db*. Update the environment variables.
1. Build the images and run the containers:

    ```sh
    $ docker-compose -f docker-compose.prod.yml up -d --build
    ```

    Test it out at [http://localhost:1337](http://localhost:1337). No mounted folders. To apply changes, the image must be re-built.


### Supplementary files
1. `hfg.ipynb` : Jupyter notebook for training the models
1. `telegram-bot/bot_script.py` : Script for the Telegram Bot 
1. `pushButtonToCapture.py` Script for Raspberry Pi + Camera
1.  [GroceryStoreDataset](https://github.com/marcusklasson/GroceryStoreDataset/tree/master/dataset/train)
