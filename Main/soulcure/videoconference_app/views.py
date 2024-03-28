from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from therapist.models import TherapySessionSchedule
from client.models import Appointment
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
# from datetime import time
from datetime import datetime, timedelta
# from date import date

# Create your views here.

@login_required
def dashboard(request):
    room_id = request.GET.get('roomID')
    return render(request, 'joinroom.html', {'name': request.user.name})

@login_required
def videocall(request):
    call_view = True
    session_id = request.GET.get('session_id')
    # print(session_id)
    return render(request, 'videocall.html', {'name': request.user.name, 'session_id': session_id })

@login_required
def videocallclient(request):
    return render(request, 'videocallclient.html', {'name': request.user.name })


# @login_required
# def join_room(request,roomID,appointment_id):
#     appointment_id = appointment_id
#     if request.user.is_authenticated:
#         current_schedule = TherapySessionSchedule.objects.get(appointment_id=appointment_id)

#         print(current_schedule)
#         if current_schedule.appointment.client == request.user:
#             current_time1 = datetime.now().time()
#             current_time = datetime.now().strftime('%I:%M %p')
#             current_date = datetime.now().date()
#             print(current_date)
#             print(current_time) 
#             one_hour_later = (datetime.combine(datetime.today(), current_time1) + timedelta(hours=1)).time()            
#             one_hour_later_str = one_hour_later.strftime('%I:%M %p')
#             print(one_hour_later,"one hr later",one_hour_later_str,"one hr later str")
#             current_appointment = Appointment.objects.get(id=appointment_id)
#             appo_date=current_appointment.date
#             print(appo_date)
#             appo_time=current_appointment.time_slot
#             appointment =current_appointment
#             print(appo_date,appo_time)
#             if appointment.date == current_date:
#                 appointment_time = appointment.time_slot
#                 if appointment_time > current_time and appointment_time <= one_hour_later:               
#                     value = str(roomID)
#                     print(value)
#                     if value:
#                         return redirect("/chat/meeting/client/?roomID=" + value)
#                 else:
#                     msg = "Meeting is not scheduled yet"
#                     return HttpResponse(loader.render_to_string('client/view-schedule-ag.html', {'message': msg,'current_schedule':current_schedule,'appointment':appointment}))
#             else:
#                 msg = "Meeting is not scheduled yet"
#                 return HttpResponse(loader.render_to_string('client/view-schedule-ag.html', {'message': msg,'current_schedule':current_schedule,'appointment':appointment}))
#         else:
#             msg = "You are not authorized to join this meeting"
#             return HttpResponse(loader.render_to_string('client/view-schedule-ag.html', {'message': msg,'current_schedule':current_schedule,'appointment':appointment}))
#     else:
#         return redirect('login')




# @login_required
# def join_room(request, roomID, appointment_id):
#     if request.user.is_authenticated:
#         current_schedule = TherapySessionSchedule.objects.get(appointment_id=appointment_id)
#         print(current_schedule)

#         if current_schedule.appointment.client == request.user:
#             current_time = datetime.now().strftime('%I:%M %p')
#             # current_time1 = datetime.now()
#             current_date = datetime.now().date()
#             print(current_date, current_time) 
#             # time_less_10_mins = current_time1 - timedelta(minutes=10)
#             # time_less_10_mins_str = time_less_10_mins.strftime('%I:%M %p')
#             # print(time_less_10_mins_str)
#             one_hour_later = (datetime.combine(datetime.today(), datetime.now().time()) + timedelta(hours=1)).strftime('%I:%M %p')
#             print(one_hour_later)

#             current_appointment = Appointment.objects.get(id=appointment_id)
#             appo_date = current_appointment.date
#             appo_time = current_appointment.time_slot.strftime('%I:%M %p')
#             appointment = current_appointment
#             print(appo_date, appo_time)

#             if appo_date == current_date:
#                 print("checking date")
#                 if appo_time < current_time and appo_time <= one_hour_later:
#                 # if appo_time > current_time : 
#                     print("checking time")              
#                     value = str(roomID)
#                     print(value)
#                     if value:
#                         return redirect("/chat/meeting/client/?roomID=" + value)
#                 else:
#                     msg = "Meeting is not scheduled yet"
#                     return HttpResponse(loader.render_to_string('client/view-schedule-ag.html', {'message': msg, 'current_schedule': current_schedule, 'appointment': appointment}))
#             else:
#                 msg = "Meeting is not scheduled yet"
#                 return HttpResponse(loader.render_to_string('client/view-schedule-ag.html', {'message': msg, 'current_schedule': current_schedule, 'appointment': appointment}))
#         else:
#             msg = "You are not authorized to join this meeting"
#             return HttpResponse(loader.render_to_string('client/view-schedule-ag.html', {'message': msg, 'current_schedule': current_schedule, 'appointment': appointment}))
#     else:
#         return redirect('login')
            
    



@login_required
def join_room(request, roomID, appointment_id):
    if request.user.is_authenticated:
        current_schedule = TherapySessionSchedule.objects.get(appointment_id=appointment_id)
        print(current_schedule)

        if current_schedule.appointment.client == request.user:
            current_time = datetime.now().strftime('%I:%M %p')
            current_date = datetime.now().date()
            print(current_date, current_time) 

            current_appointment = Appointment.objects.get(id=appointment_id)
            appo_date = current_appointment.date
            appo_time = current_appointment.time_slot
            appointment = current_appointment
            print(appo_date, appo_time)

            # Calculate 10 minutes before the appointment time
            ten_minutes_before = (datetime.combine(appo_date, appo_time) - timedelta(minutes=10)).time().strftime('%I:%M %p')
            # Calculate one hour after the appointment time
            one_hour_after = (datetime.combine(appo_date, appo_time) + timedelta(hours=1)).time().strftime('%I:%M %p')
            print("10 mins before:", ten_minutes_before, "One hour after:", one_hour_after)

            if appo_date == current_date:
                print("checking date")
                if ten_minutes_before <= current_time <= one_hour_after:
                    print("User can join the meeting")
                    value = str(roomID)
                    print(value)
                    if value:
                        return redirect("/chat/meeting/client/?roomID=" + value)
                else:
                    msg = "Meeting is not scheduled yet"
                    return HttpResponse(loader.render_to_string('client/view-schedule-ag.html', {'message': msg, 'current_schedule': current_schedule, 'appointment': appointment}))
            else:
                msg = "Meeting is not scheduled yet"
                return HttpResponse(loader.render_to_string('client/view-schedule-ag.html', {'message': msg, 'current_schedule': current_schedule, 'appointment': appointment}))
        else:
            msg = "You are not authorized to join this meeting"
            return HttpResponse(loader.render_to_string('client/view-schedule-ag.html', {'message': msg, 'current_schedule': current_schedule, 'appointment': appointment}))
    else:
        return redirect('login')