from django.urls import path
from . import views

app_name = 'membership'

urlpatterns = [
    path('info/', views.MembershipInfoView.as_view(), name='info'),
]
