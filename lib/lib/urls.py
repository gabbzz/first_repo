"""lib URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from myapp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),


    url(r'^issue/$', views.issue),
    url(r'^login/$', views.login),
    url(r'^register/$', views.register),
    url(r'^student_dashboard/$', views.student_dashboard),
    url(r'^lib_dashboard/$', views.lib_dashboard),
    url(r'^logout/$', views.logout),
    url(r'^summary/$', views.summary),
    url(r'^search/$', views.search),
    url(r'^profile/$', views.profile),
    url(r'^book_is_issued/$', views.book_is_issued),
    url(r'^return_book/$', views.return_book),
    url(r'^delete_book/$', views.delete_book),
    url(r'^shelf_books/$', views.shelf_books),
    url(r'^table_books/$', views.table_books),
    url(r'^returned_books/$', views.returned_books),
    url(r'^issued_books/$', views.issued_books),
    url(r'^move_all_to_shelf/$', views.move_all_to_shelf),
    url(r'^reciept/$', views.reciept),

    
    

    
]
