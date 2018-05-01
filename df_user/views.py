from django.shortcuts import render,redirect
from django.http import *
from .models import User
from hashlib import sha1
from df_goods.models import GoodInfo
from . import user_decorator
from df_order.models import *
from django.core.paginator import *

# Create your views here.

#登录视图
def login(request):
	uname = request.COOKIES.get('uname','')
	pwd = request.COOKIES.get('upwd','')
#获取cookie里的用户民和密码,实现自动填写信息
	context = {'uname':uname,
		   'pwd':pwd,
		   'error':0}
	try:
		url = request.META['HTTP_REFFERE']
		#获取头部的来源地址
	except: url = '/'
	response = render(request,'login.html',context)
	#将请求的URL存入cookie,然后登录跳回原来的地方
	response.set_cookie('url',url)  #在response中写入cookie
	return response


#登录的处理函数
def login_handle(request):
	#接收表单数据
	post = request.POST
	uname = post.get('username')
	upwd1 = post.get('pwd')
	#设置默认值
	remember = post.get('remenber','0')
	
	#加密
	s1 = sha1()   #创建sha1对象
	s1.update(upwd1.encode('utf8'))  #要先把表单的数据编码
	upwd2 = s1.hexdigest
	upwd = upwd2()
	#验证用户是否正确
	user = User.objects.filter(uname=uname).filter(upwd=upwd).first();
	
	if user:
		url = request.COOKIES.get('url','/')  #第二个参数为默认参数,如果URL没有,就跳到首页
		red = HttpResponseRedirect(url)
		#如果用户要求记住密码,则把用户名和密码写入cookie
		if remember == '1':
			red.set_cookie('uname',user.uname)
			red.set_cookie('upwd',upwd1)
		else:
			red.set_cookie('uname','',max_age=-1)
			red.set_cookie('upwd','',max_age=-1)
		#将uname和id写入session用来保持登录状态
		request.session['username'] = uname
		request.session['uid'] = user.id
		return red
	else:
		#如果没有用户,返回错误参数,模板界面,根据错误信息给出提示
		context = {'error': 1,
			   'uname':uname}
		return render(request,'login.html',context)

#用户退出后处理函数
def logout(request):
	request.session.flush()  #清空所有session
	return redirect('/')


#注册页面
def register(request):
	return render(request,'register.html')

#注册页面处理函数
def register_handle(request):
	#接收用户输入
	post = request.POST
	uname = post.get('user_name')
	pwd = post.get('pwd')
	cpwd = post.get('cpwd')
	email = post.get('email')
	if pwd != cpwd:
		return redirect('/user/register')   #密码不同,重定向到注册页面
	#用sha1对密码加密
	s1 = sha1()
	#加密前先对密码编码
	s1.update(pwd.encode('utf8'))
	pwd = s1.hexdigest()
	#存入数据库
	user = User()
	user.uname = uname
	user.upwd = pwd
	user.uemail = email
	user.save()
	print(user.uname)
	return redirect('/user/login')

def register_exist(request):
	uname = request.GET.get('uname')
	count = User.objects.filter(uname=uname).count()
	#返回json字典
	return JsonResponse({'count':count})


#用户中心
@user_decorator.login
def user_center_info(request):
	username = request.session.get('username')
	user = User.objects.filter(uname=username).first()
	
	#获取最近浏览的商品
	goodids = request.COOKIES.get('goodids','')  #取cookie中存的记录
	if goodids != '':
		goodids1 = goodids.split(',')  #拆分为列表
		goods_list = []
		for good_id in goodids1:
			goods = GoodInfo.objects.filter(pk=good_id).first()
			goods_list.append(goods)
	else:
		goods_list = []
	context = {'title':'用户中心',
		   'username':username,
		   'phone':user.uphone,
		   'address':user.uadr,
		   'good_list':goods_list,
		   'tag':1}
	return render(request,'user_center_info.html',context)

def user_center_site(request):
	username = request.session.get('username')
	user = User.objects.filter(uname=username).first()
	if request.method == 'POST':
		adr = request.POST.get('area')
		username = request.POST.get('user')
		phone = request.POST.get('phone')
		user.uadr = adr
		user.uphone = phone
		user.urelname = username
		user.save()
	context = {'adr':user.uadr,
		   'user':user.urelname,
		   'phone':user.uphone,
		   'tag':3}
	return render(request,'user_center_site.html',context)


def user_center_order(request,pindex):
	uid = request.session.get('uid')
	orders = Order.objects.filter(user_id=int(uid)).order_by('-odate')
	paginator = Paginator(orders,2)
	page = paginator.page(int(pindex))
	context = {'tag':2,
		   'page':page,
		   'paginator':paginator,
		  }
	return render(request,'user_center_order.html',context)
	

	
