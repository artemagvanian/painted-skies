from django.urls import path, include

from .routers import router
from .views import ProcessView, PdfMergeView

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

urlpatterns = [
    path('note', ProcessView.as_view()),
    path('pdf', PdfMergeView.as_view()),
    path('rest/', include(router.urls)),
    path('auth/obtain_token', obtain_jwt_token),
    path('auth/refresh_token', refresh_jwt_token),
    path('auth/verify_token', verify_jwt_token),
]
