from rest_framework import routers, serializers, viewsets, permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (GenericAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView,
                                     DestroyAPIView)
from rest_framework.renderers import JSONRenderer

from django.db.models import Prefetch, Min, Subquery

# ViewSets define the view behavior.
from .serializers import (UserSerializer, ExpertSerializer, RankSerializer, RankTypeSerializer, ExpertsInLabSerializer,
                          ExpertiseAreaInLabSerializer, EmptySerializer)
from users.models import Expert
from expert.models import ExpertiseArea, ExpertExpertiseArea, Laboratory, ExpertLaboratory
from main.models import RankAndType


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = Expert.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.AllowAny]


# class ExpertsView(GenericAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [permissions.AllowAny ]
#     serializer_class = ExpertSerializer
#     queryset = Expert.objects.select_related("rank", "rank_type", "position")
#     perm_rel = Prefetch("expert_expertisearea", queryset= ExpertExpertiseArea.objects.select_related("expertisearea"))
#     lab_rel = Prefetch("expert_laboratory", queryset=ExpertLaboratory.objects.select_related("laboratory"))
#     queryset = queryset.prefetch_related(perm_rel, lab_rel)
#
#     def get(self, request, pk):
#         print(self.kwargs)
#         object = self.queryset.get(pk=pk)
#         serializer = self.get_serializer(object)
#         return Response(serializer.data)

class ExpertsView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.AllowAny ]
    serializer_class = ExpertSerializer
    queryset = Expert.objects.select_related("rank", "rank_type", "position")
    perm_rel = Prefetch("expert_expertisearea", queryset= ExpertExpertiseArea.objects.select_related("expertisearea"))
    lab_rel = Prefetch("expert_laboratory", queryset=ExpertLaboratory.objects.select_related("laboratory"))
    queryset = queryset.prefetch_related(perm_rel, lab_rel)

class ExpertRetriveView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated ]
    serializer_class = ExpertSerializer
    queryset = Expert.objects.select_related("rank", "rank_type", "position")
    perm_rel = Prefetch("expert_expertisearea", queryset= ExpertExpertiseArea.objects.select_related("expertisearea"))
    lab_rel = Prefetch("expert_laboratory", queryset=ExpertLaboratory.objects.select_related("laboratory"))
    queryset = queryset.prefetch_related(perm_rel, lab_rel)

class RankListView(GenericAPIView):
    queryset = RankAndType.objects.select_related("rank")
    serializer_class = RankSerializer

    def get(self, request, type_id):
        if type_id > 0:
            object_list = self.queryset.filter(type=type_id)
        else:
            # выводятся все звания
            selected_ids = self.queryset.values("rank").annotate(ids=Min("pk")).values("ids")
            object_list = self.queryset.filter(pk__in=Subquery(selected_ids)).order_by("rank")
        serializer = self.get_serializer(instance=object_list, many=True)
        return Response(serializer.data)

class RankTypeListView(GenericAPIView):
    queryset = RankAndType.objects.select_related("type")
    serializer_class = RankTypeSerializer

    def get(self, request, rank_id):
        if rank_id > 0:
            object_list = self.queryset.filter(rank=rank_id)
        else:
            # выводятся все звания
            selected_ids = self.queryset.values("rank").annotate(ids=Min("pk"))
            print(selected_ids )
            selected_ids = self.queryset.values("type").annotate(ids=Min("pk")).values("ids")
            object_list = self.queryset.filter(pk__in=Subquery(selected_ids)).order_by("type")
            print(object_list)
        serializer = self.get_serializer(instance=object_list, many=True)
        return Response(serializer.data)

class ExpertsInLab(ListAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated ]
    serializer_class = ExpertsInLabSerializer

    def get_queryset(self):
        lab_id = self.kwargs.get('lab_id')
        return Expert.objects.filter(laboratories__id=lab_id).distinct()


class RemoveExpertFromLab(DestroyAPIView):
    serializer_class = EmptySerializer
    queryset = ExpertLaboratory.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        print(self.kwargs)
        return ExpertLaboratory.objects.filter(laboratory=self.kwargs['lab_id'], expert=self.kwargs['expert_id']).first()




class ExpertiseAreaInLab(ListAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated ]
    serializer_class = ExpertiseAreaInLabSerializer

    def get_queryset(self):
        lab_id = self.kwargs.get('lab_id')
        return ExpertiseArea.objects.filter(laboratory__id=lab_id).distinct()
