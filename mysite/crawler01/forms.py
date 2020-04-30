from django import forms
from .models import Tasks
from django.utils.translation import gettext_lazy as _

# ModelForm
class TasksForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = '__all__'
        # 新增 labels 對應
        labels = {
            'user_name': _('姓名'),
            'user_email': _('Email'),
        }

# DjangoForm
class RawTasksForm(forms.Form):
    # user_name = forms.CharField(label = '*姓名', help_text='請輸入姓名')
    user_email = forms.EmailField(label = '*Email')
    QryCond = forms.CharField(label = '*城市地區街道')
    StartPage = forms.IntegerField(label = '*開始頁次', initial='1')
    StopPage = forms.IntegerField(label = '*結束頁次', initial='0', help_text='0 代表全部，搜尋至最後一頁')

    DataType = forms.CharField(label = '*資料種類', initial='',disabled='true', help_text='以下請至少勾選一種',required='false')
    DataType_cmpyType = forms.BooleanField(label = '公司',initial='true')
    DataType_brCmpyType = forms.BooleanField(label = '分公司')
    DataType_busmType = forms.BooleanField(label = '商業')
    DataType_factType = forms.BooleanField(label = '工廠')
    DataType_lmtdType = forms.BooleanField(label = '有限合夥')

    TurnOffChrome = forms.CharField(initial='1',disabled='true')
    HeadlessMode = forms.CharField(initial='0',disabled='true')
    status = forms.CharField(initial='0',disabled='true')
