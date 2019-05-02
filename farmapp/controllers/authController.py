from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse, render_to_response
from django.utils.translation import ugettext_lazy as _
from django.views import View
from farmapp.helpers import authHelper as farmAuth
from FarmProj.helpers import validateHelper
from farmapp.models import FarmUser
from django.contrib.sites.shortcuts import get_current_site
from django.urls.base import reverse
from django.conf import settings
from django.core.mail import send_mail
from FarmProj.helpers import commonHelper as commonMethods


LOGIN_PAGE = 'login.html'
REGISTER_PAGE = 'register.html'


class AuthView(View):

    def get(self, request):
        if farmAuth.is_FarmUser_authenticated(request):
            return redirect(reverse('farmApp:home'))
        reg_link = reverse('farmApp:register')
        forgot_pass = reverse('farmApp:recoverpassword')
        return render(request, LOGIN_PAGE, {"reg_link": reg_link.__str__(),
                                            "forgot_pass": forgot_pass.__str__()})

    def validate_data(self, request):
        data = {}

        email = request.POST.get('email', '')
        data['email'] = email

        password = request.POST.get('password', '')
        data['password'] = password

        if not validateHelper.validate_email(email):
            raise ValidationError('Email Is Not Valid')

        return data

    def post(self, request):
        try:
            data = self.validate_data(request)
        except ValidationError as e:
            messages.error(request, e.message)
            return HttpResponseRedirect(reverse('farmApp:auth'))
        except Exception as e:
            pass

        try:
            farmUser = FarmUser.objects.get(email=data['email'])
        except:
            messages.error(request, "Email Id or Password Incorrect")
            return redirect(request.META['HTTP_REFERER'])

        if farmAuth.checkKycUserPassword(farmUser, data['password']):
            response = farmAuth.loginKycUser(request, farmUser)
            messages.success(request, "Login Succsufully")
            return redirect(reverse('farmApp:home'))
        else:
            messages.error(request, "Email Id or Password Incorrect")

        return redirect(request.META['HTTP_REFERER'])


class registerView(View):

    def get(self, request, *args, **kwargs):

        if farmAuth.is_FarmUser_authenticated(request):
            return redirect(reverse('farmApp:home'))
        login_link = reverse('farmApp:auth')
        return render(request, REGISTER_PAGE, {"login_link": login_link.__str__()})

    def validate_data(self, request):
        first_name = request.POST.get('first_name', '')
        data = {}
        if first_name == '':
            raise ValidationError(_('First Name Is Empty'))
        data['first_name'] = first_name

        last_name = request.POST.get('last_name', '')
        if last_name == '':
            raise ValidationError('Last Name Is Empty')
        data['last_name'] = last_name

        email = request.POST.get('email', '')

        if not validateHelper.validate_email(email):
            raise ValidationError('Email Is Not Valid')

        data['email'] = email

        mobile_no = request.POST.get('mobile_no', '')

        if not validateHelper.validate_mobile(mobile_no):
            raise ValidationError('Enter valid mobile number')

        data['mobile_no'] = mobile_no

        password = request.POST.get('password', '')
        if len(password) < 8:
            raise ValidationError(_('Enter more than 8 characters '))
        data['password'] = password

        confirm_pass = request.POST.get('confirm_pass', '')
        if confirm_pass != password:
            raise ValidationError(_('Both passwords dont match'))

        return data

    def post(self, request):

        try:
            data = self.validate_data(request)
        except ValidationError as e:
            messages.error(request, e.message)
            return HttpResponseRedirect(reverse('farmApp:register'))
        except Exception as e:
            pass

        match = FarmUser.objects.filter(email=data['email']).exists()
        if match == False:
            try:
                farmUser = FarmUser().createFarmUser(email=data['email'], first_name=data['first_name'],
                                                     last_name=data['last_name'], mobile_no=data['mobile_no'],
                                                     password=data['password'])

                messages.success(request, "Account created succufully check your email for verifiaction details")

            except Exception as e:
                messages.error(request, e.__str__())
        else:
            messages.error(request, "User already Exist With this Email")

        subject = "Activate your Account."
        message = 'Welcome to kyc'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [data['email']]
        fail_silently = False

        send_mail(subject, message, from_email, recipient_list, fail_silently)
        return redirect(request.META['HTTP_REFERER'])


@farmAuth.Farm_login_required_Def
def logout(request):
    response = farmAuth.logoutFarmUser(request, request.farm_user)
    messages.success(request, "Logout Succsufully")
    return redirect(reverse('farmApp:auth'))