from .models import *
from django.shortcuts import render

# Create your views here.
def index(request):
	context = {'guest_cart':1,
		   'title':'首页'}
	#获得最火的四个产品
	hot = GoodInfo.objects.all().order_by('-gclick')[0:4]
	context.setdefault('hot',hot)
	
	#获得各分类下的点击商品
	#先获得所有分类
	typelist = TypeInfo.objects.all()
	for i in range(len(typelist)):
		#获得type对象
		type = typelist[i]
		goods1 = type.goodinfo_set.order_by('-id')[0:4]
		goods2 = type.goodinfo_set.order_by('-gclick')[0:4]
		key1 = 'type' + str(i)   #根据id倒叙排列
		key2 = 'type' + str(i) + str(i)   #根据点击量倒叙排列
		context.setdefault(key1,goods1)  #添加键值对
		context.setdefault(key2,goods2)
	print(context)
	return render(request,'df_goods/index.html',context)

#商品列别界面,要接受多个参数
#1,type id
#2,排序的方式
#3,分页的页码
def list(request,tid,sid,pindex):
	from django.core.paginator import Paginator,Page
	type = TypeInfo.objects_set.get(pk=int(tid))
	news = type.goodinfo_set.order_by('-id')[0:2]
	if sid == '1':
		good_list = type.goodinfo_set.order_by('-id')  #按时间最新的排列
	if sid == '2':
		good_list = GoodInfo.objects.filter(gtype_id=int(tid).order_by('-gprice'))   #按价格
	if sid == '3':
		good_list = GoodInfo.objects.filter(gtype_id=int(tid).order_by('-gclick'))  
	#创建paginator分页对象
	paginator = Paginator(good_list,10)
	#返回page对象,包含商品信息
	page = paginator.page(int(pindex))
	context = {'title':'商品列表',
		   'guest_cart':1,
		   'page':page,
		   'paginator':paginator,
		   'typeinfo':type,
		   'sort':sid,
		   'news':news,
		}
	return render(request,'df_goods/list.html',context)

