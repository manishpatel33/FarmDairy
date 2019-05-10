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
from farmapp.models import FarmUser, cropentry, cropsold, cropexpenses
from django.core.exceptions import ValidationError
from FarmProj.helpers import validateHelper
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import FileSystemStorage
from datetime import datetime

HOME_PAGE = 'index.html'
PROFILE_PAGE = 'profile.html'
ENTRY_PAGE = 'entry.html'
EXPENSES_PAGE = 'expenses.html'
SOLD_PAGE = 'sold.html'
HISTORY_PAGE = 'history.html'


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


class entry(View):

    @farmAuth.Farm_login_required_Class
    def get(self, request):
        return render(request, ENTRY_PAGE)

    def validate_data(self, request):
        data = {}

        date = request.POST.get('date', '')
        if date == '':
            raise ValidationError(_('date Is Empty'))
        data['year'] = date

        crop_name = request.POST.get('crop_name', '')
        if crop_name == '':
            raise ValidationError(_('crop name Is Empty'))
        data['crop_name'] = crop_name

        area = request.POST.get('area', '')
        if int(area) < 0:
           raise ValidationError(_('Enter valid area'))
        data['area'] = area

        return data

    @farmAuth.Farm_login_required_Class
    def post(self, request):

        try:
            data = self.validate_data(request)
        except ValidationError as e:
            messages.error(request, e.message)
            return HttpResponseRedirect(reverse('farmApp:entry'))
        except Exception as e:
            pass
        user_id = request.farm_user.id
        try:
            farm = cropentry().createEntry(date=data['year'], area=data['area'],
                                           crop_name=data['crop_name'], user_id=user_id)

            messages.success(request, "data saved successfully.")
        except Exception as e:
            messages.error(request, e)

        return redirect(request.META['HTTP_REFERER'])


class expenses(View):

    @farmAuth.Farm_login_required_Class
    def get(self, request):
        detail = cropentry.objects.filter(user_id=request.farm_user.id)
        list1 = []
        list2 = []
        for i in detail:
            list1.append(i.date)
            list2.append(i.crop_name)
        list1 = list(dict.fromkeys(list1))
        list2 = list(dict.fromkeys(list2))
        return render(request, EXPENSES_PAGE, {'list1': list1, 'list2': list2})

    def validate_data(self, request):
        data = {}

        date = request.POST.get('date', '')
        if date == '':
            raise ValidationError(_('date Is Empty'))
        data['date'] = date

        for_which_crop = request.POST.get('for_which_crop', '')
        if for_which_crop == '':
            raise ValidationError(_('to give whom Is Empty'))
        data['for_which_crop'] = for_which_crop

        to_give_whom = request.POST.get('to_give_whom', '')
        if to_give_whom == '':
            raise ValidationError(_('to give whom Is Empty'))
        data['to_give_whom'] = to_give_whom

        expenses_name = request.POST.get('expenses_name', '')
        if expenses_name == '':
            raise ValidationError(_('expenses name Is Empty'))
        data['expenses_name'] = expenses_name

        expenses_amount = request.POST.get('expenses_amount', '')
        if expenses_amount == '':
            raise ValidationError(_('expenses amount Is Empty'))
        data['expenses_amount'] = expenses_amount

        return data

    def post(self, request):

        try:
            data = self.validate_data(request)
        except ValidationError as e:
            messages.error(request, e.message)
            return HttpResponseRedirect(reverse('farmApp:expenses'))
        except Exception as e:
            pass
        crop_id = cropentry.objects.get(crop_name=data['for_which_crop'])
        print(crop_id)
        try:
            farm = cropexpenses().createExpenses(date=data['date'],
                                                 expenses_name=data['expenses_name'],
                                                 expenses_amount=data['expenses_amount'],
                                                 to_give_whom=data['to_give_whom'],
                                                 crop_id=crop_id.id
                                                 )
            messages.success(request, "data saved successfully.")
        except Exception as e:
            messages.error(request, e)

        return redirect(request.META['HTTP_REFERER'])


class sold(View):

    @farmAuth.Farm_login_required_Class
    def get(self, request):
        detail = cropentry.objects.filter(user_id=request.farm_user.id)
        return render(request, SOLD_PAGE, {'detail': detail})

    def validate_data(self, request):
        data = {}

        date = request.POST.get('date', '')
        if date == '':
            raise ValidationError(_('date Is Empty'))
        data['date'] = date

        which_crop = request.POST.get('which_crop', '')
        if which_crop == '':
            raise ValidationError(_('which crop Is Empty'))
        data['which_crop'] = which_crop

        sold_to_whom = request.POST.get('sold_to_whom', '')
        if sold_to_whom == '':
            raise ValidationError(_('Sold to whom Is Empty'))
        data['sold_to_whom'] = sold_to_whom

        crop_sold = request.POST.get('crop_sold', '')
        if crop_sold == '':
            raise ValidationError(_('crop sold Is Empty'))
        data['sold'] = crop_sold

        crop_weight = request.POST.get('crop_weight', '')
        if crop_weight == '':
            raise ValidationError(_('crop weight Is Empty'))
        data['crop_weight'] = crop_weight

        return data

    def post(self, request):

        try:
            data = self.validate_data(request)
        except ValidationError as e:
            messages.error(request, e.message)
            return HttpResponseRedirect(reverse('farmApp:sold'))
        except Exception as e:
            pass

        crop_id = cropentry.objects.get(crop_name=data['which_crop'])

        try:
            farm = cropsold().createSold(sold=data['sold'], sold_to_whom=data['sold_to_whom'],
                                         crop_weight=data['crop_weight'],
                                         crop_id=crop_id.id,date=data['date'])
            messages.success(request, "data saved successfully.")
        except Exception as e:
            messages.error(request, e.__str__())

        return redirect(request.META['HTTP_REFERER'])


class history(View):

    @farmAuth.Farm_login_required_Class
    def get(self, request):
        detail = cropentry.objects.filter(user_id=request.farm_user.id)
        list1 = []
        list2 = []

        for i in detail:
            list1.append(i.date)
            list2.append(i.crop_name)
        list1 = list(dict.fromkeys(list1))
        list2 = list(dict.fromkeys(list2))
        return render(request, HISTORY_PAGE, {'list2': list2, 'list1': list1})

    def validate_data(self, request):
        data = {}

        choose_date = request.POST.get('choose_date', '')
        if choose_date == '':
            raise ValidationError(_('date Is Empty'))
        data['choose_date'] = choose_date

        crop_name = request.POST.get('crop_name', '')
        if crop_name == '':
            raise ValidationError(_('crop name Is Empty'))
        data['crop_name'] = crop_name

        return data

    def post(self, request):

        try:
            data = self.validate_data(request)
        except ValidationError as e:
            messages.error(request, e.message)
            return HttpResponseRedirect(reverse('farmApp:history'))
        except Exception as e:
            pass

        d1 = cropentry.objects.get(crop_name=data['crop_name'], date=data['choose_date'])
        selected_data = cropexpenses.objects.filter(crop_id=d1.id)

        return render(request, HISTORY_PAGE, {'selected_data': selected_data})
