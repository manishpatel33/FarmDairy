from farmapp.models import FarmUser
from passlib.hash import sha256_crypt
from FarmProj.helpers import mongoHelper as mongo
from django.http.request import HttpRequest
from django.shortcuts import redirect
from django.urls.base import reverse


Farm_SESSION_KEY = 'Farm_auth_user_id'
Farm_BACKEND_SESSION_KEY = 'Farm_auth_user_backend'
Farm_HASH_SESSION_KEY = 'Farm_auth_user_hash'


def checkFarmUserPassword(farmUser,password):
    hashedpass = farmUser.password
    return sha256_crypt.verify(password,hashedpass)


def loginFarmUser(request,farmUser):
    user_id = str(farmUser.unique_code)
    user_session = mongo.UserSession().create_user_session(user_id)
    request.session[Farm_SESSION_KEY] = str(user_session.id)


def logoutFarmUser(request,farmUser):
    if Farm_SESSION_KEY in request.session:
        user_session = mongo.UserSession().destroy_user_session(request.session[Farm_SESSION_KEY])
        del request.session[Farm_SESSION_KEY]
    else:
        pass
        

def is_FarmUser_authenticated(request):
    if Farm_SESSION_KEY in request.session:
        return True
    return False


def Farm_login_required_Def(function):
    def wrap(request, *args, **kwargs):
        if not isinstance(request,HttpRequest):
            raise RuntimeError(
                "This decorator can only work with django view methods accepting a HTTPRequest as the first parameter")
            
        if Farm_SESSION_KEY in request.session:
            user_session = mongo.UserSession().find_session(request.session[Farm_SESSION_KEY])
            farm_user = type('', (), {})()
            farm_user = FarmUser.objects.get(unique_code=user_session.user_code)
            request.__setattr__("farm_user", farm_user)
            return function(request,*args, **kwargs)
        else:
            response = redirect(reverse('farmApp:home'))
            return response
    return wrap    


def Farm_login_required_Class(function):
    def wrap(self,request, *args, **kwargs):
        if not isinstance(request,HttpRequest):
            raise RuntimeError(
                "This decorator can only work with django view methods accepting a HTTPRequest as the first parameter")
            
        if Farm_SESSION_KEY in request.session:
            user_session = mongo.UserSession().find_session(request.session[Farm_SESSION_KEY])
            farm_user = type('', (), {})()
            farm_user = FarmUser.objects.get(unique_code=user_session.user_code)
            request.__setattr__("farm_user", farm_user)
            return function(self,request,*args, **kwargs)
        else:
            response = redirect(reverse('farmApp:auth'))
            return response
    return wrap
