"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import logout
from mysite.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^$', personal_cabinet),
    url(r'^admin/', admin.site.urls),
    url(r'^top/', top_cashiers),
    url(r'^employ/(\d+)/', employ),
    url(r'^history/(\d+)/', top_history),
    url(r'^history_r/(\d+)/', history_r),
    url(r'^topr/', top_restaurants),
    url(r'^order/(\d+)/(\d+)/',order),
    url(r'^accounts/login/$', login2),
    url(r'^logout/$', logout,{'next_page': '/'}),]+static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
