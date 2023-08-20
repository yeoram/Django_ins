from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class User(AbstractBaseUser):
    """
    user profile -> 프로필 사진
    user id->화면에 표기되는 이름
    user name -> 실제 이름
    user email ->회원가입시 필요
    user password ->디폴트 사용
    """

    profile_image = models.TextField()
    nickname = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=24)
    email= models.EmailField(unique=True)

    USERNAME_FIELD = 'nickname'

    class Meta:
      db_table = "User"
