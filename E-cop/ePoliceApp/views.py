from django.shortcuts import render, redirect
from .models import *
from django.core.mail import send_mail
from random import randint
from django.conf import settings
from django.db.utils import *
import requests
import os
user_image_path = os.path.join(settings.MEDIA_ROOT, 'image\\')

app_info = {
    'app_name': 'E-Police Station',
    'msg_data': {'name': '', 'msg': '', 'type':'success', 'display': ''},
}

# check internet connection
def isConnected():
    try:
        url = requests.get('http://google.com')
        status  = url.status_code
        if status:
            return True
    except Exception as err:
        app_info['msg_data']['name'] = 'Internet Not Available'
        app_info['msg_data']['msg'] = 'Check your internet connection.'
        return False

# default index/home page
def index(request):
    if 'email' in request.session:
        profile_data(request)
    return render(request, 'index.html', app_info)

# about page
def about_page(request):
    return render(request, 'app/about.html', app_info)

# contact page
def contact_page(request):
    return render(request, 'app/contact.html', app_info)


####################################
## MAIN PAGES AND FUNCTIONALITIES ##
####################################

# id creation
def createID(n):
    range_start = 10 ** (n-1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)

# send otp on mail
def send_otp(request, otp_for='reg'):
    app_info['verify_for'] = otp_for

    email_to_list = [request.session['email'],]
    subject = 'OTP for Forgot Password'
    otp = randint(1000,9999)
    print('OTP is: ', otp)
    request.session['otp'] = otp
    message = f"your one time otp for forgot password is: {otp}"
    email_from = settings.EMAIL_HOST_USER
    if isConnected():
        send_mail(subject, message, email_from, email_to_list)

# otp page
def otp_page(request):
    print('Verify for: ', app_info['verify_for'])
    return render(request,'app/otp_page.html', app_info)

# otp verify functionality
def verify_otp(request, verify_for='reg'):
    if request.method == 'POST':
        if int(request.POST['otp']) == request.session['otp']:
            master = Master.objects.get(Email=request.session['email'])
            
            if verify_for == 'rec':
                master.Password = request.POST['password']
                app_info['msg_data']['name'] = 'Password Changed'
                app_info['msg_data']['msg'] = 'Congratulations!! Your password has successfully changed.'
            else:
                master.IsActive = True
                if master.Role.Role == 'citizen':
                    uid = f'citizen-{createID(5)}'
                    Citizen.objects.create(UID=uid, Master=master)
                elif master.Role.Role == 'department':
                    state = State.objects.get(id=1)
                    uid = f'department-{state.Name}-{createID(5)}'
                    Department.objects.create(Master=master, State=state, DeptID=uid)
                
                app_info['msg_data']['name'] = 'Verified'
                app_info['msg_data']['msg'] = 'Congratulations!! Your email has successfully verified.'

            master.save()

            app_info['msg_data']['type'] = 'success'
            app_info['msg_data']['display'] = 'show'

            del request.session['otp']
            del request.session['email']
            
            return redirect(login_page)
        else:
            app_info['msg_data']['name'] = 'Invalid OTP'
            app_info['msg_data']['msg'] = "OTP does not matched. Please enter correct otp."
            app_info['msg_data']['type'] = 'warning'
            app_info['msg_data']['display'] = 'show'
            return redirect(otp_page)
    else:
        app_info['msg_data']['name'] = 'Invalid Request'
        app_info['msg_data']['msg'] = "Something went wrong. Please try again leter."
        app_info['msg_data']['type'] = 'warning'
        app_info['msg_data']['display'] = 'show'
        return redirect(otp_page)
    pass

# load all roles
def load_role():
    all_role = Role.objects.all()
    return all_role

app_info['all_roles'] = load_role()

# register page
def register_page(request):
    return render(request, 'app/register.html', app_info)

