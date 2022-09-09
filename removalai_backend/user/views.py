from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from .models import Image, UserTransaction, UserData, Updated_image
import requests


@login_required(login_url="/login/")
def index(request):
    if request.method == 'POST':
        image = request.FILES['rm_file_upload']

        images = Image(user=request.user, image=image)
        images.save()

        user_data = UserData.objects.get(user=request.user)
        user_data_uploads = user_data.images_used
        user_data_uploads += 1
        user_data.images_used = user_data_uploads
        user_data_left = user_data.images_left
        if user_data_left != 0:
            user_data_left -= 1
            user_data.images_left = user_data_left
            user_data.save()

            user_transaction = UserTransaction(user=request.user, transaction_type = "Credit", uploads_till_now = user_data_uploads )
            user_transaction.save()

            print(images.image)

            image_url = "http://127.0.0.1:8000" + images.image.url
            # print(image_url)

            url = "https://api.removal.ai/3.0/remove"

            payload={'image_url': image_url}
            files=[
            ('image_file',images.image)
            ]
            headers = {
            'Rm-Token': '6278ec5ba0ef29.56369658'
            }

            response = requests.request("POST", url, headers=headers, data=payload, files=files)

            response_data = response.json()
            print(response_data["url"])

            updated_images = Updated_image(user=request.user, updated_image=response_data["url"])
            updated_images.save()

            context = {'image':images, 'new_image':updated_images}
            # context = {'image':images}   # Disable this in testing
            return render(request, 'dashboard2.html', context)

        else:
            context={'message':'You have reached your upload limit!'}
            return render(request, 'dashboard1.html', context)

    return render(request, 'dashboard1.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'message':'Invalid Credentials'})

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login')    


@login_required(login_url="/login/")
def history(request):
    user_data = UserData.objects.get(user=request.user)
    transaction = UserTransaction.objects.filter(user=request.user)
    # orders = AllOrder.objects.filter(user=request.user)
    # return render( request, 'student/dashboard/my_order.html',{'orders':orders})
    context = {'data':user_data, 'transactions': transaction}
    return render(request, 'history.html', context)


@login_required(login_url="/login/")
def UserProfile(request):
    user_data = UserData.objects.get(user=request.user)
    context = {'name':request.user.username, 'email':request.user.email, 'data':user_data}
    # print(context)
    return render(request, 'Profile.html', context)


@login_required(login_url="/login/")
def InfoUpdate(request):
    if request.method == 'POST':
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        email = request.POST['email']

        request.user.first_name = fname
        request.user.last_name = lname
        request.user.email = email
        request.user.save()

        return redirect('profile')

    return JsonResponse({'message':'GET Request not allowed'})

@login_required(login_url="/login/")
def PassUpdate(request):
    if request.method == 'POST':
        currpass = request.POST['current_pass']
        newpass1 = request.POST['new_pass1']
        newpass2 = request.POST['new_pass2']
        currentpassword= request.user.password #user's current password
        # print(currentpassword)
        matchcheck = check_password(currpass, currentpassword)
        if matchcheck:
            if newpass1 == newpass2:
                request.user.set_password(newpass1)
                request.user.save()
                context = {'name':request.user.username, 'email':request.user.email, 'message2':'Password Change Success'}
                return redirect('profile')
            else:
                context = {'name':request.user.username, 'email':request.user.email, 'message2':'Make sure new passwords are same!'}
                return render(request, 'Profile.html', context)
        else:
            context = {'name':request.user.username, 'email':request.user.email, 'message2':'Enter correct current password'}
            return render(request, 'Profile.html', context)
    
    return JsonResponse({'message':'GET Request not allowed'})