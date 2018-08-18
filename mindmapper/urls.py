from django.urls import path
from .views import ProcessView

urlpatterns = [
    path('note', ProcessView.as_view())
]
