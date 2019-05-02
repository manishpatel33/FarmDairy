from django.db import models
import uuid
from passlib.hash import sha256_crypt
from FarmProj.helpers import validateHelper
from django.utils.translation import ugettext_lazy as _


class BaseUser(models.Model):
    
    class Meta:
        abstract = True
    
    unique_code = models.UUIDField(_('uniqueCode'), default=uuid.uuid4, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=False)
    last_name = models.CharField(_('last name'), max_length=30, blank=False)
    mobile_no = models.CharField(_('mobile number'), max_length=16, blank=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    password = models.TextField(_('password'), blank=False)
    is_active = models.BooleanField(_('active'),default=True)

    def set_password(self, password):
        self.password = sha256_crypt.encrypt(password)

    def save(self, *args, **kwargs):
        if not validateHelper.validate_email(self.email):
            raise Exception('Email Is Not Valid')

        if sha256_crypt.identify(self.password):
            super().save(*args, **kwargs)
        else:
            raise Exception('Password Must Be Hashed Before Saving it')
