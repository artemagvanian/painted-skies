from django.urls import path, include

from mindmapper.routers import router
from mindmapper.views import ProcessView

urlpatterns = [
    path('note', ProcessView.as_view()),
    path('rest/', include(router.urls)),
    path('auth/', include('rest_framework.urls'))
]
