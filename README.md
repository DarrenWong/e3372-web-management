# E3372-Web-Management
------------
Getting E3372 device information using Python Flask and AngularJs. It can display the status of Networks and post dataswtich and send sms under the Python REST interface. Tested in Raspberry Pi 3 with JESSIE Release date:2017-01-11 and Mac OS 10.12

Installation
------------
Need to install a few python modules like flask, requests, xmltodict, json using pip. Have tested in the Raspberry Pi3 with RASPBIAN JESSIE Release date:2017-01-11 that only need to install the xmltodict.

```Shell
$ pip install xmltodict
```

Basic Usage
-----------

```Python
python e3372Web.py

```
Open your browser and it is running on http://0.0.0.0:8000/


Note
-----------
Forked from https://github.com/arska/e3372, and the js template refer to the AngularJS phone's tutorials(https://github.com/angular/angular-phonecat). Enjoy and any improvements are welcome.