# register functionality
def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        role_id = int(request.POST['role'])
        password = request.POST['password']
        try:
            role = Role.objects.get(id=role_id)
            Master.objects.create(Email=email,Role=role,Password=password)

            request.session['email'] = email
            send_otp(request)
            
            app_info['msg_data']['name'] = 'OTP Sent'
            app_info['msg_data']['msg'] = f'One-Time Password has sent to {email}.'
            app_info['msg_data']['type'] = 'success'
            app_info['msg_data']['display'] = 'show'
            
            return redirect(otp_page)

        except IntegrityError as err:
            msg = f'Error in register view @ line 139: {err}'
            print(msg)
            #console(err) # display error in terminal
            print('unique'.upper() in err.args[0])
            
            if 'unique'.upper() in err.args[0]:
                app_info['msg_data']['name'] = 'Email existed'
                app_info['msg_data']['msg'] = f'{email} is already existed.'

            app_info['msg_data']['type'] = 'danger'
            app_info['msg_data']['display'] = 'show'

            return redirect(register_page)
    else:
        pass

# login page
def login_page(request):
    return render(request, 'app/login.html', app_info)

# login functionality
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        master = ''
        try:
            master =  Master.objects.get(Email=email)
            print(password, master.Password)
            role = master.Role
            print(role.Role)
            if master.Password != password:
                raise Exception('password does not matched.')
            else:
                request.session['email'] = email

            return redirect(index)
        except Master.DoesNotExist as err:
            #console(err) # display error in terminal
            print('not exist' in err.args[0])
            
            if 'not exist' in err.args[0]:
                app_info['msg_data']['name'] = 'Not Registered'
                app_info['msg_data']['msg'] = f'{email} is not registered.'

            app_info['msg_data']['type'] = 'warning'
            app_info['msg_data']['display'] = 'show'
            return redirect(login_page)
        except Exception as err:
            #console(err) # display error in terminal
            if master.Password != password:
                app_info['msg_data']['name'] = 'Wrong Password'
                app_info['msg_data']['msg'] = f'Your {err.args[0]}'

                app_info['msg_data']['type'] = 'warning'
                app_info['msg_data']['display'] = 'show'
            return redirect(login_page)
    else:
        pass

# forgot password page
def forgot_pass_page(request):
    return redirect(login_page)

# forgot password functionality
def forgot_pass(request):
    if request.method == 'POST':
        email_to = request.session['email'] = request.POST['email']

        send_otp(request, otp_for='rec')

        app_info['msg_data']['name'] = 'OTP Sent'
        app_info['msg_data']['msg'] = f'One-Time Password has sent to {email_to} for verification.'
        app_info['msg_data']['type'] = 'success'
        app_info['msg_data']['display'] = 'show'

        return redirect(otp_page)
    else:
        pass

# load all bookings from pet owner
def load_complaints(pk):
    bookings = Complaint.objects.filter(PetCareTaker=pk)
    print(bookings)
    for s in bookings:
        print(s.Master)
        #for i in app_info['pet_service_names']:
        #    if s.PetDetail.Name == i['short_tag']:
        #        s.PetDetail.Name = i['tag']
    return bookings

# set status on bookings
def set_complaint_status(request, booking_id, status):
    print(booking_id, status)
    master =  Master.objects.get(Email=request.session['email'])
    pet_care = PetCareTaker.objects.get(Master=master)
    booking = Booking.objects.get(pk=booking_id, PetCareTaker=pet_care)
    print(booking)
    booking.Status = status
    booking.save()

    return redirect(profile_page)

# get profile data
def profile_data(request):
    if 'email' in request.session:
        try:
            master =  Master.objects.get(Email=request.session['email'])
            user_role = master.Role.Role
            print(user_role)
            
            state = State.objects.get(Country = 'India')
            cities = City.objects.filter(State = state) # default state is gujarat only

            app_info['user_role'] = user_role
            app_info['cities'] = cities

            if user_role == 'citizen':
                user = Citizen.objects.get(Master=master)
                app_info['profile_data'] = user
                app_info['complaint_data'] = Complaint.objects.filter(Citizen=user)[::-1]
                app_info['suspect_list'] = SuspectList.objects.filter(Citizen=user)[::-1]
                
            elif user_role == 'department':
                department = Department.objects.get(Master=master)
                app_info['profile_data'] = department
                app_info['stations'] = Station.objects.all()[::-1]
                
                #app_info['all_complaints'] = load_appointments(citizen, user_role)[::-1]
            elif user_role == 'petcaretaker':
                pet_care_data = PetCareTaker.objects.get(Master=master)
                app_info['profile_data'] = pet_care_data
                app_info['all_services'] = load_services(pet_care_data.pk)[::-1]
                app_info['all_bookings'] = load_bookings(pet_care_data)[::-1]

            if app_info['profile_data'].Image.url.split('/')[-1] != 'avtar.jpg':
                app_info['has_profile_image'] = True
            else:
                app_info['has_profile_image'] = False

        except Exception as err:
            print('Error in profile_data method: ', err)

