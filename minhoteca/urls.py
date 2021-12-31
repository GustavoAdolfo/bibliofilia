"""minhoteca URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordResetConfirmView
from users.views import password_reset_confirm


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'', include('biblioteca.urls', namespace='biblioteca')),
    url(r'^user/', include('users.urls', namespace='user')),
    url(r'^emprestimos/',
        include('emprestimos.urls', namespace='emprestimos')),
    url(r'^captcha/', include('captcha.urls')),
    # url('^user/', include('django.contrib.auth.urls'))
    # url('', include('django.contrib.auth.urls'))
    # path('reset/<uidb64>/<token>/',
    #      PasswordResetConfirmView.as_view(
    #          template_name="users/password_reset_confirm.html"),
    #      name='password_reset_confirm'),
    path('reset/<uidb64>/<token>/',
         password_reset_confirm,
         name='password_reset_confirm'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
