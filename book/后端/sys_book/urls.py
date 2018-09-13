"""sys_book URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from app01.controllers import book,author,publish
urlpatterns = [
    path('book/list', book.list.index),
    path('book/add', book.add.index),
    path('book/update', book.update.index),
    path('book/delete', book.delete.index),
    path('author/list', author.list.index),
    path('author/add', author.add.index),
    path('author/update', author.update.index),
    path('author/delete', author.delete.index),
    path('publish/list', publish.list.index),
    path('publish/add', publish.add.index),
    path('publish/update', publish.update.index),
    path('publish/delete', publish.delete.index),
    path('', book.list.index),
]
