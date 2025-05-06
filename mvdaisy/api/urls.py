from django.urls import path, include
from rest_framework import routers
from .views import (CustomUserViewSet,
                    ExpertsView,
                    ExpertRetriveView,
                    RankListView,
                    RankTypeListView,
                    ExpertsInLab,
                    ExpertiseAreaInLab)

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('experts/<int:pk>/', ExpertRetriveView.as_view(), name='expert'),
    path('experts/', ExpertsView.as_view(), name='experts'),
    path('ranks/<int:type_id>/', RankListView.as_view(), name='ranks'),
    path('ranktypes/<int:rank_id>/', RankTypeListView.as_view(), name='ranktypes'),
    path('experts_lab/<int:lab_id>/',ExpertsInLab.as_view(), name='experts_lab'),
    path('ex_area_lab/<int:lab_id>/', ExpertiseAreaInLab.as_view(), name='ex_area_lab'),

]