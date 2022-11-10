from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from pars.models import Log
from pars.serializers import LogCreateSerializer


class ParserViewSet(GenericViewSet, mixins.CreateModelMixin):
    queryset = Log.objects.all()
    serializer_class = LogCreateSerializer
