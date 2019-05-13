from django.urls import path
from app import views
# Create your views here.

urlpatterns = [
    path('', views.index),
    path('help/', views.help),
    path('admin/', views.admin),

    path('getAct/', views.getAct),
    path('submitResult/', views.submitResult),

    path('startRoom/', views.startRoom),
    path('stopRoom/', views.stopRoom),
    path('roomStatus/', views.roomStatus),

    path('userReg/', views.userReg),
    path('userOut/', views.userOut),
    path('userAct/', views.userAct),
    path('userStatus/', views.userStatus),
    # path('userScript/', views.userScript),

    path('getStatus/', views.getStatus),
]
