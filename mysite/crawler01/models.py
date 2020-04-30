from django.db import models
from django.contrib import admin

# Create your models here.
class Tasks(models.Model):
    user_name = models.CharField(max_length=200, default='')
    user_email = models.CharField(max_length=200, default='')
    QryCond = models.CharField(max_length=200)
    StartPage = models.IntegerField(default=0)
    StopPage = models.IntegerField(default=0)
    DataType = models.CharField(max_length=10)
    TurnOffChrome = models.CharField(max_length=200)
    HeadlessMode = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10)
    
    # 覆寫 __str__
    def __str__(self):
        return self.QryCond

@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    # list_display = ('id', 'QryCond')
    list_display = [field.name for field in Tasks._meta.fields]
    list_editable = ('user_name','user_email')

# python manage.py makemigrations crawler01
# python manage.py migrate crawler01 0001