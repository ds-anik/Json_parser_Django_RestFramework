import json

from rest_framework import serializers

from pars.models import Log
from pars.utils import DictObj, Object


class IgnoreUpdateCreateMixin(object):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class TextSerializer(IgnoreUpdateCreateMixin, serializers.Serializer):
    text = serializers.CharField()


class SeasonSerializer(IgnoreUpdateCreateMixin, serializers.Serializer):
    seasons = serializers.ListSerializer(child=TextSerializer(), required=False)
    description = serializers.CharField(required=False)


class AuthorSerializer(IgnoreUpdateCreateMixin, serializers.Serializer):
    username = serializers.CharField()
    id = serializers.CharField()


class CounterSerializer(IgnoreUpdateCreateMixin, serializers.Serializer):
    A = serializers.IntegerField()
    B = serializers.IntegerField()


class TransformSerializer(IgnoreUpdateCreateMixin, serializers.Serializer):
    path = serializers.CharField(source="address")
    seasons = serializers.ListSerializer(
        source="content.seasons", child=serializers.CharField()
    )
    body = serializers.CharField(source="content.description")
    author_name = serializers.CharField(source="author.username")
    author_id = serializers.CharField(source="author.id")
    created_date = serializers.SerializerMethodField()
    created_time = serializers.SerializerMethodField()
    updated_date = serializers.SerializerMethodField()
    updated_time = serializers.SerializerMethodField()
    counters_total = serializers.SerializerMethodField()
    id = serializers.CharField()

    @staticmethod
    def get_created_date(instance):
        return instance.created.date().isoformat()

    @staticmethod
    def get_created_time(instance):
        return instance.created.time().isoformat()

    @staticmethod
    def get_updated_date(instance):
        try:
            return instance.updated.date().isoformat()
        except AttributeError:
            pass

    @staticmethod
    def get_updated_time(instance):
        try:
            return instance.updated.time().isoformat()
        except AttributeError:
            pass

    @staticmethod
    def get_counters_total(instance):
        return instance.counters.A + instance.counters.B

    def to_representation(self, instance):
        if hasattr(instance, "content"):
            if hasattr(instance.content, "seasons"):
                instance.content.seasons = [
                    season.text for season in instance.content.seasons
                ]
            else:
                setattr(instance.content, "seasons", None)
            if not hasattr(instance.content, "description"):
                setattr(instance.content, "description", None)
        else:
            instance.content = Object()
            instance.content.description = None
            instance.content.seasons = None
        return super(TransformSerializer, self).to_representation(instance)


class LogCreateSerializer(IgnoreUpdateCreateMixin, serializers.Serializer):
    address = serializers.CharField()
    content = SeasonSerializer(required=False)
    updated = serializers.DateTimeField(required=False)
    created = serializers.DateTimeField()
    author = AuthorSerializer()
    id = serializers.CharField()
    counters = CounterSerializer()

    def create(self, validated_data):
        return Log.objects.create(
            data=json.dumps(TransformSerializer(instance=DictObj(validated_data)).data)
        )

    def to_representation(self, instance):
        return json.loads(instance.data)
