import requests


def send_sms(mobile, message):
    url = "http://msg.msgclub.net/rest/services/sendSMS/sendGroupSms"
    params = {
        'AUTH_KEY': '3380567192fd2e6d18f63985aace',
        'message': message,
        'senderId': 'MRCARC',
        'routeId': 1,
        'mobileNos': mobile,
        'smsContentType': 'english'
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()  # Parse the JSON response to a Python dict
        response_code = data.get('responseCode')
        response_value = data.get('response')

        # Now you can use the values
        print("Response Code:", response_code)
        print("Response:", response_value)
    else:
        print("Failed to send SMS", response.text)
