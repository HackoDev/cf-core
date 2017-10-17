from django.utils import timezone
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, GenericViewSet
from rest_framework import pagination

from .serializers import DictionarySerializer, CitySerializer
from ..models import ModerationNote
from .filters import ModerationNotesFilter


class PageNumberPaginator(pagination.PageNumberPagination):

    page_query_param = 'page'
    page_size_query_param = 'page_size'
    page_size = 20


class DictionaryViewSet(ViewSet):

    def get_items(self):
        return [
            {
                'name': 'MODERATE_STATUS_CHOICES',
                'items': ModerationNote.MODERATE_STATUS_CHOICES._doubles
            }
        ]

    def list(self, request, *args, **kwargs):
        serializer = DictionarySerializer(self.get_items(), many=True)
        return Response(serializer.data)


class ModerationNoteViewSet(mixins.ListModelMixin, GenericViewSet):

    serializer_class = serializers.ModerationNoteSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberPaginator
    filter_backends = (DjangoFilterBackend,)
    filter_class = ModerationNotesFilter

    def get_queryset(self):
        # TODO: implement polymorphic queryset (mixin or extra fields)
        self.http_method_not_allowed(self.request, "Not implemented")

    @detail_route(methods=['put'])
    def mark_as_seen(self, request, pk):
        obj = self.get_object()
        if obj.last_seen is None:
            obj.last_seen = timezone.now()
            obj.save(update_fields=['last_seen', 'modified'])
        return Response()
