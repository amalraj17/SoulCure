from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect

from .models import Room, Message, UserRooms,Notifiction
from accounts.models import UserProfile
def notification(request):
    noti=Notifiction.objects.filter(user_id=request.user.id)
    print(noti)
    return render(request,'notification.html',{'notifications':noti})
@login_required
def rooms(request):
    rooms = Room.objects.all()
    ruser = request.user
    up = UserProfile.objects.get(user=ruser)

    # Filter UserRooms based on the current user
    userrooms = UserRooms.objects.filter(user=ruser)
    print(userrooms)

    return render(request, 'room/rooms.html', {'rooms': rooms, 'up': up,'userrooms':userrooms})


# @login_required
# def room(request, slug):
#     room = Room.objects.get(slug=slug)
#     messages = Message.objects.filter(room=room)
    
#     up = UserProfile.objects.all()
    
#     # print(list(messages)) [0:60]

#     return render(request, 'room/room.html', {'room': room, 'messages': messages,'up':up})
 
from django.utils import timezone
@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)

    cuser=request.user
    print(cuser)
    userroom_exists = UserRooms.objects.filter(user=cuser, room=room).exists()
    room_users=UserRooms.objects.filter(room=room)
    print("FUNCTION CALLED")
    for i in room_users:
            print("ROROOOOOROOM")
            obj=Notifiction(
                user_id=i.user_id,
                content=cuser.name+' messaged in the room '+room.name,
                time=timezone.now()
            )
            obj.save()
    if not userroom_exists:
        userroom = UserRooms(user=cuser, room=room, in_check=True)
        print("BEFORE SAVE")
        userroom.save()
        
        

    # Get the users who sent messages in the room
    users = [message.user for message in messages]

    # Fetch the corresponding UserProfile instances for the users
    user_profiles = UserProfile.objects.filter(user__in=users)

    # Create a dictionary to map user IDs to their respective profile pictures
    profile_picture_dict = {profile.user_id: profile.profile_picture for profile in user_profiles}

    # Attach profile picture URL to each message's user
    for message in messages:
        message.user.profile_picture = profile_picture_dict.get(message.user_id)

    # Print profile_picture_dict in the console
    print(profile_picture_dict)

    return render(request, 'room/room.html', {'room': room, 'messages': messages})

