import requests
import json
from twilio.rest import Client
from datetime import datetime

date=datetime.today().strftime('%d-%m-%Y')

notificationmap=[ 
                {
                    "districtCode": xxx,
                    "phone": ["xxx", "xxx", ...],
                    "block_name" : "xxx"
                } ]

account_sid='xxxx'
auth_token='xxxx'

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

    print("Vaccine info: " + str(vaccine_data))

    print(json.dumps(vaccine_data, indent=2, sort_keys=False))

    if vaccine_data:
        client = Client(account_sid, auth_token)
        try:
            for number in node['phone']: 
                message = client.messages.create(to=number, from_="+13475149515", body=json.dumps(vaccine_data, indent=2, sort_keys=False))
                print("Successfully notified: "+ str(number) + " " + str(print(message.sid)))
        except Exception as e:
            print("Error while sending SMS: "+str(e))
