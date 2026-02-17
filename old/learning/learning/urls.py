from django.contrib import admin
from django.urls import path,include, re_path
# from myapp.views import home, student_detail
from api.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home.as_view(), name='home'),
    path('api/', include('api.urls')),
    path('', include('blogs.urls')),
    # path('student/',include('myapp.urls')),
    # re_path(r'^student/(?P<id>\d+)/$', student_detail,kwargs={'role': 'admin'}),

    # path('student/<int:pk>/'    , student_detail.as_view(), name='student_detail'),
]