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

* ### Create driver <br/>

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


* ### Create client <br/>

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
    ```python
    {
        "driver": "14ec7cb3a5db4f5cbf643824e3ab636c",
        "fleet": "d89581bba49c41d4ab50c8d6eba14e45",
        "info": {
            "start": "{{start}}",
            "end": "{{end}}",
            "duration": {{duration}},
            "distance": 10
        },
        "data": {{data}}
    }
    ```

    **Response**
    > **uuid**: Driver UUID\
    > **name**: Driver name\
    > **drivers**: List with drivers uuid\
    > **fleets**: List with fleets uuid




