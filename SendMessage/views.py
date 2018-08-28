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
import csv
import logging

account_sid = "--"
auth_token = "--"
my_twilio = "--"
API_Key='--'

error = "Unregistered Number"

def twilioSMS(k,msg, count):
	
	# To check for country code
	pn = phonenumbers.parse(k)
	print pn.country_code
	country = pycountry.countries.get(alpha_2=region_code_for_number(pn))
	yo = region_code_for_country_code(pn.country_code)
	
	# To get timezone for the specified country
	url = "http://api.timezonedb.com/v2/list-time-zone?key=" + API_Key + "&format=json&country=" + yo
	json_obj_places = urllib2.urlopen(url)
	places = json.load(json_obj_places)
	print places["zones"][0]["zoneName"]

	local_date = datetime.now(pytz.timezone(places["zones"][0]["zoneName"]))
	print local_date.time()

	hour = local_date.time().hour

	try:
		# To check whether the time is the night time or not
		if hour in range(7, 23):
			client = Client(account_sid, auth_token)
			message = client.messages.create(to=k, from_=my_twilio, body=msg)

			time.sleep( 60 )
			print message.sid
			bappa = client.messages(message.sid).fetch()

			print(bappa.body)
			print(bappa.status)

			# Checking the status of the Message after 1 minute if not delivered or sent, sending again
			if bappa.status not in ["delivered", "sent"] and count<5:
				print bappa.status
				count = count +1
				print count
				logging.basicConfig()
				time.sleep(2)
				obj = MessageLog(number=k, dateField=local_date.date(), timeField=local_date.time(), status="Failed or Undelivered")
				obj.save()
				print "yoyo"
				time.sleep(5)
				twilioSMS(k,msg, count)	
		else:
			#Saving to database in Night Time
			print "Night time"
			time.sleep(2)
			logging.basicConfig()
			obj = MessageLog(number=k, dateField=local_date.date(), timeField=local_date.time(), status="Night Time")
			print obj
			obj.save()
			print "bappa"
	except:
		# Checking if the number is invalid
		print "yo bappa"
		obj = MessageLog(number=k, dateField=local_date.date(), timeField=local_date.time(), status="Not Sent")
		obj.save()
		print "error"


def sendSMS(request):
	if request.method == 'POST':
		code = request.POST.get('country_code')
		mobile_no = request.POST.get('mobile_no')
		msg = request.POST.get('msg')

		print code
		print mobile_no
		k = code+mobile_no
		print k

		# Checking if number registered on Twilio or not and starting the Scheduler for every hour
		if k in ['--', '--', '--']:
			scheduler = BackgroundScheduler()
			count = 0
			scheduler.add_job(twilioSMS, 'interval', minutes=60, args=(k,msg,count))
			print "bappa"
			scheduler.start()
			atexit.register(lambda: scheduler.shutdown(wait=False))
			# Atexit for stopping the Scheduler

			return HttpResponseRedirect(reverse('msgLogs', args=(str(k), )))

		else:
			return render(request, 'home.html', {'error':error})

# Function for Message logs
def msgLogs(request, numb):
	logging.basicConfig()
	err=0;
	print "test"
	obj = MessageLog.objects.filter(number=numb).order_by("-id")
	if len(obj) == 0:
		print "test2"
		err=1
	print "test3"
	return render(request, 'logs.html', {'obj':obj, 'err':err})
