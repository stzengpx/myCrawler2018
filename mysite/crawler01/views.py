from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Tasks
from .forms import TasksForm
from .forms import RawTasksForm

def index(request):
    return HttpResponse("Hello, world. You're at the crawler01 index.")

def tasks_index(request):
    # 今天先不探討什麼是 render，先記得它會去撈 test.html
    # return render(request, 'test.html')
    tasks_list = Tasks.objects.all()
    context = {'tasks_list': tasks_list} # 建立 Dict 對應到 Tasks 的資料，
    # return render(request, 'test.html', context)
    return render(request, 'detail.html', context)

def tasks_create_view(request):
    form = TasksForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = TasksForm() # 清空 form

    context = {
        'form' : form
    }
    return render(request, "create-model-form.html", context)

def tasks_create2_view(request):
    form = RawTasksForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        print(form.cleaned_data.get('user_name'))
        # Tasks.objects.create(**form.cleaned_data)
        # myDict = {'user_name': 'patrick2', 'user_email': 'st.zengpx@gmail.com', 'QryCond': '台北市信義區', 'StartPage': 1, 'StopPage': 2, 'DataType': '10000', 'TurnOffChrome': '1', 'HeadlessMode': '0', 'status': '0'}
        # Tasks.objects.create(**myDict)
        
        form = RawTasksForm()
    
    context = {
        'form' : form
    }
    return render(request, "create-django-form.html", context)