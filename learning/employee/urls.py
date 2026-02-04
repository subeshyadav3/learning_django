from django.urls import path,include
# from .views import EmployeeView, EmployeeDetailView
from .views import EmployeeViewset
from rest_framework.routers import DefaultRouter


router=DefaultRouter()
router.register('',EmployeeViewset,basename='employee')

urlpatterns = [
    # path('',EmployeeView.as_view()),
    # path('<int:pk>/',EmployeeDetailView.as_view()),
    path('',include(router.urls))
]
