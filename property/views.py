from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import PropertyListing, PropertyComment, Notification, Meeting
from .forms import PropertyListingForm, MeetingForm
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta, datetime
from property.utils.createNotification import create_notification
from property.utils.getNotifications import get_notifications_for_user
import json
from .decorators import allowed_users

@login_required
# @allowed_users(allowed_roles=['admin'])
def homeView(request):
    try:
        group = request.user.groups.all()[0].name

        if group == 'customer':
            form = PropertyListingForm()
            user_property = PropertyListing.objects.filter(is_active=True).order_by('-id')

            context = {
                'properties': user_property,
                'form': form
            }

            if request.method == 'POST':
                form = PropertyListingForm(request.POST)
                print("form valid => ", form)
                if form.is_valid():
                    property = form.save(commit=False)
                    property.owner = request.user
                    property.save()

                    create_notification(
                        title="New Property Added",
                        detail=f"A new property was added by {request.user.username}: {request.POST['title']}",
                        property=property,
                        user=request.user,
                        notification_type='property'
                    )

                    return redirect('home')

            return render(request, 'property/home.html', context)
        elif group == 'admin':
            properties = PropertyListing.objects.filter(is_active=True).order_by('-id')

            context = {
                'properties': properties,
            }

            return render(request, 'property/admin/home.html', context)
        else:
            return redirect('login')
    except Exception as e:
        print("error => ",e)
        messages.success(request, 'Your profile is not complete for login')
        return redirect('logout')

@login_required
def updatePropertyView(request, pk):
    try:
        property = PropertyListing.objects.get(pk=pk, is_active=True)
    except Exception as e:
        pass
    form = PropertyListingForm(instance=property)

    if request.method == 'POST':
        form = PropertyListingForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'property/updateProperty.html', context)

@login_required
def deletePropertyView(request, pk):
    try:
        property = PropertyListing.objects.get(pk=pk, is_active=True)
        property.is_active = False

        property.save()
        return redirect('home')
    except Exception as e:
        pass

@login_required
def propertyDetailView(request, pk):
    try:
        property = PropertyListing.objects.get(pk=pk, is_active=True)
        comments = PropertyComment.objects.filter(property=property).order_by('-created_at')
    except Exception as e:
        pass

    if request.method == 'POST':
        new_comment = PropertyComment(
            comment=request.POST['comment'],
            user=request.user,
            property=property
        )
        new_comment.save()

        # Create a notification for the new comment
        create_notification(
            title="New Comment Added",
            detail=f"A new comment was added by {request.user.username}: {request.POST['comment']}",
            property=property,
            user=request.user,
            comment=new_comment,
            notification_type='comment'
        )

    context = {'property': property, 'comments': comments}
    return render(request, 'property/detailView.html', context)

@login_required
def updateComment(request, pk):
    try:
        data = json.loads(request.body)
        comment_text = data.get('comment')

        comment = PropertyComment.objects.get(pk=pk)
        if comment:
            comment.comment = comment_text
            comment.save()
            return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False})

@login_required
def deleteCommentView(request, comment_pk, property_pk):
    try:
        comment = PropertyComment.objects.get(pk=comment_pk)
        
        if comment:
            comment.delete()
        
        return redirect('property_detail', pk=property_pk)
    except Exception as e:
        pass

@login_required
def updatePropertyStatusView(request, pk):
    try:
        property = PropertyListing.objects.get(pk=pk, is_active=True)
    except Exception as e:
        pass

    if request.method == 'POST':
        property.status = request.POST['status']
        property.save()

        create_notification(
            title="Property status has been updated",
            detail=f"{request.user.username}: has updated the status of your property",
            property=property,
            user=request.user,
            notification_type='status'
        )

    return redirect('property_detail', pk=pk)


