from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Mindmap
from ..utils.graph_comparators import EdgeGraphComparator


class CompareAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        query = Mindmap.objects.filter(
            Q(owner=request.user.id) | Q(owner__classrooms__teacher_id=request.user.id)).distinct()
        a = query.get(id=request.GET['a'])
        b = query.get(id=request.GET['b'])
        cmp = EdgeGraphComparator(a.mindmap, b.mindmap)
        return Response({'index': cmp.compare()})
