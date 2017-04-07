# coding: utf-8
from django.contrib import admin
from django.utils.html import format_html
from mysite.models import *


class Restaurants_lists(admin.ModelAdmin):
    fields = ('title', 'shifr','p','middle_check','checks_per_hour','ip','port','password')
    list_display = ('title', 'shifr','p','middle_check','checks_per_hour','ip','port')
admin.site.register(Restaurants,Restaurants_lists)

class Cashiers_lists(admin.ModelAdmin):
    fields = ('user','shifr','phone','model_pic')
    list_display = ('user', 'shifr','fullname','phone')
admin.site.register(Cashiers,Cashiers_lists)

class Games_lists(admin.ModelAdmin):
    fields = ('name', 'description','start_game','finish')
    list_display = ('name', 'description','start_game','finish','_get_top','_get_topr')
    def _get_top(self, obj):
        return u'<a href="/history/%s/">Топ кассиров</a>' % obj.id
    _get_top.allow_tags = True

    def _get_topr(self, obj):
        return u'<a href="/history_r/%s/">Топ ресторанов</a>' % obj.id
    _get_topr.allow_tags = True
admin.site.register(Games,Games_lists)

class Playing_dishes_lists(admin.ModelAdmin):
    fields = ('game', 'shifr')
    list_display = ('game', 'shifr')
    list_filter = ('game',)
admin.site.register(Playing_dishes,Playing_dishes_lists)

class Sales_lists(admin.ModelAdmin):
    fields = ('number','server', 'date','game','restaurant','cashier','summa','summa_normal','count_dishers')
    list_display = ('number','server', 'date','game_name','restaurant_name','cashier_name','summa','summa_normal','count_dishers','_get_order')
    list_filter = ('game','restaurant')
    search_fields = ['cashier__shifr','summa','number']

    def restaurant_name(self, instance):
        return instance.restaurant.title

    def cashier_name(self, instance):
        return instance.cashier.fullname()

    def game_name(self, instance):
        return instance.game.name

    def _get_order(self,obj):
       param = str(obj.number)+'/'+str(obj.server)
       return u'<a href="/order/%s">Чек</a>' % param
    _get_order.allow_tags = True

admin.site.register(Sales,Sales_lists)

class Orders_lists(admin.ModelAdmin):
   fields=('game','number','server','sifr','gaming','name','quant','paysum')
   list_display=('game','number','server','sifr','gaming','name','quant','paysum')
   list_filter = ('game',)
   search_fields = ['number']

admin.site.register(Orders,Orders_lists)

class Prize_fund_lists(admin.ModelAdmin):
    fields = ('game', 'total_sum')
    list_display = ('game', 'total_sum')
admin.site.register(Prize_fund,Prize_fund_lists)



class Personal_result_lists(admin.ModelAdmin):
    fields = ('game', 'cashier','check_count','check_normal','raiting','percent','summa')
    list_display = ('game', 'cashier','check_count','check_normal','raiting','percent','summa')
    list_filter = ('game', 'cashier','check_count','check_normal','raiting','percent','summa')

admin.site.register(Personal_result,Personal_result_lists)


class Restaurants_raiting_lists(admin.ModelAdmin):
    fields = ('game', 'restaurant','peoples','percent','summa')
    list_display = ('game', 'restaurant','peoples','percent','summa')
    list_filter = ('game', 'restaurant','peoples','percent','summa')

admin.site.register(Restaurants_raiting,Restaurants_raiting_lists)


class Restaurants_result_lists(admin.ModelAdmin):
    fields = ('game', 'cashier','restaurant','summa')
    list_display = ('game', 'cashier','restaurant','summa')
    list_filter = ('game', 'cashier','restaurant','summa')

admin.site.register(Restaurants_result,Restaurants_result_lists)
