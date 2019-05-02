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

HOME_PAGE = 'main_theme.html'


class index(View):

    #@farmAuth.Farm_login_required_Class
    def get(self, request):
        return render(request, HOME_PAGE)


