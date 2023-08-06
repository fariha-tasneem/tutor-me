from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
class MyAccountAdapter(DefaultAccountAdapter):
  def get_signup_redirect_url(self, request):
     return '/googlelogin/type'
  def get_login_redirect_url(self, request):
      if request.user.type == "":
         return '/googlelogin/type'
      url = '/' + request.user.email
      if(request.user.type == 'stu'):
         url += '/student/'
      else:
         url +='/tutor/'
      return url