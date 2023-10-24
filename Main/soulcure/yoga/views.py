from django.shortcuts import render

# Create your views here.
def yoga_page(request):
    return render(request, 'yoga.html')