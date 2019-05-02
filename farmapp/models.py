from django.db import models
from django.utils.translation import ugettext_lazy as _
from passlib.hash import sha256_crypt
from FarmProj.helpers import validateHelper
from FarmProj.helpers import modelHelper
import uuid
import re
from datetime import datetime


class FarmUser(modelHelper.BaseUser):
    class Meta:
        db_table = 'farm_users'

    def getFarmUserByUniqueCode(self, unique_code):
        return self.objects.get(unique_code=unique_code)

    def getFarmUserById(self, pk):
        return self.objects.get(pk=pk)

    def getFarmUserByEmail(self, email):
        return self.objects.get(email=email)

    def createFarmUser(self, email, first_name, last_name, mobile_no, password):
        if not validateHelper.validate_email(email):
            raise Exception('Email Is Not Valid')

        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.mobile_no = mobile_no
        self.set_password(password)
        self.is_active = True
        self.save()
