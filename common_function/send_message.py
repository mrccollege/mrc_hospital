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
        print("SMS sent successfully!")
    else:
        print("Failed to send SMS", response.text)
