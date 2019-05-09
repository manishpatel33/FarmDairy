from django.urls import path
from farmapp.controllers import authController as Auth
from farmapp.controllers import homeController as Home

app_name = "farmApp"

urlpatterns = [
    path('login/', Auth.AuthView.as_view(), name='auth'),
    path('register/', Auth.registerView.as_view(), name='register'),
    path('forgetpass/', Auth.forgetpassword.as_view(), name='forgetpass'),
    path('resetpass/<email>/<token>/<ctime>/', Auth.resetpassword, name='resetpass'),
    path('changepassword/', Home.changepassword.as_view(),name='changepassword'),

    path('home/', Home.index.as_view(), name='home'),
    path('profile', Home.profile.as_view(), name='profile'),
    path('entry', Home.entry.as_view(), name='entry'),
    path('history', Home.history.as_view(), name='history'),
    path('sold', Home.sold.as_view(), name='sold'),

    path('logout/', Auth.logout, name='logout'),
]
