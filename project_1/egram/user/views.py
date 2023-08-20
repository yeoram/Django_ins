import os
from uuid import uuid4
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from egram.settings import MEDIA_ROOT
from .models import User
from django.contrib.auth.hashers import make_password

class Join(APIView):
    def get(self, request):
        return render(request,'user/join.html')
    
    def post(self, request):
        print("JOIN POST JOIN POST")
        email = request.data.get('email', None)
        nickname = request.data.get('nickname', None)
        name = request.data.get('name', None)
        password = request.data.get('password', None)
        profile_image = 'default_profile.jpeg'

        print(email, nickname, name, password, profile_image)
        
        User.objects.create(email=email, 
                            nickname=nickname, 
                            name=name, 
                            password=make_password(password),
                            profile_image= profile_image)
        
        return Response(status=200)


class Login(APIView):
    def get(self, request):
        return render(request, 'user/login.html')
    
    def post(self, request):
        print("LOGIN POST LOGIN POST")
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        print(email)
        user = User.objects.filter(email=email).first()

        if user is None :
            return Response(status=400, data=dict(message='회원정보가 잘못되었습니다.'))
        
        if user.check_password(password):
            #로그인 성공 : 세선 or 쿠키
            request.session['email'] = email
            return Response(status=200)
        else:
            return Response(status=400, data=dict(message='회원정보가 잘못되었습니다'))
        

class Logout(APIView):
    def get(self, request):
        request.session.flush()
        return render(request, 'user/login.html')
    
    def post(self, request):
        pass

class UploadProfile(APIView):
    def post(self, request):
        print('POST POST POST')
        file = request.FILES['file']

        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name) #MEDIA_ROOT+uuid_name을 해서 파일 경로 만들기
        #실제 파일을 저장하는 코드
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        profile_image = uuid_name
        email = request.data.get('email')
        
        user = User.objects.filter(email=email).first()

        user.profile_image = profile_image
        user.save()

        #Feed.objects.create(image=image, content=content, user_id=user_id, profile_image=profile_image, like_count=0)


        return Response(status=200)