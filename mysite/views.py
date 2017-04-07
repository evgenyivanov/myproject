from operator import itemgetter
import datetime
import pyodbc

from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
#from django.forms.util import ErrorList
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.models import User
from django.db.models import Count,Sum
from django.utils.timezone import utc
#from django.db.models.query import QuerySet
from django.contrib.auth.decorators import user_passes_test
from mysite.models import *
from mysite.forms import *

@user_passes_test(lambda u: u.is_superuser)
def employ(request,id):
    try:
        cnx = pyodbc.connect(
              DRIVER = 'FreeTDS',
              TDS_Version = '7.0',
              clientCharset = 'UTF8',
              PORT = '',
              SERVER = '',
              DATABASE = '',
              UID = '',
              PWD = '')
        cursor = cnx.cursor()

        request_text = """SELECT
                          EMP.SIFR AS SIFR,
                          EMP.CardCode AS CARDCODE,
                          EMP.NAME AS NAME
                          FROM EMPLOYEES AS EMP
                          WHERE EMP.CARDCODE ='"""+str(id)+"'"
        
        
        result = cursor.execute(request_text)
        
        L=[]
        for el in result:
            L.append([el[0],el[1],el[2]])

        d={'L':L}
        t = get_template("employ.html")
        c = Context(d)
        html = t.render(c)
        return HttpResponse(html)
    except Exception as e:
            return HttpResponse(str(e))

@user_passes_test(lambda u: u.is_superuser)
def order(request,number,server):
   
    L = Orders.objects.filter(number = number).filter(server = server)
    name = number + '/'+ server
    total = L.aggregate(Sum('paysum'))['paysum__sum']
    d = {'name':name,'L':L,'total':total}
    t = get_template('order.html')
    c = Context(d)
    html = t.render(c)
    return HttpResponse(html)    

def top_cashiers(request):
    current_game  = Games.objects.latest('start_game')
    L= Sales.objects.filter(game=current_game)
   
    result = list(L.values('cashier__user').annotate(count1=Sum('count_dishers')).annotate(count_total=Count('number')).annotate(summa_total=Sum('summa')))
    top_list=[]
    for i in range(len(result)):
        el = result[i]

        cashier = Cashiers.objects.filter(user=el['cashier__user'])[0]
        restaurant = L.filter(cashier = cashier)[0].restaurant
        if int(round(el['summa_total']/float(el['count_total']),0))> int(restaurant.middle_check):
           a = '<img width="35" height="35"  src="/static/up.jpg">'
        else:
           a = '<img width="35" height="35"  src="/static/down.jpg">'
       
        img = '<img class="img-rounded" width="52" height="52"  src="'+cashier.model_pic.url+'">'
        top_list.append([img,cashier.fullname(),round(el['count1']/float(el['count_total']),4),restaurant,int(round(el['summa_total']/float(el['count_total']),0)),int(restaurant.middle_check),a])
    top=sorted(top_list, key=itemgetter(2),reverse=True)
    index=0
    for i in range(len(top)):
        index=index+1
        top[i].insert(0,index)
        
    start = str(current_game.start_game)[0:10]
    start = start[8:10]+'-'+start[5:7]+'-'+start[0:4]
    finish = str(current_game.finish)[0:10]
    finish = finish[8:10]+'-'+finish[5:7]+'-'+finish[0:4]
    d={'L':top,'name':current_game.name,'description':current_game.description,'start':start,'finish':finish}
    t = get_template("top.html")
    c = Context(d)
    html = t.render(c)
    return HttpResponse(html)


