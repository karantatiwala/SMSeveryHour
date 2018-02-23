# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
import pycountry
import phonenumbers
from phonenumbers.phonenumberutil import region_code_for_country_code
from phonenumbers.phonenumberutil import region_code_for_number
from geopy import geocoders
import pytz
from datetime import datetime
from twilio.rest import Client
import time
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import urllib2
import json
from phonenumbers.phonenumberutil import region_code_for_country_code
from models import MessageLog

account_sid = "ACdef11a02e9ad8742733e867273c87286"
auth_token = "e3de76780ef4f40d326f8480c67dc5c9"
# my_cell = "+919680848615"
my_twilio = "+15732791035"
API_Key='V955UXDHBY3A'
# count = 0
error = "Unregistered Number"
def twilioSMS(k,msg, count):

	try:
		pn = phonenumbers.parse(k)
		print pn
		print pn.country_code
		country = pycountry.countries.get(alpha_2=region_code_for_number(pn))
		yo = region_code_for_country_code(pn.country_code)
		print yo
		print(country.name)
		# print country.code
		name = country.name
		pro=""
		url = "http://api.timezonedb.com/v2/list-time-zone?key=" + API_Key + "&format=json&country=" + yo
		print url
		json_obj_places = urllib2.urlopen(url)
		places = json.load(json_obj_places)
		print places
		print places["zones"][0]["zoneName"]

		local_date = datetime.now(pytz.timezone(places["zones"][0]["zoneName"]))  # use datetime here
		print local_date.date()
		print local_date.time()
		print type(local_date.time())


		hour = local_date.time().hour

		if hour in range(7, 23):
			client = Client(account_sid, auth_token)

			my_msg = "Hello your name is KARAN..Please remember it"

			message = client.messages.create(to=k, from_=my_twilio, body=msg)

			time.sleep( 60 )
			print message.sid
			bappa = client.messages(message.sid).fetch()

			print(bappa.body)
			print(bappa.status)

			print "yoyo"
			# print count+1

			if bappa.status not in ["delivered"] and count<5:
				count = count +1
				print count
				print "hello"
				obj = MessageLog(number=k, dateField=local_date.date(), timeField=local_date.time(), status="Failed or Undelivered")
				obj.save()
				# enter databse
				twilioSMS(k,msg, count)	
		else:
			print "Night time"
			obj = MessageLog(number=k, dateField=local_date.date(), timeField=local_date.time(), status="Night Time")
			obj.save()
	except:
	# 	# time.sleep(2) #some error
	# 	# twilioSMS(k,msg)
		print "error"
		# pass

# Create your views here.
def sendSMS(request):
	if request.method == 'POST':
		code = request.POST.get('country_code')
		mobile_no = request.POST.get('mobile_no')
		msg = request.POST.get('msg')

		print code
		print mobile_no
		p = str(code)
		print type(p)
		print type(mobile_no)
		k = code+mobile_no
		print code+mobile_no

		if k in ['+919680848615', '+919462767891']:
			
			# twilioSMS(k,msg)
			scheduler = BackgroundScheduler()
			count = 0
			scheduler.add_job(twilioSMS, 'interval', minutes=60, args=(k,msg,count))
			scheduler.start()
			atexit.register(lambda: scheduler.shutdown(wait=False))
			# twilioSMS(k,msg, count)
			# obj = MessageLog.objects.filter(number=k)

			# return render(request, 'home.html', {'obj':obj})
			return HttpResponseRedirect(reverse('msgLogs', args=(str(k), )))

		else:
			return render(request, 'home.html', {'error':error})


def msgLogs(request, numb):
	obj = MessageLog.objects.filter(number=numb)
	return render(request, 'logs.html', {'obj':obj})