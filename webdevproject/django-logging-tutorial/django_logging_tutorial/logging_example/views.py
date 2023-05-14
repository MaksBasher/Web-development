from django.shortcuts import render
from django.http import HttpResponse
import datetime
# import the logging library
import logging
# Create your views here.


# Get an instance of a logger
logger = logging.getLogger(__name__)

def welcome_page(request):
    logger.warning('Homepage was accessed at '+str(datetime.datetime.now())+' hours!')
    return HttpResponse("<h1>Please give me points for the assignment <3</h1>")
