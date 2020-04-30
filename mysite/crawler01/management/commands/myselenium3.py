from django.core.management.base import BaseCommand, CommandError
from crawler01.models import Tasks as Tasks

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import datetime
import csv
import codecs
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
import sys

class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('tasks_ids', nargs='*', type=int)

    def handle(self, *args, **options):
        if options['tasks_ids']:
            for tasks_id in options['tasks_ids']:
                try:
                    # if Tasks.objects.filter(status='0').count() > 0: 
                    task = Tasks.objects.get(pk=tasks_id)
                except Tasks.DoesNotExist:
                    raise CommandError('Tasks "%s" does not exist' % tasks_id)
                #task.status = 1
                task.opened = False
                task.save()
                self.stdout.write(self.style.SUCCESS('Successfully closed tasks "%s"' % tasks_id))
        else:
            task_count = Tasks.objects.filter(status = '0').count()
            if task_count > 0:
                task = Tasks.objects.filter(status='0').first()
                task.status = 1
                task.save()
                
                user_name = task.user_name
                user_email = task.user_email
                QryCond = task.QryCond
                StartPage = task.StartPage
                StopPage = task.StopPage
                DataType = task.DataType
                TurnOffChrome = task.TurnOffChrome
                HeadlessMode = task.HeadlessMode
                created = task.created
                status = task.status
                taskid = task.id
                print(user_name)
                print(user_email)
                print(QryCond)
                print(StartPage)
                print(StopPage)
                print(DataType)
                print(TurnOffChrome)
                print(HeadlessMode)
                print(created)

                self.mycrawler(task)

                task.status = 2
                task.save()
                print(status)
                print(taskid)



            else:
                self.stdout.write(self.style.SUCCESS('No tasks'))

    def mycrawler(self, task):
        print('hello crawler')
        print(task.user_email)
        # 產生 excel report
        # 寄完成通知信及excel附件
