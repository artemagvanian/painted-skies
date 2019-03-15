from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Mindmap
from ..utils.comparators import DisjointComparator
from ..utils.normalizers import PyMorphyNormalizer


class CompareAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        query = Mindmap.objects.filter(
            Q(owner=request.user.id) | Q(owner__profile__classrooms__teacher_id=request.user.id))
        a = query.get(id=request.GET['a'])
        b = query.get(id=request.GET['b'])
        cmp1 = DisjointComparator(a.mindmap, b.mindmap, PyMorphyNormalizer())
        return Response({'index': cmp1.compare()})
