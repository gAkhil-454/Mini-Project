#! /usr/bin/python

# Imports
import requests

def send_simple_message():
	return requests.post(
		"https://api.mailgun.net/v3/sandboxf0768c693bb647ab89629b73c75fbf22.mailgun.org/messages",
		auth=("api", "d983be43b6b16fbd5bc2001be571c09a-30344472-f9b16d3c"),
		files =[ ("attachment", ("image.jpg", open("image.jpg", "rb").read()))],
		data = {"from": "Mailgun Sandbox <postmaster@sandboxf0768c693bb647ab89629b73c75fbf22.mailgun.org>",
            "to": "Akhil <drstrange5940@gmail.com>",
            "subject": "Some one is there at your doorstep!!",
            "text":    " " + "If you want to permit , you have 30 seconds . Navigate to your Blynk app andd proceed!"})
                      
request = send_simple_message()
print ('Status: '+format(request.status_code))
print ('Body:'+ format(request.text))
