from rest_framework import serializers

from cf_core.models import Location, ModerationNote


class DictionaryItemSerializer(serializers.Serializer):

    def to_representation(self, instance):
        return {
            'value': instance[0],
            'display_name': instance[1],
        }


class DictionarySerializer(serializers.Serializer):

    def to_representation(self, instance):
        return {
            'name': instance['name'],
            'items': DictionaryItemSerializer(instance['items'], many=True).data
        }


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ('id', 'name')


class ModerationNoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModerationNote
        fields = (
            'id', 'note',  'last_seen', 'created'
        )
