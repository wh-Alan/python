from django.db import models

# Create your models here.

class Book(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    price=models.DecimalField(max_digits=8,decimal_places=2)
    publish_date=models.DateField()
    is_valid = models.IntegerField(default=1)
    publish=models.ForeignKey(to='Publish',to_field='id',on_delete=models.CASCADE)
    authors=models.ManyToManyField(to='Author')


class Author(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    age=models.IntegerField()
    is_valid = models.IntegerField(default=1)
    author_detail=models.OneToOneField(to='AuthorDetail',to_field='id',unique=True,on_delete=models.CASCADE)

class AuthorDetail(models.Model):
    id=models.AutoField(primary_key=True)
    phone=models.BigIntegerField()
    birthday = models.DateField()
    addr = models.CharField(max_length=64)

class Publish(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    is_valid = models.IntegerField(default=1)
    email = models.EmailField()

