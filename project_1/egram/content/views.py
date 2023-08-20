from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from user.models import User
from uuid import uuid4 #파일 업로드시 유니크한 코드를 주어서 파일이름을 설정하기 위해 필요함
import os
from egram.settings import MEDIA_ROOT
from .models import Reply, Like, Bookmark
from home.models import Feed

class UploadReplay(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        reply_content = request.data.get('reply_content', None)
        email = request.session.get('email', None)

        Reply.objects.create(feed_id=feed_id, reply_content=reply_content, email=email)

        return Response(status=200)