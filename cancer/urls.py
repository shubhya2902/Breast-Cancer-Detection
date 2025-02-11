from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',views.index, name='index'),

    path('signup/', views.signupuser, name="signup"),
    path('login/', views.loginuser, name="login"),
    path('logout/', views.logoutuser, name="logout"),

    path('otp_login/', views.otp_login, name="otp_login"),
    path('check_mail/', views.check_mail, name="check_mail"),

    path('home/',views.home,name='home'),
    path('users/',views.users,name='users'),
    path('about/', views.about, name='about'),

    path('predict/',views.predict,name="predict"),
    path('yes/', views.yes, name="yes"),
    path('no/', views.no, name="no"),

    path('forget_password/',views.forget_password,name="forget_password"),
    path('update_password/',views.update_password,name="update_password"),
    path('verify_reset_otp/',views.verify_reset_otp,name="verify_reset_otp"),


]


from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