# profile page
def profile_page(request):
    profile_data(request)
    return render(request, 'app/profile.html', app_info)

# profile update
def profile_update(request):
    master = Master.objects.get(Email=request.session['email'])
    user = ''
    user_name = ''
    user_uid = ''
    profile_image_path = ''

    user_role = master.Role.Role
    if user_role == 'citizen':
        user = Citizen.objects.get(Master=master)
        user_uid = user.UID
        user.FullName = user_name = request.POST['fullname']
        user.Gender = request.POST['gender']
        user.Country = request.POST['country']
        user.State = request.POST['state']
        user.City = request.POST['city']
        user.Pincode = request.POST['pincode']
        user.Address = request.POST['address']

        profile_image_path = os.path.join(user_image_path, 'users')

    elif user_role == 'department':
        user = Department.objects.get(Master=master)
        user_uid = user.DeptID
        user.DeptName = user_name = request.POST['deptname']
        user.About = request.POST['about']
        user.HeadOfficeAddress = request.POST['address']

        profile_image_path = os.path.join(user_image_path, 'departments')

    user.Mobile = request.POST['mobile']

    if 'user_image' in request.FILES:
        user_image = request.FILES['user_image']
        
        # renaming the uploaded image according to user id
        user_name = '_'.join(user_name.split())
        user_image.name = f'{user_uid}-{user_name.lower()}.{user_image.name.split(".")[-1]}'

        #citizen_image_path = os.path.join(user_image_path, 'users')
        is_path = os.path.isdir(profile_image_path)
        
        if not is_path:
            os.makedirs(profile_image_path)

        for file_name in os.listdir(profile_image_path):
            #print('files: ', fname)
            if file_name == user_image.name:
                f = os.path.join(profile_image_path, user_image.name)
                print(f)
                os.remove(f)
                print(f"file {f} is deleted successfully")

        user.Image = user_image
    user.save()
    
    app_info['msg_data']['name'] = 'Profile Updated'
    app_info['msg_data']['msg'] = f'Your profile has been successfully updated.'
    app_info['msg_data']['type'] = 'success'
    app_info['msg_data']['display'] = 'show'
    return redirect(profile_page)

# change password
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']

        master = Master.objects.get(Email=request.session['email'])

        if current_password == master.Password:
            master.Password = new_password
            master.save()
            app_info['msg_data']['name'] = 'Password Changed'
            app_info['msg_data']['msg'] = f'Your password changed successfully done.'
            app_info['msg_data']['type'] = 'success'
        else:
            app_info['msg_data']['name'] = 'Not Matched'
            app_info['msg_data']['msg'] = f'Please enter your currect current password.'
            app_info['msg_data']['type'] = 'warning'
        app_info['msg_data']['display'] = 'show'
        return redirect(profile_page)
    else:
        pass

