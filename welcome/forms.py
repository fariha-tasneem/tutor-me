from allauth.account.forms import LoginForm
from django import forms
from allauth.account.forms import SignupForm
class MyCustomSignupForm(SignupForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    def save(self, request):
        user = super(MyCustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        return user
class MyCustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

from allauth.socialaccount.forms import SignupForm
class MyCustomSocialSignupForm(SignupForm):
    def save(self, request):
        first_name = forms.CharField(required=True)
        last_name = forms.CharField(required=True)
        def save(self, request):
            user = super(MyCustomSocialSignupForm, self).save(request)
            user.first_name = self.cleaned_data.get('first_name')
            user.last_name = self.cleaned_data.get('last_name')
            user.save()
            return user