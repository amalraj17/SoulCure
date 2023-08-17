from django.shortcuts import render
from django.contrib.auth import get_user_model

User = get_user_model
# Create your views here.
def index(request):
    return render(request,'index.html',{'user':request.user})