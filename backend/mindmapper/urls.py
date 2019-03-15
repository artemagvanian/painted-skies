from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from .api.classroom import ClassroomList, ClassroomDetail
from .api.comparator import CompareAPI
from .api.convertor import PdfMergeView
from .api.mindmap import MindmapList, MindmapDetail
from .api.notetaker import ProcessView
from .api.user import UserDetail
from .views import get_csrf_token, signup

urlpatterns = [
    path('note', ProcessView.as_view()),
    path('pdf', PdfMergeView.as_view()),
    path('compare', CompareAPI.as_view()),

    path('rest/mindmaps/', MindmapList.as_view()),
    path('rest/mindmaps/<int:pk>/', MindmapDetail.as_view()),

    path('rest/classrooms/', ClassroomList.as_view()),
    path('rest/classrooms/<int:pk>/', ClassroomDetail.as_view()),

    path('rest/users/<int:pk>/', UserDetail.as_view()),

    path('csrf', get_csrf_token),

    path('auth/obtain_token', obtain_jwt_token),
    path('auth/refresh_token', refresh_jwt_token),
    path('auth/verify_token', verify_jwt_token),

    path('auth/signup', signup)
]