@login_required
def fetch_notifications(request):
    if request.user.is_authenticated:
        group = request.user.groups.all()[0].name
        
        if group == 'admin':
            user_properties = PropertyListing.objects.filter(is_active=True).order_by('-id')
        else:
            user_properties = PropertyListing.objects.filter(owner=request.user, is_active=True).order_by('-id')
        
        notifications = get_notifications_for_user(
            user=request.user,
            property_filter=user_properties,
            notification_types=['comment', 'status', 'meeting'] if group == 'customer' else ['comment', 'property']
        )

        notifications_data = [
            {
                'id': notification.pk,
                'title': notification.title,
                'detail': notification.detail,
                'property': notification.property.pk if notification.property else None,
                'meeting': notification.meeting.pk if notification.meeting else None,
                'type': notification.notification_type,
                'created_at': notification.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            for notification in notifications
        ]
        return JsonResponse({'notifications': notifications_data})
    else:
        return JsonResponse({'notifications': []})


@login_required
def mark_notification_read(request, notification_id):
    if request.method == 'POST' and request.user.is_authenticated:
        print('getting post.....')
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.is_readed = True
            notification.save()
            return JsonResponse({'success': True})
        except Notification.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Notification does not exist'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def viewNotificationDetail(request, notification_pk, property_pk):
    if request.method == 'GET' and request.user.is_authenticated:

        try:
            notification = Notification.objects.get(pk=notification_pk)

            if notification:
                notification.is_readed = True
                notification.save()
                return JsonResponse({'success': True, 'propertyId': property_pk})
        except Exception as e:
            pass

        return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def confirmMeeting(request, meeting_id):
    meeting = Meeting.objects.get(id=meeting_id)
    if request.method == 'POST':
        meeting.confirmed = True
        meeting.save()
        return redirect('meetings', request.user.id)
    return render(request, 'property/admin/confirm_meeting.html', {'meeting': meeting})

@login_required
def meetingDetails(request, meeting_id):
    meeting = Meeting.objects.get(id=meeting_id)
    return render(request, 'property/admin/meeting_details.html', {'meeting': meeting})

@login_required
def calendarView(request, property_pk):
    property = None
    try:
        property = PropertyListing.objects.get(pk=property_pk, is_active=True)
    except Exception as e:
        pass

    context = {'property': property}
    return render(request, 'property/admin/calendar_view.html', context)

@login_required
def availableTimeSlots(request):
    today = timezone.now().date()
    time_slots = []
    booked_slots = Meeting.objects.filter(date__gte=today)
    
    for i in range(30):
        date = today + timedelta(days=i)
        for hour in range(9, 17):
            start_time = datetime.combine(date, datetime.min.time()) + timedelta(hours=hour)
            end_time = start_time + timedelta(hours=1)
            slot_info = {
                'start': start_time.isoformat(),
                'end': end_time.isoformat(),
                'title': f'{hour}:00-{hour+1}:00',
                'display': 'block'
            }
            # Check if the slot is booked
            if booked_slots.filter(date=date, time__hour=hour).exists():
                slot_info['backgroundColor'] = 'red'
                slot_info['clickable'] = False
                slot_info['title'] = slot_info['title']+' Reserved'
            time_slots.append(slot_info)
    return JsonResponse(time_slots, safe=False)


@csrf_exempt
@login_required
def bookMeeting(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        date = data['date']
        time = data['time']
        property_id = data['property_id']
        try:
            property = PropertyListing.objects.get(pk=property_id, is_active=True)
        except Exception as e:
            pass

        if property:
            meeting = Meeting.objects.create(
                admin=request.user,
                landowner_id=property.owner.id,
                date=date,
                time=time
            )

            create_notification(
                title="A meeting has been scheduled",
                detail=f"{request.user.username}: has scheduled a meeting with you, Please click to confirm.",
                property=property,
                user=request.user,
                meeting=meeting,
                notification_type='meeting'
            )

            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)

def fetchAllMeetings(request, user_pk):
    if request.user.groups.all()[0].name == 'admin':
        meetings = Meeting.objects.filter(admin=request.user)
    elif request.user.groups.all()[0].name == 'customer':
        meetings = Meeting.objects.filter(landowner=request.user)

    context = {'meetings': meetings}
    return render(request, 'property/meetings.html', context)

@login_required
def attendMeeting(request, meeting_id):
    print("meeting......", meeting_id)
    meeting = get_object_or_404(Meeting, id=meeting_id)
    return render(request, 'property/meeting.html', {'meeting_id': meeting_id})
