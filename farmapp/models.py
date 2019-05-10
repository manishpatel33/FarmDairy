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

    def createFarmUser(self, email, full_name, contact_no, password):
        if not validateHelper.validate_email(email):
            raise Exception('Email Is Not Valid')

        self.email = email
        self.full_name = full_name
        self.contact_no = contact_no
        self.set_password(password)
        self.is_active = True
        self.save()


class cropentry(models.Model):

    class Meta:
        db_table = 'crop_entry'

    date = models.DateField(default=datetime.now)
    crop_name = models.CharField(max_length=20, blank=True, null=True)
    area = models.FloatField(null=False, blank=False)
    user_id = models.IntegerField(null=False, blank=False)

    def createEntry(self, date, crop_name, area, user_id):
        self.date = date
        self.crop_name = crop_name
        self.area = area
        self.user_id = user_id
        self.save()




class cropexpenses(models.Model):

    class Meta:
        db_table = 'crop_expenses'

    date = models.DateField(default=datetime.now)
    to_give_whom = models.CharField(max_length=100)
    crop_id = models.IntegerField()
    expenses_name = models.TextField()
    expenses_amount = models.FloatField()

    def createExpenses(self, date, crop_id, to_give_whom, expenses_name, expenses_amount):
        self.date = date
        self.to_give_whom = to_give_whom
        self.expenses_name = expenses_name
        self.expenses_amount = expenses_amount
        self.crop_id = crop_id
        self.save()


class cropsold(models.Model):

    class Meta:
        db_table = 'crop_sold'

    date = models.DateField(default=datetime.now)
    sold_to_whom = models.CharField(max_length=100)
    sold = models.CharField(max_length=12)
    crop_weight = models.CharField(max_length=12)
    crop_id = models.IntegerField()

    def createSold(self, sold_to_whom, date, sold, crop_weight, crop_id):
        self.sold_to_whom = sold_to_whom
        self.date = date
        self.crop_weight = crop_weight
        self.sold = sold
        self.crop_id = crop_id
        self.save()