@user_passes_test(lambda u: u.is_superuser)
def top_history(request,id):
    current_game  = Games.objects.filter(id=id)[0]
    L= Sales.objects.filter(game=current_game)
   
    result = list(L.values('cashier__user').annotate(count1=Sum('count_dishers')).annotate(count_total=Count('number')).annotate(summa_total=Sum('summa')))
    top_list=[]
    for i in range(len(result)):
        el = result[i]
        try:
            cashier = Cashiers.objects.filter(user=el['cashier__user'])[0]
        except:
            return HttpResponse(el['cashier__user'])
        
        try:
            restaurant = L.filter(cashier = cashier)[0].restaurant
        except:
            return HttpResponse(cashier)
        if int(round(el['summa_total']/float(el['count_total']),0))> int(restaurant.middle_check):
           a = '<img width="35" height="35"  src="/static/up.jpg">'
        else:
           a = '<img width="35" height="35"  src="/static/down.jpg">' 
       
        img = '<img class="img-rounded" width="52" height="52"  src="'+cashier.model_pic.url+'">'
        top_list.append([img,cashier.fullname(),round(el['count1']/float(el['count_total']),4),cashier.user.username,cashier.shifr,restaurant,int(el['count1']),int(el['count_total']),int(round(el['summa_total']/float(el['count_total']),0)),int(restaurant.middle_check),a])
    top=sorted(top_list, key=itemgetter(2),reverse=True)
    index=0
    for i in range(len(top)):
        index=index+1
        top[i].insert(0,index)
        
    start = str(current_game.start_game)[0:10]
    start = start[8:10]+'-'+start[5:7]+'-'+start[0:4]
    finish = str(current_game.finish)[0:10]
    finish = finish[8:10]+'-'+finish[5:7]+'-'+finish[0:4]
    d={'L':top,'name':current_game.name,'description':current_game.description,'start':start,'finish':finish}
    t = get_template("history.html")
    c = Context(d)
    html = t.render(c)
    return HttpResponse(html)


def top_restaurants(request):
    current_game  = Games.objects.latest('start_game')
    L= Sales.objects.filter(game=current_game)
   
    result = list(L.values('restaurant').annotate(count1=Sum('count_dishers')).annotate(count_total=Count('number')).annotate(summa_total=Sum('summa')))
    top_list=[]
    for i in range(len(result)):
        el = result[i]

        restaurant = Restaurants.objects.filter(id = el['restaurant'])[0]
        if int(round(el['summa_total']/float(el['count_total']),0))> int(restaurant.middle_check):
           a = '<img width="35" height="35"  src="/static/up.jpg">'
        else:
           a = '<img width="35" height="35"  src="/static/down.jpg">'   
         
        
        top_list.append([restaurant.title,round(el['count1']/float(el['count_total']),4),int(round(el['summa_total']/float(el['count_total']),0)),int(restaurant.middle_check),a])
    top=sorted(top_list, key=itemgetter(1),reverse=True)
    index=0
    for i in range(len(top)):
        index=index+1
        top[i].insert(0,index)
        
    start = str(current_game.start_game)[0:10]
    start = start[8:10]+'-'+start[5:7]+'-'+start[0:4]
    finish = str(current_game.finish)[0:10]
    finish = finish[8:10]+'-'+finish[5:7]+'-'+finish[0:4]
    d={'L':top,'name':current_game.name,'description':current_game.description,'start':start,'finish':finish}
    t = get_template("topr.html")
    c = Context(d)
    html = t.render(c)
    return HttpResponse(html)

def history_r(request,id):
    current_game  = Games.objects.filter(id=id)[0]
    L= Sales.objects.filter(game=current_game)
   
    result = list(L.values('restaurant').annotate(count1=Sum('count_dishers')).annotate(count_total=Count('number')).annotate(summa_total=Sum('summa')))
    top_list=[]
    for i in range(len(result)):
        el = result[i]

        restaurant = Restaurants.objects.filter(id = el['restaurant'])[0]
        if int(round(el['summa_total']/float(el['count_total']),0))> int(restaurant.middle_check):
           a = '<img width="35" height="35"  src="/static/up.jpg">'
        else:
           a = '<img width="35" height="35"  src="/static/down.jpg">'
         
        
        top_list.append([restaurant.title,round(el['count1']/float(el['count_total']),4),int(round(el['summa_total']/float(el['count_total']),0)),restaurant.middle_check,a])
    top=sorted(top_list, key=itemgetter(1),reverse=True)
    index=0
    for i in range(len(top)):
        index=index+1
        top[i].insert(0,index)
        
    start = str(current_game.start_game)[0:10]
    start = start[8:10]+'-'+start[5:7]+'-'+start[0:4]
    finish = str(current_game.finish)[0:10]
    finish = finish[8:10]+'-'+finish[5:7]+'-'+finish[0:4]
    d={'L':top,'name':current_game.name,'description':current_game.description,'start':start,'finish':finish}
    t = get_template("topr.html")
    c = Context(d)
    html = t.render(c)
    return HttpResponse(html)


