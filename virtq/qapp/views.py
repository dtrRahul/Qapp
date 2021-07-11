from django.shortcuts import render, loader, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Customers, Shop, Time, Barbers
from django.contrib.auth.models import auth
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http import HttpResponse
import requests
# import random
import emoji

# Create your views here.


def index(request):
    return render(request, 'index.html')


def services(request):
    return render(request, 'services.html')


# @csrf_protect
def appointment(request):
    shop = Shop.objects.filter(id=1)
    time = Time.objects.filter(status='Available')
    user = User.objects.all()
    return render(request, 'appointment.html', {'shop': shop, 'time': time, 'user': user})


def saloons(request):
    shop = Shop.objects.all()
    return render(request, 'barbers.html', {'shop': shop})


def contact(request):
    return render(request, 'contact.html')

@csrf_protect
def reschedule(request, uid):
    time = Time.objects.filter(status='Available')
    customer = Customers.objects.get(logid_id=uid)
    return render(request, 'reschedule.html', {'time': time, 'customer': customer})


@csrf_protect
def rescheduled_user(request,uid):
    if request.method == "POST":
        uid = request.POST['id']
        user_time = request.POST['times']
        date = request.POST['date']
        customer = Customers.objects.get(logid_id=uid)
        customer.time = user_time
        customer.save()
        data = Customers.objects.filter(logid_id=uid).all()
        userr = User.objects.filter(id=uid).values('username').first()
        user = userr['username']


        def convert24(user_time):
            if user_time[-4:] == "a.m.":
                return user_time[:-4]

            else:

                # add 12 to hours and remove PM
                return str(int(user_time[:1]) + 12) + user_time[1:4]
        customer_time = convert24(user_time)

        # tim = Time.objects.filter(time=user_time).values('id').first()
        # tid = tim['id']
        #
        # Time.objects.filter(id=tid).update(status='Unavailable', no_customers=1)

        # return render(request, 'user.html', {'data': data, 'user': user})
        return redirect('user', uid=uid)


def user(request, uid):
    data = Customers.objects.filter(logid_id=uid).all()
    userr = User.objects.filter(id=uid).values('username').first()
    user = userr['username']
    return render(request, "user.html", {'data': data, 'user': user})

@csrf_protect
def admin(request):
    shop = Shop.objects.all()
    return render(request, 'adm.html', {'shop': shop})


