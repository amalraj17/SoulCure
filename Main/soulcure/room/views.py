from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect

from .models import Room, Message, UserRooms,Notification
from accounts.models import UserProfile


@login_required
def rooms(request):
    rooms = Room.objects.all()
    ruser = request.user
    up = UserProfile.objects.get(user=ruser)
    userrooms = UserRooms.objects.filter(user=ruser)
    print(userrooms)
    return render(request, 'room/rooms.html', {'rooms': rooms, 'up': up,'userrooms':userrooms})

from django.utils import timezone
# from django.utils.text import slugify  # Import slugify

@login_required
def room(request, slug):
    # Slugify the room name
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)
    cuser=request.user
    print(cuser)
    userroom_exists = UserRooms.objects.filter(user=cuser, room=room).exists()
    room_users=UserRooms.objects.filter(room=room)

    for p in room_users:
        print(p)
    for i in room_users:
        obj=Notification(
            user_id=i.user_id,
            room=room,
            content=cuser.name+' messaged in the room '+room.name,
            time=timezone.now()
        )
        obj.save()
    if not userroom_exists:
        userroom = UserRooms(user=cuser, room=room, in_check=True)
        userroom.save()
        
    users = [message.user for message in messages]
    user_profiles = UserProfile.objects.filter(user__in=users)
    profile_picture_dict = {profile.user_id: profile.profile_picture for profile in user_profiles}

    for message in messages:
        message.user.profile_picture = profile_picture_dict.get(message.user_id)

    return render(request, 'room/room.html', {'room': room, 'messages': messages})


# @login_required
# def room(request, slug):
    
#     room = Room.objects.get(slug=slug)
#     messages = Message.objects.filter(room=room)

#     users = [message.user for message in messages]
#     user_profiles = UserProfile.objects.filter(user__in=users)
#     profile_picture_dict = {profile.user_id: profile.profile_picture for profile in user_profiles}

#     for message in messages:
#         message.user.profile_picture = profile_picture_dict.get(message.user_id)

#     return render(request, 'room/room.html', {'room': room, 'messages': messages})

# @login_required
# def notification(request):
#     noti = Notification.objects.get(user_id=request.user.id)
#     print(noti)
#     return render(request,'notification.html',{'notifications':noti})




@login_required
def notification(request,room_slug):
    room = Room.objects.get(slug=room_slug)
    try:
        # Retrieve notifications sent by other users (excluding the current user)
        # noti = Notification.objects.exclude(user=request.user).order_by('-time')[:10]
        notifications = Notification.objects.filter(room=room, user=request.user, status=True)
    except IndexError:
        # Handle the case where no notification is found
        noti = None
    
    print(noti)
    return render(request, 'notification.html', {'notifications': noti,'room': room})

@login_required
def mark_notifications_as_read(request):
    if request.method == 'POST':
        noti = Notification.objects.exclude(user=request.user)
        for i in noti:
            i.status = False
            i.save()

    return redirect('notification')
