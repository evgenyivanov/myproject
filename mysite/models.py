#  coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class Restaurants(models.Model):
    class Meta:
        verbose_name = 'Рестораны'
        verbose_name_plural = 'Рестораны'

    title = models.CharField(max_length=200)
    shifr = models.IntegerField()
    p = models.FloatField()
    middle_check = models.FloatField(default=1.0)
    checks_per_hour = models.FloatField(default=1.0)
    ip = models.CharField(max_length = 20,blank = True)
    port = models.CharField(max_length=4,blank = True)
    password = models.CharField(max_length=20,blank = True)


    def __unicode__(self):
        return self.title



class Cashiers(models.Model):
    user = models.ForeignKey(User)
    shifr = models.IntegerField(unique=True)
    phone = PhoneNumberField(blank = True)
    model_pic = models.ImageField(upload_to = 'pic_folder', default = 'pic_folder/no-img.jpg')

    class Meta:
        verbose_name = 'Кассиры'
        verbose_name_plural = 'Кассиры'

    def fullname(self):
        return self.user.last_name+' '+self.user.first_name

    def __unicode__(self):
        return self.user.last_name+' '+self.user.first_name

    


class Games(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    start_game = models.DateTimeField()
    finish = models.DateTimeField()

    class Meta:
        verbose_name = 'Игры'
        verbose_name_plural = 'Игры'

    def __unicode__(self):
        return self.name

  #  def top(self):
   #     return '<a href="/history/'+str(self.id)+'/">Топ кассиров</a>    
class Playing_dishes(models.Model):
    game = models.ForeignKey(Games)
    shifr = models.IntegerField()

    class Meta:
        verbose_name = 'Игровые блюда'
        verbose_name_plural = 'Игровые блюда'

class Sales(models.Model):
    number = models.IntegerField() 
    #Номер чека
    server = models.IntegerField()
    date = models.DateTimeField()
    game = models.ForeignKey(Games)
    restaurant = models.ForeignKey(Restaurants)
    cashier = models.ForeignKey(Cashiers)
    summa = models.FloatField()
    summa_normal = models.FloatField()
    count_dishers = models.FloatField(blank=True)

    class Meta:
        verbose_name = 'Продажи'
        verbose_name_plural = 'Продажи'

class Orders(models.Model):
    game = models.ForeignKey(Games)
    number = models.IntegerField()
    server = models.IntegerField()
    sifr = models.CharField(max_length = 20)
    gaming = models.BooleanField(default = False)
    name = models.CharField(max_length = 200,blank = True)
    quant = models.IntegerField()
    paysum = models.FloatField()

    class Meta:
       verbose_name = 'Чеки'
       verbose_name_plural = 'Чеки'

class Prize_fund(models.Model):
    game = models.ForeignKey(Games)
    total_sum = models.IntegerField()

    class Meta:
        verbose_name = 'Призовой фонд'
        verbose_name_plural = 'Призовой фонд'

class Personal_result(models.Model):
    game = models.ForeignKey(Games)
    cashier = models.ForeignKey(Cashiers)
    check_count = models.IntegerField()
    check_normal = models.IntegerField()
    raiting = models.FloatField()
    percent = models.FloatField()
    summa = models.FloatField()
   
   
    class Meta:
        verbose_name = 'Результат: личный рейтинг'
        verbose_name_plural = 'Результат: личный рейтинг'

class Restaurants_raiting(models.Model):
    game = models.ForeignKey(Games)
    restaurant = models.ForeignKey(Restaurants)
    peoples = models.FloatField()
    percent = models.FloatField()
    summa = models.FloatField()

    class Meta:
        verbose_name = 'Результат: рейтинг ресторанов'
        verbose_name_plural = 'Результат: рейтинг ресторанов'

class Restaurants_result(models.Model):
    game = models.ForeignKey(Games)
    cashier = models.ForeignKey(Cashiers)
    restaurant = models.ForeignKey(Restaurants)
    summa = models.FloatField()

    class Meta:
        verbose_name = 'Результат: по ресторану'
        verbose_name_plural = 'Результат: по ресторану'




