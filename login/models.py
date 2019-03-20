from django.db import models

# Create your models here.

class ResManage(models.Model):
    resid=models.AutoField(primary_key=True)
    resname=models.CharField(max_length=32)
    resip=models.CharField(max_length=32)
