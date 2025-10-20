from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        exclude = ['watchlist']
        


class WatchListSerializer(serializers.ModelSerializer):
    length_name = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = WatchList
        fields = '__all__'

    def get_length_name(self, object):
        return len(object.title)

    def validate(self, data):
        if data.get('title') == data.get('story_line'):
            raise serializers.ValidationError("Title and Story Line should be different")
        return data

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title is too short")
        return value

    
class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)
    # watchlist = serializers.StringRelatedField(many=True)
    # watchlist = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='single-watchlist')
    class Meta:
        model = StreamPlatform
        fields = '__all__'
