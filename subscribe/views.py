from django.shortcuts import render
import logging

def subscribe(request):
	return render(request, "subscribe.html")

def about(request):
	return render(request, "about.html")