def login(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            request.session['uid'] = user.id
            user = User.objects.filter(username=username).values('username', 'id').first()
            user_id = user['id']
            data = Customers.objects.filter(logid_id=user_id).all()
            return render(request, 'user.html', {'data': data, 'user': request.user.username})
        else:
            return HttpResponse("The login is failed.You are not an Authorized User!!")

    return render(request, 'login.html')


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return render(request, 'index.html')


@csrf_protect
def user_data(request):
    cust = Customers.objects.all()

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']
        # sname = request.POST['shopname']
        user = auth.authenticate(username=username, password=password)
        print(user)
        custmer = Customers.objects.filter(hairdresser=username)
        if user is not None:
            auth.login(request, user)
            request.session['uid'] = user.id

            return render(request, 'userdata.html', {'cust': custmer})

        else:
            return HttpResponse("The login is failed.You are not an Authorized Admin!!")

    return render(request, 'userdata.html', {'cust': cust})  #this should be disabled after development

@csrf_exempt
def destroy(request, id):
    customer = Customers.objects.get(id=id)
    customer.delete()
    return render(request, 'index.html')

@csrf_exempt
def delete_customer(request, pid):
    if request.method == "POST":
        user_obj = Customers.objects.get(logid_id=pid)
        print(user_obj)
        barber = Customers.objects.filter(logid_id=pid).values('hairdresser').first()
        barber_name = barber['hairdresser']
        Barbers.objects.filter(name=barber_name).update(status='Available')
        user_obj.delete()

        cust = Customers.objects.filter()
        return render(request, 'userdata.html', {'cust': cust})


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = User.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    email_obj = Customers.objects.filter(email=email).exists()
    if email_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_protect
def booking(request):
    shop = Shop.objects.all()

    if request.method == "POST":

        sid = request.POST['id']
        firstname = request.POST['fname']
        lastname = request.POST['lname']
        username = request.POST['uname']
        password = request.POST['pswd']
        email = request.POST['email']
        phone = request.POST['phone']
        comments = request.POST['comments']
        date = request.POST['date']
        shopnames = request.POST['sname']
        shopaddress = request.POST['address']
        user_time = request.POST['times']
        # print(date)
        # print(user_time)
        # print(phone)

        user = User.objects.create_user(username=username, password=password)
        user.save()

        barber = Barbers.objects.filter(status='Available', shopname=shopnames).values('name').first()
        assigned_barber = barber['name']
        customer = Customers(firstname=firstname, lastname=lastname, email=email, mobile=phone, comments=comments,
                             logid_id=user.id, time=user_time, shopdetails=shopnames+','+shopaddress,
                             hairdresser=assigned_barber)
        customer.save()
        Barbers.objects.filter(name=assigned_barber).update(status='unavailable')

        # for generating token id and time by system itself
        # tim = Time.objects.filter(time=user_time).values('id', 'time').first()
        # tid = tim['id']
        # timm = tim['time']
        # print(timm)

        shop = Shop.objects.filter(id=sid)
        cid = customer.logid_id
        mail = customer.email

        def convert24(user_time):                                                    # Python program to convert time from 12 hour to 24 hour format
                                                                                     # Function to convert the date format

            if user_time[-4:] == "a.m.":
                return user_time[:-4]

            else:

                # add 12 to hours and remove PM
                return str(int(user_time[:1]) + 12) + user_time[1:4]
        customer_time = convert24(user_time)

        tim = Time.objects.filter(time=customer_time).values('id').first()
        tid = tim['id']

        subject = 'Thank you for using our services.'
        message = 'The token id for your appointment is :'

        from_email = settings.EMAIL_HOST_USER
        to_email = [mail]
        contact_message = "Hai %s\n %s  %s\n %s\n %s\n %s %s" % \
                          (username, message, cid, shopnames, shopaddress, date, user_time)

        send_mail(subject, contact_message, from_email, to_email, fail_silently=False)
        Time.objects.filter(id=tid).update(status='Unavailable', no_customers=1)

        global val

        def val():
            return username, user_time, cid, shopnames, shopaddress, firstname, lastname, phone

        return render(request, 'success.html')        # , 'sms': 'Thank you for making appointment. Mail has been sent'

    return render(request, 'index.html', {'shop': shop})


@csrf_exempt
def whatsapp(request):
    TWILIO_ACCOUNT_SID = 'AC4dbe5b35ef79baa1733caa36fbb958d7'
    TWILIO_AUTH_TOKEN = 'e83058bffe3a9f0921ad101617e34cec'
    TWILIO_API_KEY = 'SKc1592819029f6e0641289b0555015a12'
    TWILIO_API_SECRET = 'qrXZnPzWhcbNyb2trZu1QPI5pzpOgXzC'
    TWILIO_CHAT_SERVICE_SID = 'ISc58bf5e5d5fd4adca7207e26adff8aaf'

    global v
    v = val()
    print(v)
    username = v[0]
    token = v[2]
    phone = v[7]

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    from_whatsapp_number = 'whatsapp:+14155238886'
    to_whatsapp_number = 'whatsapp:%s' % phone
    bodymsg = 'Hai %s your token number is %s' \
              '\nYou are able to' \
              '\n1. Know Your Timing\n2.Know Your Status\n3.Get your complete Booking Info' \
              '\nRespond By number or hello for other Information.' \
              % (username, token)
    client.messages.create(body=bodymsg,
                           from_=from_whatsapp_number,
                           to=to_whatsapp_number)

    return render(request, 'index.html')


@csrf_exempt
def sms(request):

    if request.method == 'POST':
        # retrieve incoming message from POST request in lowercase
        incoming_msg = request.POST.get('Body')
        print(incoming_msg)
        vi = v
        uname = vi[0]
        usertime = vi[1]
        token = vi[2]
        shopname = vi[3]
        shopaddress = vi[4]
        fname = vi[5]
        lname = vi[6]
        print(vi)
        # create Twilio XML response
        resp = MessagingResponse()
        msg = resp.message()

        responded = False

        if incoming_msg == 'hello':
            response = emoji.emojize("""
            *Hi! Welcome to StyleBarber Bot* :wave:
            Let's be friends :wink:
            You can give me the following commands:
            :black_small_square: *'quote':* Hear an inspirational quote to start your day! :rocket:
            :black_small_square: *'statistics <country>'*: Show the latest COVID19 statistics for each country. :earth_americas:
            :black_small_square: *'statistics <prefix>'*: Show the latest COVID19 statistics for all countries starting with that prefix. :globe_with_meridians:
            """, use_aliases=True)
            msg.body(response)
            responded = True

        elif incoming_msg == 'quote':
            # returns a quote
            r = requests.get('https://api.quotable.io/random')

            if r.status_code == 200:
                data = r.json()
                quote = f'{data["content"]} ({data["author"]})'

            else:
                quote = 'I could not retrieve a quote at this time, sorry.'

            msg.body(quote)
            responded = True

        elif incoming_msg == '1':
            response = "Hi %s This is your timing %s" % (uname, usertime)
            msg.body(response)
            responded = True

        elif incoming_msg == '2':
            response = "Hi %s This is your Shop details %s\n%s" % (uname,shopname,shopaddress)
            msg.body(response)
            responded = True

        elif incoming_msg == '3':
            response = "Hi %s This is your complete booking info\n%s\n%s\n%s\n%s\n%s\n%s" % (uname, fname, lname, usertime, token, shopname, shopaddress)
            msg.body(response)
            responded = True

        if not responded:
            msg.body("Sorry, I don't understand. Respond with a number or hello")

        return HttpResponse(str(resp))

    return render(request, 'index.html')