# create suspect list by citizen
def create_suspect_list(request):
    suspect_name = request.POST['suspect_name']
    suspect_mobile = request.POST['suspect_mobile']
    suspect_gender = request.POST['suspect_gender']
    suspect_address = request.POST['suspect_address']

    master = Master.objects.get(Email=request.session['email'])
    citizen = Citizen.objects.get(Master=master)

    suspect_data = SuspectList.objects.create(
        Citizen=citizen,
        SuspectName=suspect_name,
        Gender=suspect_gender,
        SuspectAddress=suspect_address,
    )

    if suspect_mobile:
        suspect_data.SuspectMobile = suspect_mobile

    if 'suspect_image' in request.FILES:
        suspect_image = request.FILES['suspect_image']
        
        # renaming the uploaded image according to user id
        suspect_name = '_'.join(suspect_data.SuspectName.split())
        suspect_image.name = f'{citizen.UID}-{suspect_data.SuspectName.lower()}.{suspect_image.name.split(".")[-1]}'

        suspect_image_path = os.path.join(user_image_path, 'suspects')
        is_path = os.path.isdir(suspect_image_path)
        
        if not is_path:
            os.makedirs(suspect_image_path)

        for fname in os.listdir(suspect_image_path):
            print('files: ', fname)
            if fname == suspect_image.name:
                f = os.path.join(suspect_image_path, suspect_image.name)
                print(f)
                os.remove(f)
                print(f"file {f} is deleted successfully")

        suspect_data.Image = suspect_image

    suspect_data.save()

    app_info['msg_data']['name'] = 'Suspect Added.'
    app_info['msg_data']['msg'] = f'Suspect has been successfully added to pet list.'
    app_info['msg_data']['type'] = 'success'
    app_info['msg_data']['display'] = 'show'
    return redirect(profile_page)

# add complaint
def create_complaint_list(request):
       if request.POST:
        DateCreated = request.POST['DateCreated']
        DateOfCrime = request.POST['DateOfCrime']
        Description = request.POST['Description']

        obj = Complaint(DateCreated=DateCreated, DateOfCrime=DateOfCrime, Description=Description)
        obj.save()
        

        return redirect('profile')
        app_info['msg_data']['msg'] = 'Congratulations!! Your complaint successfully addded.'
    


# remove pet detail
def remove_suspect_detail(request, pk):
    master = Master.objects.get(Email=request.session['email'])
    citizen = Citizen.objects.get(Master=master)
    Citizen.objects.get(pk=pk, Citizen=citizen).delete()

    return redirect(profile_page)

# remove complaint
def remove_complaint(request, pk):
    Booking.objects.get(pk=pk).delete()
    return redirect(profile_page)

# complaint history
def complaint_history(request):
    master = Master.objects.get(Email=request.session['email'])
    bookings = Booking.objects.filter(Master=master)
    
    dic = []

    for booking in bookings:
        for i in service_name_choices:
            if booking.Service.Name in i[0]:
                booking.Service.Name = i[1]
        #print(booking)
        
        dic.append(
            {
                'id': booking.id,
                #'pet_owner': pet_owner,
                'service': {'s_id': booking.Service.id, 's_name': booking.Service.Name},
                'pet_care_taker': {'ptc_id': booking.PetCareTaker.id, 'ptc_name': booking.PetCareTaker.FullName},
                'pets': {'pet_id': booking.PetDetail.id, 'pet_name': booking.PetDetail.Name},
                'date_time': booking.Date.strftime('%Y-%m-%d'),
                'status': booking.Status,
            }
        )

        
    return JsonResponse({'booking_history': dic[::-1]})

# add station by department
def add_station(request):
    city_id = int( request.POST['city'] )
    city = City.objects.get(id=city_id)


    master = Master.objects.get(Email=request.session['email'])
    department = Department.objects.get(Master=master)


    st_id = f'{createID(5)}-{city.Name}'

    station_data=Station.objects.create(
        StID = st_id,
        StationName=request.POST['station'],
        Email=request.POST['st_email'],
        Mobile=request.POST['st_mobile'],
        Pincode=request.POST['st_pincode'],
        Address=request.POST['st_address'],
        City=city,
        Department=department,
        
    )

    app_info['msg_data']['name'] = 'Station Added'
    app_info['msg_data']['msg'] = f'Your Station Added successfully done.'
    app_info['msg_data']['type'] = 'success'

    return redirect(profile_page)

# remove station
def remove_station(request, pk):
    Station.objects.get(pk=pk).delete()
    return redirect(profile_page)

# Logout Functionality
def logout(request):
    present_sessions = []
    for i in request.session.keys():
        if not i.startswith('_'):
            present_sessions.append(i)

    for i in present_sessions:
        del request.session[i]

    return redirect(index)

def petcaretaker_content(request):
    return render(request, "app/petcaretaker_content.html")







    