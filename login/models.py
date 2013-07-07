from django.db import models

class login(models.Model):
    user_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)