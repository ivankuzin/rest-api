    How to run:
1. Install Python3
2. "cd rest-api"
3. "pip install pipenv"
4. "pipenv install"
5. "pipenv shell"
6. "python iapi.py"

    Endpoint:
Base URL:
http://127.0.0.1:5000/

Resource:
GET     /dealers                - Receives a list of all dealers from database
POST    /dealers                - Addes dealer to database
PUT     /dealers/{dealer_id}    - Change dealer data with dealer_id
DELETE  /dealers/{dealer_id}    - Delete dealer data with dealer_id
GET     /cars                   - Receives a list of all cars from database
POST    /cars                   - Addes car to database
PUT     /cars/{cars_id}         - Change car data with car_id
DELETE  /cars/{cars_id}         - Delete car data with car_id e.g. car was bought (my TS)
GET     /cars/{brand}           - Receives a list of cars with the specific brand from database
GET     /cars/{brand}/{model    - Receives a list of cars with the specific brand and model from database
GET     /dealers/{dealer_id}    - Receives a list of all cars owned by specific dealer

You can also find two json_schema for both dealer and car response.