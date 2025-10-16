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


# def name_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError("Name is too short")
#     return value

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=255, validators=[name_length])
#     about = serializers.CharField()
#     active = serializers.BooleanField(default=True)

#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.about = validated_data.get('about', instance.about)
#         instance.active = validated_data.get('active', instance.active)

#         instance.save()
#         return instance 

#     def validate(self, data):
#         if data.get('name') == data.get('about'):
#             raise serializers.ValidationError("Name and About should be different")
#         return data

#     def validate_name(self, value):
#         if len(value) < 5:
#             raise serializers.ValidationError("Name is too short")
#         return value