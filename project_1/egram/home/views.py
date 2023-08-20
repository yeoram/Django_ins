from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import Feed
from user.models import User
from content.models import Reply, Like, Bookmark
from uuid import uuid4 #파일 업로드시 유니크한 코드를 주어서 파일이름을 설정하기 위해 필요함
import os
from egram.settings import MEDIA_ROOT


def home(request):
    return render(request, 'user/login.html')

@api_view(['GET'])
def get(request):
    print('GET GET GET')
    email = request.session.get('email', None)
    print('로그인 사용자', request.session.get('email', None))
    if email is None:      
        return render(request, 'user/login.html')
    
    user = User.objects.filter(email=email).first()

    if user is None:
        return render(request, 'user/login.html')
    
    feed_list = []
    feed_object_list = Feed.objects.all().order_by("-id")          #select * from home_feed,,, order_by('-id') 나중에 삽입된 것부터 읽어온다
    for feed in feed_object_list:
        feed_user = User.objects.filter(email=feed.email).first()
        reply_object_list = Reply.objects.filter(feed_id=feed.id)
        reply_list = []
        for reply in reply_object_list:
            re_user = User.objects.filter(email=reply.email).first()
            reply_list.append(dict(feed_id=reply.feed_id,
                                   reply_content=reply.reply_content,
                                   nickname=re_user.nickname))
        like_count = Like.objects.filter(feed_id=feed.id,is_like=True).count()
        is_like = Like.objects.filter(feed_id=feed.id, email=email,is_like=True).exists()
        is_marked = Bookmark.objects.filter(feed_id=feed.id, email=email, is_marked=True).exists()
        feed_list.append(dict(id= feed.id,
                              image=feed.image,
                              content=feed.content,
                              like_count=like_count,
                              profile_image=feed_user.profile_image,
                              nickname=feed_user.nickname,
                              reply_list=reply_list,
                              is_like=is_like,
                              is_marked=is_marked))
    return render(request, 'home/main.html', context=dict(feed_list=feed_list, user=user))

@api_view(['POST'])
def post(request):
    print('POST POST POST')
    file = request.FILES['file']
    uuid_name = uuid4().hex
    save_path = os.path.join(MEDIA_ROOT, uuid_name) #MEDIA_ROOT+uuid_name을 해서 파일 경로 만들기
    #실제 파일을 저장하는 코드
    with open(save_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    
    image = uuid_name
    content = request.data.get('content')
    email = request.session.get('email', None)

    Feed.objects.create(image=image, content=content, email=email)


    return Response(status=200)

@api_view(['GET'])
def profile(request):
    print("PROFILE PROFILE GET GET GET")
    email = request.session.get('email', None)
    print('로그인 사용자', request.session.get('email', None))
    if email is None:      
        return render(request, 'user/login.html')
    
    user = User.objects.filter(email=email).first()

    if user is None:
        return render(request, 'user/login.html')
    
    return render(request, 'home/profile.html', context=dict(user=user))

class Profile(APIView):
    def get(self, request):
        print("PROFILE CLASS PROFILE CLASS GET GET GET")
        email = request.session.get('email', None)
        print('로그인 사용자', request.session.get('email', None))
        if email is None:      
            return render(request, 'user/login.html')
        
        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, 'user/login.html')
        
        feed_list = Feed.objects.filter(email=email).all()
        print(feed_list)

        feed_count = feed_list.count()
        
        like_list = list(Like.objects.filter(email=email, is_like=True).values_list('feed_id', flat=True))
        like_feed_list = Feed.objects.filter(id__in=like_list)
        bookmark_list = list(Bookmark.objects.filter(email=email, is_marked=True).values_list('feed_id', flat=True))
        bookmark_feed_list = Feed.objects.filter(id__in=bookmark_list)
        return render(request, 'home/profile.html', context=dict(feed_list=feed_list,
                                                                like_feed_list=like_feed_list,
                                                                bookmark_feed_list=bookmark_feed_list,
                                                                user=user,
                                                                feed_count = feed_count))


class UploadReplay(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        reply_content = request.data.get('reply_content', None)
        email = request.session.get('email', None)
        print(feed_id, reply_content, email)
        Reply.objects.create(feed_id=feed_id, reply_content=reply_content, email=email)

        return Response(status=200)
    

class Toglelike(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        favorite_text = request.data.get('favorite_text', True)
        if favorite_text == 'favorite_border':
            print(favorite_text)
            is_like=True
        else:
            print(favorite_text)
            is_like=False

        email = request.session.get('email', None)
        print(feed_id,is_like, email)
        is_exist = Like.objects.filter(feed_id=feed_id, email=email).first()
        print("is_exist:   ", is_exist)
        if is_exist:
            print("업데이트 :", feed_id,is_like, email)
            is_existis_marked =is_like
            is_exist.save()
           # Like.objects.create(feed_id=feed_id,is_marked, email=email)
        else:
            print("크리에이트 :", feed_id,is_like, email)
            Like.objects.create(feed_id=feed_id,is_like=is_like, email=email)

        return Response(status=200)
    
class TogleBookmark(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        bookmark_text = request.data.get('bookmark_text', True)
        if bookmark_text == 'bookmark_border':
            print(bookmark_text)
            is_marked=True
        else:
            print(bookmark_text)
            is_marked=False

        email = request.session.get('email', None)
        print(feed_id, is_marked, email)
        is_exist = Bookmark.objects.filter(feed_id=feed_id, email=email).first()
        print("is_exist:   ", is_exist)
        if is_exist:
            print("업데이트 :", feed_id,is_marked, email)
            is_exist.is_marked = is_marked
            is_exist.save()
           # Like.objects.create(feed_id=feed_id,is_marked, email=email)
        else:
            print("크리에이트 :", feed_id,is_marked, email)
            Bookmark.objects.create(feed_id=feed_id, is_marked=is_marked, email=email)

        return Response(status=200)
    
class Search(APIView):
    def post(self, request):
        search_content = request.session.get('search_content', None)
        print('검색어', search_content)
        if search_content is None:      
            return render(request, 'main.html')
        
        user = User.objects.filter(email=search_content).first()

        if user is None:
            user = User.objects.filter(nickname=search_content).first()
            if user is None:
                return render(request, 'main.html')
        
        feed_list = Feed.objects.filter(email=user.email).all()
        if feed_list is None:
            print("검색할 수 없습니다")
            return render(request, 'main.html')
        
        return render(request, 'home/main.html', context=dict(feed_list=feed_list))