@login_required
@csrf_protect
def personal_cabinet(request):

    try:
        fullname = request.user.first_name+' '+request.user.last_name
    except:
       fullname=''


    current_game  =  Games.objects.latest('start_game')


    try:
        current_cashier = Cashiers.objects.filter(user=request.user)[0]
        current_restaurant = Sales.objects.filter(game=current_game).filter(cashier=current_cashier).reverse()[0].restaurant
        restaurant_name=current_restaurant.title
        restaurant_count=current_restaurant.checks_per_hour
        restaurant_summa=current_restaurant.middle_check

    except:
        restaurant_name=""
        restaurant_count=0
        restaurant_summa=0

    summa_sales=0
    count_checks=0
    reiting=0

    L= Sales.objects.filter(game=current_game)
    result = list(L.values('cashier__user').annotate(count1=Sum('count_dishers')).annotate(count_total=Count('number')).annotate(summa_total=Sum('summa_normal')))
    top_list=[]

    for i in range(len(result)):
        el = result[i]
        top_list.append([el['cashier__user'],el['count1']/float(el['count_total'])])
        if el['cashier__user'] == request.user.id:
            summa_sales = el['summa_total']
            count_checks = el['count_total']




    top=sorted(top_list, key=itemgetter(1),reverse=True)
    index=0
    for i in range(len(top)):
        index=index+1
        if top[i][0]==request.user.id:
            reiting= index
        top[i].insert(0,index)

    L= Sales.objects.filter(game=current_game).filter(cashier__user=request.user.id)


    try:
        start_sales = L[0].date
        finish_sales = datetime.datetime.utcnow().replace(tzinfo=utc)
        delta = finish_sales - start_sales
        hours= int(delta.total_seconds()//3600)
    except:
        hours = 0

    d = {'fullname':fullname,'game_name':current_game.name,'game_description':current_game.description,'restaurant_name':restaurant_name,}
    d.update({'restaurant_count':restaurant_count*hours,'restaurant_summa':restaurant_summa})
    d.update({'reiting':str(reiting)+"/"+str(len(top))})
    if count_checks==0:
        d.update({'middle_check':0})
    else:
         d.update({'middle_check': round(summa_sales/count_checks,1)})

    d.update({'count_checks':count_checks})
    d.update({'img_f':ImageUploadForm})

    if request.method == "POST":
       form = ImageUploadForm(request.POST, request.FILES)
       if form.is_valid():
          
          current_cashier.model_pic = form.cleaned_data['image']
          current_cashier.save()

    if request.method == 'GET':
       d.update({'f':ChangePassword,'change':False,'passw_text':0})
    elif request.method == 'POST' and 'paasword' in request.POST:
        if request.POST['password'] != request.POST['password_repeat']:
            d.update({'f':ChangePassword,'change':True,'passw_text': False})
        else:
            usr = request.user
            usr.set_password(request.POST['password'])
            usr.save()
            d.update({'f':ChangePassword,'change':True,'passw_text':True})
    return render(request,'cabinet.html',d)
    

@csrf_protect
def login2(request):
    if request.method == 'POST':
        f = LoginForm(request.POST)
        login_ = request.POST['login']
        password = request.POST['password']
        user = authenticate(username=login_, password=password)
        if  user is not None:
            login(request, user)
            return redirect('/')
        else:
            d = {'f': f,'errors':'Error: login and password'}
            t = get_template("login.html")
            c = Context(d)
            html = t.render(c)
            return HttpResponse(html)
    else:
       f = LoginForm
       d = {'f': f}

       return render(request, "login.html", d)
