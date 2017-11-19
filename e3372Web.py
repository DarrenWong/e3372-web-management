#!/usr/bin/python
#coding:utf-8
from flask import Flask, render_template, jsonify, request
import sys
import pprint
import requests
import xmltodict
import json
import time
import logging
import traceback
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('logs/configlog.log', maxBytes=2000, backupCount=5)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class CustomFlask(Flask):   # custom the flask var as {#var#}
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='{%',
        block_end_string='%}',
        variable_start_string='{#',
        variable_end_string='#}',
        comment_start_string='<#',
        comment_end_string='#>',
    ))

#app = Flask(__name__)
app = CustomFlask(__name__)

class HuaweiE3372(object):
  BASE_URL = 'http://{host}'
  COOKIE_URL = '/html/index.html'
  XML_APIS = [
    '/api/monitoring/converged-status',
    '/api/device/basic_information',
    '/api/device/information',
    '/api/device/signal',
    '/api/net/net-mode',
    # below API would refer to refresh periodly 
    '/api/monitoring/status',
    '/api/monitoring/check-notifications',
    '/api/monitoring/traffic-statistics',
    '/api/dialup/mobile-dataswitch',
    '/api/monitoring/traffic-statistics',
    '/api/net/current-plmn',
  ]
  session = None
  
  def __init__(self,host='192.168.8.1'):
    self.host = host
    self.base_url = self.BASE_URL.format(host=host)
    self.session = requests.Session()
    r = self.session.get(self.base_url + self.COOKIE_URL)

  def get(self,path):
    return xmltodict.parse(self.session.get(self.base_url + path).text).get('response',None)

  def postSMS(self, path, number, text):
    SessionToken = xmltodict.parse(self.session.get(self.base_url + "/api/webserver/SesTokInfo").text).get('response', None)
    APIurl = self.base_url + path
    if SessionToken is not None:
      Session = SessionToken.get("SesInfo")  # cookie
      Token = SessionToken.get("TokInfo")  # token
      headers = {'Cookie': Session, '__RequestVerificationToken': Token, "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    else:
      Token = xmltodict.parse(self.session.get(self.base_url + "/api/webserver/token").text).get('response', None).get("token")
      headers = {'__RequestVerificationToken': Token, "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}

    Length = str(len(text))  # text length
    post_data = "<request><Index>-1</Index><Phones><Phone>" + number + "</Phone></Phones><Sca></Sca><Content>" + text + "</Content><Length>" + Length + "</Length><Reserved>1</Reserved><Date>-1</Date></request>"
    logging.debug(post_data)
    return xmltodict.parse(self.session.post(url=APIurl, data=post_data, headers=headers).text)

  def postdataswitch(self,path,dataswitch):
    SessionToken = xmltodict.parse(self.session.get(self.base_url + "/api/webserver/SesTokInfo").text).get('response',None)
    APIurl = self.base_url + path
    Session = SessionToken.get("SesInfo")  #cookie
    Token = SessionToken.get("TokInfo") #token
    headers = {'Cookie': Session, '__RequestVerificationToken':Token, "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}
    post_data = "<request><dataswitch>"+dataswitch+"</dataswitch>"
    print post_data   
    return xmltodict.parse(self.session.post(url=APIurl, data= post_data,headers=headers).text)

@app.route("/")
def mainpage():  
    try:
        return render_template('index.html', updatetime = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    except:
        logger.error("Render mainpage failed")  
        return "error"

@app.route('/getdata', methods=['GET'])  #API data return as json
def getAPIdata():
    try:
        e3372 = HuaweiE3372()
        dict = {}
        for path in e3372.XML_APIS:
            for key,value in e3372.get(path).items():
                if  (value):
                    dict[key]=value
        logger.info("Get dongle data successful")
        return jsonify(**dict)
    except:
        logger.error("Get dongole data failed")  
        return "Unknown error"

@app.route('/sendsms', methods=['POST']) #send Message using POST
def sendsms():
    jsonData =  request.data
    dataDict = json.loads(jsonData)
    try:
        e3372 = HuaweiE3372()
        name = dataDict['number']
        text = dataDict['SMStext']
        test = e3372.postSMS("/api/sms/send-sms", name,text).get('response')
        logger.info("Sent Message")
        return "Message status: %s" %test
    except: 
        logger.error("Send Message failed")  
        return "Unknown error"

@app.route('/dataswitch', methods=['POST']) # mobile data on or off using POST 
def dataswitch():   
    jsonData =  request.data
    dataDict = json.loads(jsonData)
    try:
        dataswitch = dataDict['dataswitch']
        e3372 = HuaweiE3372()
        test = e3372.postdataswitch("/api/dialup/mobile-dataswitch",dataswitch).get('response',None)
        logger.info("Data switched")
        return "Dataswitch status: %s" %test
    except: 
        logger.error("data switch failed")  
        return "Unknown error"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
