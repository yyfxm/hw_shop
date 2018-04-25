from django.db import models

# Create your models here.

class Order(models.Model):
	oid = models.CharField(max_length=20,primary_key=True)  #订单号
	user = models.ForeignKey('df_user.User',on_delete=models.CASCADE)
	odate = models.DateTimeField(auto_now=True)   #订单提交时间
	oisPay = models.BooleanField(default=False)
	ototal = models.DecimalField(max_digits=6,decimal_places=2)
	oadr = models.CharField(max_length=150)

class OrderDetail(models.Model):
	goods = models.ForeignKey('df_goods.GoodInfo',on_delete=models.CASCADE)
	order = models.ForeignKey(Order,on_delete=models.CASCADE)
	price = models.DecimalField(max_digits=6,decimal_places=2)
	count = models.IntegerField()
	
