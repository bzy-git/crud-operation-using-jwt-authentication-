from django.urls import path
from blog.views import * 

urlpatterns = [
    path('post/', PostView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginAPI.as_view()),
]
