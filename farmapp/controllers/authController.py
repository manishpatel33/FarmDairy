import time

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
FORGETPASSWORD_PAGE = 'forgetpassword.html'
RESETPASSWORD_PAGE = 'resetpassword.html'


class AuthView(View):

    def get(self, request):
        if farmAuth.is_FarmUser_authenticated(request):
            return redirect(reverse('farmApp:home'))
        register_link = reverse('farmApp:register')
        forgetpass_link = reverse('farmApp:forgetpass')
        return render(request, LOGIN_PAGE, {"register_link": register_link.__str__(),
                                            "forgetpass_link": forgetpass_link})

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

        if farmAuth.checkFarmUserPassword(farmUser, data['password']):
            response = farmAuth.loginFarmUser(request, farmUser)
            messages.success(request, "Login Successfully")
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
        full_name = request.POST.get('full_name', '')
        data = {}
        if full_name == '':
            raise ValidationError(_('Full Name Is Empty'))
        data['full_name'] = full_name

        email = request.POST.get('email', '')

        if not validateHelper.validate_email(email):
            raise ValidationError('Enter Valid Email ')

        data['email'] = email

        contact_no = request.POST.get('contact_no', '')

        if not validateHelper.validate_mobile(contact_no):
            raise ValidationError('Enter valid Contact number')

        data['contact_no'] = contact_no

        password = request.POST.get('password', '')
        if len(password) < 8:
            raise ValidationError(_('Enter more than 8 characters'))
        data['password'] = password

        confirm_pass = request.POST.get('confirm_pass', '')
        if confirm_pass != password:
            raise ValidationError(_('password and Retype password not match'))
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
        if not match:
            try:
                farmUser = FarmUser().createFarmUser(email=data['email'], full_name=data['full_name'],
                                                     contact_no=data['contact_no'], password=data['password'])

                messages.success(request, "Account created successfully. check your email for verifiaction details")

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


class forgetpassword(View):

    def get(self, request):

        if farmAuth.is_FarmUser_authenticated(request):
            return redirect(reverse('farmApp:home'))
        login_link = reverse('farmApp:auth')
        reg_link = reverse('farmApp:register')
        return render(request, FORGETPASSWORD_PAGE, {"login_link": login_link.__str__(),
                                                     "reg_link": reg_link.__str__()})

    def validate_data(self, request):
        data = {}

        email = request.POST.get('email')
        if not validateHelper.validate_email(email):
            raise ValidationError('Email Is Not Valid')
        data['email'] = email
        try:
            farmUser = FarmUser.objects.get(email=data['email'])
        except:
            raise ValidationError("Email is not register")

        recaptcha = request.POST.get('g-recaptcha-response')
        response_captcha = commonMethods.recaptcha_response(request, recaptcha)
        response_captcha = response_captcha.json()

        if response_captcha['success'] is False:
            raise ValidationError('Select Captcha')

        data['g-recaptcha-response'] = recaptcha
        return data

    def post(self, request):
        try:
            data = self.validate_data(request)
        except ValidationError as e:
            messages.error(request, e.message)
            return HttpResponseRedirect(reverse('farmApp:forgetpass'))
        except Exception as e:
            pass

        obj = FarmUser.objects.get(email=data['email'])

        current_site = get_current_site(request)
        encryption = commonMethods.Encryption()
        enc_email = encryption.encrypt(data['email'])
        Re_captcha = encryption.encrypt(data['g-recaptcha-response'])
        token = str(obj.pk) + str(obj.first_name) + str(obj.last_name)
        enc_token = encryption.encrypt(token)
        millis = str(round(time.time() * 1000))
        c_time = encryption.encrypt(millis)
        activation_url = reverse('farmApp:resetpass',
                                 kwargs={'email': enc_email, 'token': enc_token, 'ctime': c_time})

        subject = "Reset Your Password"
        message = activation_url
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [data['email']]
        fail_silently = False

        send_mail(subject, message, from_email, recipient_list, fail_silently)
        messages.success(request, "Mail successfully send")
        return redirect(reverse('farmApp:forgetpass'))


def resetpassword(request, email, token, ctime):

    data = {}
    data['page'] = 'resetpassword'
    encryption = commonMethods.Encryption()
    url = reverse('farmApp:auth')

    try:
        dec_email = encryption.decrypt(email)
        dec_token = encryption.decrypt(token)
        dec_time = encryption.decrypt(ctime)
        user = FarmUser.objects.get(email=dec_email)
    except:
        messages.error(request, "Link is not Valid")
        return redirect(reverse('farmApp:auth'))
    else:
        millis = int(round(time.time() * 1000))
        dec_time = int(dec_time)
        diff_time = (millis - dec_time) / (1000 * 60)
        if diff_time > 60:
            messages.error(request, "link is expired")
            return redirect(reverse('farmApp:auth'))

    if request.method == "GET":
        login_link = reverse('farmApp:auth')
        return render(request, RESETPASSWORD_PAGE, {"login_link": login_link.__str__()})

    if request.method == "POST":
        password = request.POST['password']
        re_pass = request.POST['confirm_password']
        if password != re_pass:
            messages.error("password and confirm password not match")
            return render(request, RESETPASSWORD_PAGE)
        user.set_password(password)
        user.save()
    return redirect(reverse('farmApp:auth'))


@farmAuth.Farm_login_required_Def
def logout(request):
    response = farmAuth.logoutFarmUser(request, request.farm_user)
    messages.success(request, "Logout Succsufully")
    return redirect(reverse('farmApp:auth'))
