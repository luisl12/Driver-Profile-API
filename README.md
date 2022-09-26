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
    ```python
    {
        "name": <str>,  # Driver name
    }
    ```

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
    ```python
    {
        "client": <str>,  # Client name
        "fleets": <list>,  # List with fleet names
    }
    ```

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
        "driver": <str>,
        "fleet": <str>,
        "info": {
            "start": <str>,
            "end": <str>,
            "duration": <float>,
            "distance": <float>
        },
        "idreams_uuid": <str, optional>,
        "data": {
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
    > **uuid**: Driver UUID\
    > **name**: Driver name\
    > **drivers**: List with drivers uuid\
    > **fleets**: List with fleets uuid




