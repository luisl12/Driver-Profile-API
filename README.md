# Driver-Profile-API
Driver Profile REST API

Pre-Requisites
--------------

Working Python 3 installation (Python version = 3.9), with the pipenv package previously installed.


Running the API
-------------------

1. Create virtual environment (if not already created).
    * Use "pipenv shell".
2. Activate virtual environment.
    * Use "pipenv shell".
3. Install requirements.
    * Use "pipenv install".
4. Run the API.
    * Make sure you have the database configured.
    * Make sure you have the environment variables configured as in the ".env.template" file, in a ".env" file.
    * Use "python wsgi.py".


Endpoints
-------------------

* ### Create driver

    **Endpoint**\
    [POST]
    /drivers

    **Headers**\
    Content-Type: application/json

    **Body**
    > **name**: Driver name

    **Response**
    > **uuid**: Driver UUID\
    > **name**: Driver name


* ### Create client

    **Endpoint**\
    [POST]
    /clients

    **Headers**\
    Content-Type: application/json

    **Body**
    > **client**: Client name\
    > **fleets**: List with fleet names

    **Response**
    > **uuid**: Driver UUID\
    > **name**: Driver name\
    > **drivers**: List with drivers uuid\
    > **fleets**: List with fleets uuid


* ### Create trip

    **Endpoint**\
    [POST]
    /trips

    **Headers**\
    Content-Type: application/json

    **Body**
    > **driver**: Client name\
    > **fleet**: List with fleet names\
    > **info**:{
    >> **start**:\
    >> **start**:\
    >> **start**:\
    >> **start**:\
    }\
    **data**:

    **Response**
    > **uuid**: Driver UUID\
    > **name**: Driver name\
    > **drivers**: List with drivers uuid\
    > **fleets**: List with fleets uuid




