from django.http import JsonResponse
from django.conf import settings
import re

from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.views.generic.edit import FormView
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.core.exceptions import ValidationError
from farmapp.helpers import authHelper as farmAuth
from farmapp.models import FarmUser
from django.core.exceptions import ValidationError
from FarmProj.helpers import validateHelper
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import FileSystemStorage

HOME_PAGE = 'index.html'
PROFILE_PAGE = 'profile.html'


class index(View):

    @farmAuth.Farm_login_required_Class
    def get(self, request):
        return render(request, HOME_PAGE)


class profile(View):

    @farmAuth.Farm_login_required_Class
    def get(self, request):
        return render(request, PROFILE_PAGE)

    def validate_data(self, request):
        data = {}

        full_name = request.POST.get('full_name', '')
        if full_name == '':
            raise ValidationError('Full Name Is Empty')
        data['full_name'] = full_name

        email = request.POST.get('email', '')
        if not validateHelper.validate_email(email):
            raise ValidationError('Enter Valid Email ')
        data['email'] = email

        contact_no = request.POST.get('contact_no', '')
        if not validateHelper.validate_mobile(contact_no):
            raise ValidationError('Enter valid Contact number')
        data['contact_no'] = contact_no

        return data

    @farmAuth.Farm_login_required_Class
    def post(self, request):

        try:
            data = self.validate_data(request)
        except ValidationError as e:
            messages.error(request, e.message)

            return HttpResponseRedirect(reverse('farmApp:profile'))
        except Exception as e:
            messages.error(request, e.message)
            return HttpResponseRedirect(reverse('farmApp:profile'))

        farmuser = request.farm_user
        farmuser.full_name = data['full_name']
        farmuser.email = data['email']
        farmuser.contact_no = data['contact_no']
        farmuser.save()
        messages.success(request, "Changes Successfully Save")
        return HttpResponseRedirect(reverse('farmApp:profile'))


class changepassword(View):

    def validate_data(self, request):
        data = {}
        old_password = request.POST.get('old_password', '')

        if len(old_password) < 8:
            raise ValidationError(_('Enter more than 8 characters'))

        if farmAuth.checkFarmUserPassword(request.farm_user, old_password) is False:
            raise ValidationError(
                _('Current password not match with your password'))

        new_password = request.POST.get('new_password', '')

        if len(new_password) < 8:
            raise ValidationError(_('Enter more than 8 characters '))

        data['new_password'] = new_password

        confirm_pass = request.POST.get('confirm_password', '')

        if confirm_pass != new_password:
            raise ValidationError(
                _('New Password and Confirm Password dont match'))

        return data

    @farmAuth.Farm_login_required_Class
    def post(self, request):

        try:
            data = self.validate_data(request)
        except ValidationError as e:
            messages.error(request, e.message)
            return HttpResponseRedirect(reverse('farmApp:profile'))
        except Exception as e:
            messages.error(request, e.message)
            return HttpResponseRedirect(reverse('farmApp:profile'))

        farmuser = request.farm_user
        farmuser.set_password(data['new_password'])
        farmuser.save()
        messages.success(request, "Password Updated Successfully")
        return HttpResponseRedirect(reverse('farmApp:profile'))
