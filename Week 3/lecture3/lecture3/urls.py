"""lecture3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

#The logic of how django processes URLs is as follows. Whenever it is given a url, it looks at the project level urls.py file to see whether any path matches the request that is sent 
#by client. In local, the defauly url is 127.0.0.1. So if the requested url is 127.0.0.1/hello then it looks at urlpatterns in project level urls.py to see if that fits any path
#Here, we see that it does fit a path and that path says to include all urls in hello.urls. Thus, it then looks at what comes after 127.0.0.1/hello and try to match it to urls defined in
#hellos.urls. In this case, there is nothing and a path in hellos.url does match that path. 

urlpatterns = [
    path('admin/', admin.site.urls),
    #the first argument means if we hit the route hello, then call the path referenced in the 2nd argument
    #the include argument means call ALL the urls found in hello.urls 
    path('hello/', include("hello.urls")),
    path('newyear/', include("newyear.urls")),
    path('tasks/', include("tasks.urls"))
]
