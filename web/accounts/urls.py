from django.urls import path
from accounts import views


urlpatterns=[
    # path("create/",create_account,name="create_account")
    path('',views.GeekViews.as_view(),name='geek_list'),
    path('form/',views.my_view,name='geek_form'),
]