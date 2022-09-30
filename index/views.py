from django.shortcuts import render

# Create your views here.
def index_view(requset):
    return render(requset,'index/index.html')