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
import pickle

account_sid = "ACdef11a02e9ad8742733e867273c87286"
auth_token = "e3de76780ef4f40d326f8480c67dc5c9"
my_twilio = "+15732791035"
API_Key='V955UXDHBY3A'

error = "Unregistered Number"
def twilioSMS(k,msg, count):

	try:
		pn = phonenumbers.parse(k)
		# print pn
		print pn.country_code
		country = pycountry.countries.get(alpha_2=region_code_for_number(pn))
		yo = region_code_for_country_code(pn.country_code)
		# print yo
		# print(country.name)
		# print country.code
		name = country.name
		pro=""
		url = "http://api.timezonedb.com/v2/list-time-zone?key=" + API_Key + "&format=json&country=" + yo
		# print url
		json_obj_places = urllib2.urlopen(url)
		places = json.load(json_obj_places)
		# print places
		print places["zones"][0]["zoneName"]

		local_date = datetime.now(pytz.timezone(places["zones"][0]["zoneName"]))  # use datetime here
		# print local_date.date()
		print local_date.time()
		# print type(local_date.time())


		hour = local_date.time().hour

		if hour in range(4, 7):
			client = Client(account_sid, auth_token)
			message = client.messages.create(to=k, from_=my_twilio, body=msg)

			time.sleep( 50 )
			print message.sid
			bappa = client.messages(message.sid).fetch()

			print(bappa.body)
			print(bappa.status)

			print "yoyo"
			l = k+".csv"
			print l

			if bappa.status not in ["delivered", "sent"] and count<5:
				print bappa.status
				count = count +1
				print count
				# print "hello"
				logging.basicConfig()
				time.sleep(2)
				obj = MessageLog(number=k, dateField=local_date.date(), timeField=local_date.time(), status="Failed or Undelivered")
				obj.save()
				# l = k+".csv"
				# print "before 20"
				# time.sleep(20)
				# print "after 20"
				# with open(l, 'a') as newfile:
				# 	newWriter = csv.writer(newfile)
				# 	newWriter.writerow([k, local_date.date(), local_date.time(), "Failed or Undelivered"])
				
				print "yoyo"
				time.sleep(5)
				twilioSMS(k,msg, count)	
		else:
			print "Night time"
			time.sleep(2)
			l = k+".csv"
			print l
			logging.basicConfig()
			obj = MessageLog(number=k, dateField=local_date.date(), timeField=local_date.time(), status="Night Time")
			print obj
			obj.save()
			# with open(l, 'a') as newfile:
			# 	newWriter = csv.writer(newfile)
			# 	newWriter.writerow([k, local_date.date(), local_date.time(), "Night Time"])
			print "bappa"
	except:
		print "error"


def sendSMS(request):
	if request.method == 'POST':
		code = request.POST.get('country_code')
		mobile_no = request.POST.get('mobile_no')
		msg = request.POST.get('msg')

		# print code
		# print mobile_no
		# p = str(code)
		# print type(p)
		# print type(mobile_no)
		k = code+mobile_no
		# print code+mobile_no

		if k in ['+919680848615', '+919462767891', '+919925100879']:
			scheduler = BackgroundScheduler()
			count = 0
			scheduler.add_job(twilioSMS, 'interval', minutes=10, args=(k,msg,count))
			print "bappa"
			scheduler.start()
			atexit.register(lambda: scheduler.shutdown(wait=False))

			l= k+".csv"
			print l
			# with open(l, "w") as initial:
			# 	firstWriter = csv.writer(initial)
			# 	firstWriter.writerow(["number", "dateField", "timeField", "status"])

			return HttpResponseRedirect(reverse('msgLogs', args=(str(k), )))

		else:
			return render(request, 'home.html', {'error':error})


def msgLogs(request, numb):
	logging.basicConfig()
	# l = numb + ".csv"
	# print l
	# reader = csv.DictReader(open(l, 'r'))
	# obj = []
	# for row in reader:
	# 	print "uuu"
	# 	obj.append(row)
	# print obj
	# # print "uuuuuu"
	err=0;
	# if len(obj)==0:
	# 	err = 1
	print "jjjj"
	obj = MessageLog.objects.filter(number=numb).order_by("-id")
	if len(obj) == 0:
		print "kkkk"
		err=1
	print "qqqqq"
	return render(request, 'logs.html', {'obj':obj, 'err':err})