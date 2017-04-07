
from datetime import datetime, timedelta
from operator import itemgetter
from django.core.management.base import BaseCommand,CommandError
from django.db.models import Count,Sum
from django.utils.timezone import utc
from mysite.models import *
import pyodbc

class Command(BaseCommand):
    help='*******'
    def handle(self, *args, **options):
        date = datetime.now() - timedelta(hours = 0)
        date_string = str(date.year)+"/"
        if len(str(date.month))==1:
            date_string = date_string + "0"+str(date.month)+"/"
        else:
            date_string = date_string+str(date.month)+"/"
  
        if len(str(date.day))==1:
            date_string = date_string+"0"+str(date.day)
        else:
            date_string = date_string + str(date.day)
        date_string = date_string + " 00:00:01"           
       
        current_game  = Games.objects.latest('start_game')
        current_restaurant = Restaurants.objects.filter(shifr = 4 )[0]
        my_likes = Playing_dishes.objects.filter(game=current_game)
        my_likes_list = []
        for el in my_likes:
            my_likes_list.append(el.shifr)
            
            
      
        try:
            cnx = pyodbc.connect(
                  DRIVER = 'FreeTDS',
                  TDS_Version = '7.0',
                  ClientCharset = 'UTF8',
                  PORT ='',
                  SERVER = '',
                  DATABASE = "",
                  UID = '',
                  PWD = '')

            cursor = cnx.cursor()
            

            request_text = """SELECT 
                           MENU.CODE AS CODE,
                           MENU.SIFR AS SIFR
                           FROM MENUITEMS AS MENU """

            result = cursor.execute(request_text)
            M = []
            for el in result:               
                if el.CODE in my_likes_list:
                    M.append(str(el.SIFR))
            request_text = """SELECT
                           MF.CODE AS CODE,
                           MF.SIFR AS SIFR
                           FROM MODIFIERS AS MF"""
            for el in result:
                if str(el.CODE) in my_likes_list:
                    M.append(str(el.SIFR))       

       

            request_text = """SELECT 
                             ORD.STARTSERVICE AS TDATE,
                             ORD.ICREATOR AS TCREATOR,
                             ORD.Visit  AS ORDERID,
                             ORD.MidServer AS Server,
                             ORD.ToPaySum AS SUM
                             FROM ORDERS AS ORD
                             WHERE ORD.STARTSERVICE > CONVERT(datetime,'zzz')
                             AND ORD.PAID = 1"""
            
            request_text =  request_text.replace('zzz',date_string)
            
            result = cursor.execute(request_text)
            result_list=[]
            for row in result:
                result_list.append([row.ORDERID,row.TCREATOR,row.SUM,row.TDATE,row.Server])
                self.stdout.write(str(row.TCREATOR))

            for row in result_list:
               L = Cashiers.objects.filter(shifr = row[1])
             
                            
               if len(L)>0:
                                      
                   L2 = Sales.objects.filter(restaurant = current_restaurant)
                   if len(L2.filter(number = row[0]).filter(server = row[4]))==0:
                       
                       obj = Sales()
                       obj.number = row[0]
                       obj.server = row[4]
                       obj.date  =  datetime.strptime(str(row[3]),'%Y-%m-%d %H:%M:%S').replace(tzinfo=utc)
                       obj.game = current_game
                       obj.restaurant = current_restaurant
                       obj.cashier = L[0]
                       obj.summa = row[2]
                       obj.summa_normal = float(row[2]) * current_restaurant.p
                       
                       request_text = """SELECT
                                         DISHES.SIFR AS SIFR,
                                         DISHES.Quantity AS Quant,
                                         DISHES.PaySum AS PaySum,
                                         MENUITEMS.Name AS Name
                                         FROM SESSIONDISHES AS DISHES
                                         LEFT JOIN MENUITEMS ON DISHES.SIFR = MENUITEMS.SIFR
                                         WHERE DISHES.Visit =zzz
                                         AND DISHES.MidServer = yyy """
                       request_text= request_text.replace('zzz',str(row[0]))
                       request_text= request_text.replace('yyy',str(row[4]))
                       result2 = cursor.execute(request_text)
                       count =0
                       
                       for dish in result2:
                           obj2 = Orders()
                           obj2.game = obj.game
                           obj2.number = obj.number
                           obj2.server = obj.server
                           obj2.sifr = dish.SIFR
                           obj2.name = dish.Name
                           obj2.quant = dish.Quant
                           obj2.paysum = dish.PaySum
                                                      
                           if str(dish.SIFR) in M:                               
                               count = count + dish.Quant
                               obj2.gaming = True
                           obj2.save()

                       request_text = """SELECT
                                         MF.SIFR AS SIFR
                                         FROM DISHMODIFIERS AS MF
                                         WHERE MF.Visit =zzz"""
                       request_text = request_text.replace('zzz',str(row[0]))
                       result2 = cursor.execute(request_text)
                       for el in result2:
                           if str(el.SIFR) in M:
                              count = count +1
                       obj.count_dishers = count
                       
                       
                       if obj.summa >0:
                           obj.save()
                           self.stdout.write('add')
               
               
               

        except Exception as e:
           self.stdout.write('Error:'+str(e))
        self.stdout.write('SUCCES')
       

