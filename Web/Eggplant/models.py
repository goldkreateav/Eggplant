from django.db import models


class User(models.Model):
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    type = models.CharField(max_length=2)
    pid = models.CharField(max_length=10, default=0)


class Session(models.Model):
    cookie = models.CharField(max_length=30)
    uid = models.CharField(max_length=30)


class Order(models.Model):
    file = models.CharField(max_length=70)
    client = models.CharField(max_length=30)
    provider = models.CharField(max_length=30)
