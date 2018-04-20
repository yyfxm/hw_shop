from django.db import models

# Create your models here.

class Cart(models.Model):
	user = models.ForeignKey('df_user.User',on_delete=models.CASCADE)
	goods = models.ForeignKey('df_goods.GoodInfo',on_delete=models.CASCADE)
	count = models.IntegerField()
