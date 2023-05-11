from django.urls import path
from .views import *

urlpatterns = [
    path("",homepageview,name="homepageview"),
#     path("",abs_summ,name='abs_summ'),
    path('ajax_test/', ajax_test, name='ajax_test'),
    path('ajax_test2/', ajax_test2, name='ajax_test2'),
]