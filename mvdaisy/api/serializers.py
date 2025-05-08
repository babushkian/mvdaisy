from django.contrib.auth import get_user_model
from rest_framework import  serializers

from main.models import RankType, Rank, Position

from expert.models import ExpertLaboratory, ExpertExpertiseArea, ExpertiseArea
from main.models import RankAndType

Expert = get_user_model()


class EmptySerializer(serializers.Serializer):
    pass

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Expert
        fields = ['url', 'username', "last_name", "first_name", "second_name",'email', 'is_staff']


class ExpertExpertiseAreaSetializer(serializers.ModelSerializer):
    expertisearea = serializers.StringRelatedField()
    class Meta:
        model = ExpertExpertiseArea
        fields = ("expertisearea", "start_date", "end_date")

class ExpertLaboratorySerializer(serializers.ModelSerializer):
    laboratory = serializers.StringRelatedField()
    class Meta:
        model = ExpertLaboratory
        fields = ("laboratory", "start_date", "end_date")



class ExpertSerializer(serializers.ModelSerializer):

    expert_laboratory = ExpertLaboratorySerializer(many=True, read_only=True)
    expert_expertisearea = ExpertExpertiseAreaSetializer(many=True, read_only=True)
    position = serializers.StringRelatedField()
    # rank = serializers.SlugRelatedField(queryset=Rank.objects.all(), slug_field="name")
    # rank = serializers.PrimaryKeyRelatedField(queryset=Rank.objects.all() )
    rank_and_type = serializers.SerializerMethodField()
    fio = serializers.SerializerMethodField()

    class Meta:
        model = Expert
        fields = [ 'fio', 'username', "last_name", "first_name", "second_name", "sex",'is_staff',
                   'rank_and_type',
                   # 'rank',
                   'position',
                   'expert_laboratory', 'expert_expertisearea',
        ]

    def get_fio(self, obj):
        ln = obj.last_name if obj.first_name else obj.username
        fn_letter = f" {obj.first_name[0]}." if obj.first_name else ""
        sn_letter = f" {obj.second_name[0]}." if obj.first_name else ""
        return f"{ln}{fn_letter}{sn_letter}"

    def get_rank_and_type (self, obj):
        return f"{obj.rank} {obj.rank_type}"


class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model= RankAndType
        fields=["rank",]
    rank= serializers.StringRelatedField()

class RankTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model= RankAndType
        fields=["type",]
    type= serializers.StringRelatedField()


class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model= RankAndType
        fields=["rank",]
    rank= serializers.StringRelatedField()



class ExpertsInLabSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name (self, obj):
        return f"{obj.last_name} {obj.first_name}"

    class Meta:
        model= Expert
        fields=["pk", "name"]


class ExpertiseAreaInLabSerializer(serializers.ModelSerializer):
    class Meta:
        model= ExpertiseArea
        fields=["pk", "name"]