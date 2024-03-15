from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def dashboard(request):
    return render(request, 'joinroom.html', {'name': request.user.name})

@login_required
def videocall(request):
    call_view = True
    session_id = request.GET.get('session_id')
    print(session_id)
    return render(request, 'videocall.html', {'name': request.user.name, 'session_id': session_id })



@login_required
def join_room(request):
    if request.method == 'POST':
        roomID = request.POST['roomID']
        return redirect("/chat/meeting/?roomID=" + roomID)
    return render(request, 'joinroom.html')


