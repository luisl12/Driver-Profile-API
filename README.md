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
    * Make sure you have the database configured (you only need to create the database, the models are created automatically).
    * Make sure you have the environment variables configured as in the ".env.template" file, in a ".env" file.
    * Use "python wsgi.py" to run the API.


Endpoints
-------------------

<details>
<summary><h3>Create driver</h3></summary>

**Endpoint**\
[POST]
/drivers

**Headers**\
Content-Type: application/json

**Body**
```python
{
    "name": <str>,  # Driver name
}
```

**Response**
```python
{
    "uuid": <str>,  # Driver UUID
    "name": <str>,  # Driver name
}
```
</details>


* ### Create client

    **Endpoint**\
    [POST]
    /clients

    **Headers**\
    Content-Type: application/json

    **Body**
    ```python
    {
        "client": <str>,  # Client name
        "fleets": <list>,  # List with fleet names
    }
    ```

    **Response**
    ```python
    {
        "uuid": <str>,  # Driver UUID
        "name": <str>,  # Driver name
        "drivers": <list>,  # List with drivers uuid
        "fleets": <list>,  # List with fleets uuid
    }
    ```


* ### Create trip

    **Endpoint**\
    [POST]
    /trips

    **Headers**\
    Content-Type: application/json

    **Body**
    ```python
    {
        "driver": <str>,  # Driver UUID
        "fleet": <str>,  # Fleet UUID
        "info": {  # Trip info
            "start": <str>,  # Trip start datetime in ISO format
            "end": <str>,  # Trip end datetime in ISO format
            "duration": <float>,  # Trip duration in seconds
            "distance": <float>  # Trip distance in km
        },
        "idreams_uuid": <str>,  # i-DREAMS trip UUID, required if "data" is None
        "data": {  # Trip data, required if "idreams_uuid" is None
            "n_ha": <int>,
            "n_ha_l": <int>,
            "n_ha_m": <int>,
            "n_ha_h": <int>,
            "n_hb": <int>,
            "n_hb_l": <int>,
            "n_hb_m": <int>,
            "n_hb_h": <int>,
            "n_hc": <int>,
            "n_hc_l": <int>,
            "n_hc_m": <int>,
            "n_hc_h": <int>,
            "fcw_time": <int>,
            "hmw_time": <int>,
            "ldw_time": <int>,
            "pcw_time": <int>,
            "n_pedestrian_dz": <int>,
            "n_tsr_level": <int>,
            "n_tsr_level_0": <int>,
            "n_tsr_level_1": <int>,
            "n_tsr_level_2": <int>,
            "n_tsr_level_3": <int>,
            "n_tsr_level_4": <int>,
            "n_tsr_level_5": <int>,
            "n_tsr_level_6": <int>,
            "n_tsr_level_7": <int>,
            "n_brakes": <int>,
            "speed": <int>,
            "n_fcw": <int>,
            "n_hmw": <int>,
            "n_ldw": <int>,
            "n_ldw_left": <int>,
            "n_ldw_right": <int>,
            "n_pcw": <int>,
            "n_fatigue_0": <int>,
            "n_fatigue_1": <int>,
            "n_fatigue_2": <int>,
            "n_fatigue_3": <int>,
            "n_headway__1": <int>,
            "n_headway_0": <int>,
            "n_headway_1": <int>,
            "n_headway_2": <int>,
            "n_headway_3": <int>,
            "n_overtaking_0": <int>,
            "n_overtaking_1": <int>,
            "n_overtaking_2": <int>,
            "n_overtaking_3": <int>,
            "n_speeding_0": <int>,
            "n_speeding_1": <int>,
            "n_speeding_2": <int>,
            "n_speeding_3": <int>
        }
    }
    ```

    **Response**
    ```python
    {
        "uuid": <str>,  # Trip UUID
        "start": <str>,  # Trip start datetime in ISO format
        "end": <str>,  # Trip end datetime in ISO format
        "duration": <float>,  # Trip duration in seconds
        "distance": <float>  # Trip distance in km
        "profile": <str>  # Trip profile
        "fleet": <str>  # Fleet UUID
    }
    ```


* ### Get clients

    **Endpoint**\
    [GET]
    /clients

    **Response**
    ```python
    # List of all clients
    [
       {
        'uuid': <str>,  # Client UUID
        'name': <str>,  # Client name
        'drivers': <list>,  # List of client drivers UUID
        'fleets': <list>  # List of client fleets UUID
       }
       ...
    ]
    ```

* ### Get drivers

    **Endpoint**\
    [GET]
    /drivers

    **Response**
    ```python
    # List of all drivers
    [
       {
        'client': <str>,  # Client UUID
        'name': <str>,  # Driver name
        'uuid': <str>,  # Driver UUID
       }
       ...
    ]
    ```


* ### Get driver trips

    **Endpoint**\
    [GET]
    /drivers/<uuid>/trips

    **Response**
    ```python
    # List of all driver trips
    [
       {
        "uuid": <str>,  # Trip UUID
        "start": <str>,  # Trip start datetime in ISO format
        "end": <str>,  # Trip end datetime in ISO format
        "duration": <float>,  # Trip duration in seconds
        "distance": <float>  # Trip distance in km
        "profile": <str>  # Trip profile
        "fleet": <str>  # Fleet UUID
        }
       ...
    ]
    ```


* ### Get fleet trips

    **Endpoint**\
    [GET]
    /clients/<uuid>/fleets/<uuid>/trips

    **Response**
    ```python
    # List of all client fleet trips
    [
       {
        "uuid": <str>,  # Trip UUID
        "start": <str>,  # Trip start datetime in ISO format
        "end": <str>,  # Trip end datetime in ISO format
        "duration": <float>,  # Trip duration in seconds
        "distance": <float>  # Trip distance in km
        "profile": <str>  # Trip profile
        "fleet": <str>  # Fleet UUID
        }
       ...
    ]
    ```

