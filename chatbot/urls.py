from django.urls import path
from .views import chat

urlpatterns = [
    path("chat/", chat, name="chat"),
]



from django.urls import path
from .views import chat, index

urlpatterns = [
    path("", index, name="index"),
    path("chat/", chat, name="chat"),
]

