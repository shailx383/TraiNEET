from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class att_1(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    test_name = models.CharField(max_length = 10)

class att_2(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    test_name = models.CharField(max_length = 10)

class att_3(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    test_name = models.CharField(max_length = 10)

class att_4(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    test_name = models.CharField(max_length = 10)
    