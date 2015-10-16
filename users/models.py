from string import printable
from django.db import models
from django.db.models import signals, Q
from django.contrib.auth import models as authmod
from django.contrib.auth.models import User
from companies.models import Company
from django import forms

class CreateUserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    email = forms.EmailField()
    last_name = forms.CharField()
    first_name = forms.CharField()


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    companies = models.ManyToManyField(Company, blank=True)
    
    def get_favorites(self):
        c = self.companies.get(active=true,favorite=true)
        y = c.years.get(active=true,favorite=true)
        t = y.trimesters.get(active=true,favorite=true)
        return t

    def __str__(self):
        return self.user.username

    def real_name(self):
        return self.user.first_name + " " + self.user.last_name

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
