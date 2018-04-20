from django.db import models
from tinymce.models import HTMLField

# Create your models here.

class TypeInfo(models.Model):
	ttitle = models.CharField(max_length=20)
	isDelete = models.BooleanField(default=False)
	def __str__(self):
		return self.ttitle

class GoodInfo(models.Model):
	gtitle = models.CharField(max_length=50)
	gpic = models.ImageField(upload_to='df_goods/uploadpics')
	gprice = models.DecimalField(max_digits=5,decimal_places=2)
	isDelete = models.BooleanField(default=False)
	gunit = models.CharField(max_length=20,default='500g')
	gclick = models.IntegerField()  #点击量
	gintro = models.CharField(max_length=100)  #简介
	gdetail = HTMLField()
	gtype = models.ForeignKey("TypeInfo",on_delete=models.CASCADE,)
	gkucun = models.IntegerField(default=0)  #库存
	def __str__(self):
		return self.gtitle
