# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import MessageLog

# Register your models here.
class MessageLogData(admin.ModelAdmin):
	list_display = ('number', 'dateField', 'timeField', 'status')

admin.site.register(MessageLog, MessageLogData)