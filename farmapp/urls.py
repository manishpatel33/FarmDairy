from django.urls import path
from farmapp.controllers import authController as Auth
from farmapp.controllers import homeController as Home

app_name = "farmApp"

urlpatterns = [
    path('login/', Auth.AuthView.as_view(), name='auth'),
    path('register/', Auth.registerView.as_view(), name='register'),
    path('index/', Home.index.as_view(), name='home'),
    path('logout/', Auth.logout, name='logout'),
]
