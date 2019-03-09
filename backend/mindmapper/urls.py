from django.urls import path
from .views import ProcessView, PdfMergeView, get_csrf_token, signup
from .api_views import MindmapDetail, MindmapList
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

urlpatterns = [
    path('note', ProcessView.as_view()),
    path('pdf', PdfMergeView.as_view()),
    path('rest/mindmaps/', MindmapList.as_view()),
    path('rest/mindmaps/<int:pk>/', MindmapDetail.as_view()),
    path('csrf', get_csrf_token),
    path('auth/obtain_token', obtain_jwt_token),
    path('auth/refresh_token', refresh_jwt_token),
    path('auth/verify_token', verify_jwt_token),
    path('auth/signup', signup)
]
