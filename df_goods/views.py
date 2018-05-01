from .models import *
from django.shortcuts import render
from django.core.paginator import Paginator,Page
from df_cart.models import Cart
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
	return render(request,'df_goods/index.html',context)

#商品列别界面,要接受多个参数
#1,type id
#2,排序的方式
#3,分页的页码
def list(request,tid,sid,pindex):
	type = TypeInfo.objects.get(pk=int(tid))
	news = type.goodinfo_set.order_by('-id')[0:2]
	if sid == '1':
		good_list = type.goodinfo_set.order_by('-id')  #按时间最新的排列
	if sid == '2':
		good_list = GoodInfo.objects.filter(gtype_id=int(tid)).order_by('-gprice')   #按价格
	if sid == '3':
		good_list = GoodInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick') 
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

#详情页
def detail(request,id):
	goods = GoodInfo.objects.filter(pk=int(id)).first()
	goods.gclick += 1   #点击量+1
	goods.save()
	#返回用于购物车内的商品数量
	cart_count = Cart.objects.filter(user_id=request.session.get('uid',0)).count()
	news = goods.gtype.goodinfo_set.order_by('-id')[0:2]
	context = {'title':goods.gtype.ttitle,
		   'goods':goods,
		   'cart_count':cart_count,
		   'news':news,
		   'guest_cart':1,
		   'typeinfo':goods.gtype,
		  }
	response = render(request,'df_goods/detail.html',context)
	#将浏览信息存入cookie以便最近浏览功能的使用
	#存入cookie的形式为{'goodids':'1,5,6,7,8,9'}
	#id间用逗号隔开
	goodids = request.COOKIES.get('goodids','')
	if goodids != '':
		goodids1 = goodids.split(',')   #按逗号拆分字符串列表
		if goodids1.count(id) >= 1:
			#如果已经存在,删除存在的元素,之后会插入新的
			goodids1.remove(id)
		goodids1.insert(0,id)
		#如果队列长度大于等于6个就删除最后一个,保持最近浏览记录只有5个
		if len(goodids1) >= 6:
			del goodids1[5]
		goodids = ','.join(goodids1)   #再将列表拼接为字符串
	else:  #如果最近浏览中无值,直接添加
		goodids = id
	response.set_cookie('goodids',goodids)
	return response
