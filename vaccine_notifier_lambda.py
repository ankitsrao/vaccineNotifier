import base64
import json
import os
import urllib
from urllib import request, parse
import requests
from datetime import datetime, timedelta

def lambda_handler(event, context):
    date=(datetime.today()+timedelta(hours=6)).strftime('%d-%m-%Y') #Adding 6 hours so that Lambda considers the Indian local time for computation
    
    notificationmap=[ {
                      "districtCode": xxx,
                      "phone": ["xxx", "xxx", ...],
                      "block_name" : "xxx"
                  } ]
    
    TWILIO_SMS_URL = "https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json"
    TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
    
    # insert Twilio Account SID into the REST API URL
    TWILIO_URL = TWILIO_SMS_URL.format(TWILIO_ACCOUNT_SID)
    
    for node in notificationmap:
        url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=%s&date=%s" % (node['districtCode'], date)
    
        print("Vaccine finder URL: "+ url)
        response = requests.request("GET", url)
        response_data=json.loads(response.content)
    
        center_data=response_data['centers']
        vaccine_data=[]
    
        for center in center_data:
            sessions = center['sessions']
            for session in sessions:
                if session['min_age_limit'] == 18 and session['available_capacity'] > 0 and center['block_name'] == node['block_name']:
                    availabilty_details = {
                                                "Center Name" : center['name'],
                                                "Pincode" : center['pincode'],
                                                "Availabilty Date" : session['date'],
                                                "Available Capacity" : session['available_capacity']
                                            }
                    vaccine_data.append(availabilty_details)
    
        print("Vaccine info: ")
    
        print(json.dumps(vaccine_data, indent=2, sort_keys=False))
    
        if vaccine_data:
            for number in node['phone']:
                post_params = {"To": number, "From": "+13475149515", "Body": json.dumps(vaccine_data, indent=2, sort_keys=False)}
    
                data = parse.urlencode(post_params).encode()
                TWILIO_REQUEST = request.Request(TWILIO_URL)
            
                # add authentication header to request based on Account SID + Auth Token
                authentication = "{}:{}".format(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                base64string = base64.b64encode(authentication.encode('utf-8'))
                TWILIO_REQUEST.add_header("Authorization", "Basic %s" % base64string.decode('ascii'))
            
                try:
                    # perform HTTP POST request
                    with request.urlopen(TWILIO_REQUEST, data) as f:
                        print("Twilio returned {}".format(str(f.read().decode('utf-8'))))
                        print("Successfully notified: "+ str(number))
                except Exception as e:
                    print("Error while sending SMS: "+str(e))
