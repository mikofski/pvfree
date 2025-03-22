[![test_pvfree](https://github.com/BreakingBytes/pvfree/actions/workflows/test_pvfree.yml/badge.svg?branch=main&event=push)](https://github.com/BreakingBytes/pvfree/actions/workflows/test_pvfree.yml)

PV Free
=======
A public API for PV modeling parameters and pvlib API for learning about solar.

Announcements
-------------
_2025-03-22_: Now that ElephantSQL has reached its end-of-life, and the Aiven migration is working as expected, the dev website deployed
at AlwaysData has been terminated. Please use https://pvfree.azurewebsites.net/ only.

Hosting
-------
pvfree is hosted at [Microsoft Azure Cloud App service](https://azure.microsoft.com/en-us/products/app-service/).
Please use https://pvfree.azurewebsites.net/ to get module and inverter parameters for pvlib and to learn about solar energy modeling.

The pvfree database is hosted at [Aiven](https://aiven.io/) using PostgreSQL.

Contributing
------------
The `pytest.ini` file is set to run using `DJANGO.SETTINGS_MODULE=pvfree.settings.dev` and find all tests automatically,
to allow you to use just the `pytest` command instead of `python manage.py test testdir --settings pvfree.settings.dev`.

Usage
-----
Browsing to
[`pvfree.azurewebsites.net/api/v1/pvinverter/`](https://pvfree.azurewebsites.net/api/v1/pvinverter/?format=json)
will display a JSON string with the first 20 records. The endpoint and query
string to obtain the next set
[`api/pvinverter/?limit=20&offset=20`](https://pvfree.azurewebsites.net/api/v1/pvinverter/?format=json&limit=20&offset=20)
is contained in the `next` key of the string as are the endpoints for each
inverter. Note: the query string `?format=json` is only necessary when using the API url directly in a browser to display the response.

[Tastypie](https://django-tastypie.readthedocs.org/en/latest/)
--------------------------------------------------------------
The API is generated by the Tastypie django extension. Add the following endpoints to the base URL, [`https://pvfree.azurewebsites.net/`](https://pvfree.azurewebsites.net/):

* Get first 20 pvinverters.

        api/pvinverter/

* Get first pvinverter.

        api/pvinverter/1/

* Get pvinverter set containing #'s 2, 3, 5, and 10.

        api/pvinverter/set/2;3;5;10/

* Get 100 pvinverters starting from pvinverter # 500.

        api/pvinverter/?limit=100&offset=500

* Get pvinverter database schema.

        api/pvinverter/schema/

[Python Requests](https://requests.readthedocs.io/en/master/)
-------------------------------------------------------------
Python has several libraries for interacting with URLs. The Requests package is available from [PyPI](https://pypi.python.org/pypi/requests).

```python
>>> import requests
>>> response = requests.get('https://pvfree.azurewebsites.net/api/v1/pvinverter/set/1;3;5/')
>>> response
  <Response [200]>
>>> response.status_code
  200
>>> response.content
  {"objects": [{"C0": -2.48104842861e-05, "C1": -9.0149429405099999e-05, "C2": 0.00066889632690700005, "C3": -0.018880466688599998, "Idcmax": 10.0, "MPPT_hi": 50.0, "MPPT_low": 20.0, "Paco": 250.0, "Pdco": 259.52205054799998, "Pnt": 0.02, "Pso": 1.7716142241299999, "Sandia_ID": 1399, "Tamb_low": -40.0, "Tamb_max": 85.0, "Vaco": 208.0, "Vdcmax": 65.0, "Vdco": 40.242603174599999, "id": 1, "manufacturer": "ABB", "name": "MICRO-0.25-I-OUTD-US-208", "numberMPPTChannels": 1, "resource_uri": "/api/v1/pvinverter/1/", "source": "CEC", "vintage": "2014-01-01", "weight": 1.6499999999999999}, ...]}
```
