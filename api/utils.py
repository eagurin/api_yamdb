from rest_framework import viewsets
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)


class CreateListViewSet(CreateModelMixin,
                        ListModelMixin,
                        DestroyModelMixin,
                        viewsets.GenericViewSet):
    pass
