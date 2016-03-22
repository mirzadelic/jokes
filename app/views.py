from rest_framework import serializers, viewsets, filters, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from models import *


# serializer for joke model
class JokeSerializer(serializers.ModelSerializer):
    likes = serializers.ReadOnlyField(source='get_likes_count')
    score = serializers.ReadOnlyField(source='get_rating_score')
    liked = serializers.SerializerMethodField('check_if_liked')
    rated = serializers.SerializerMethodField('check_if_rated')

    # return if device_id already liked joke (boolean)
    def check_if_liked(self, obj):
        device_id = self.context['request'].query_params.get('device_id', None)
        if device_id:
            return bool(obj.likes.filter(device_id=device_id).count())
        return False

    # return if device_id already rated joke (boolean)
    def check_if_rated(self, obj):
        device_id = self.context['request'].query_params.get('device_id', None)
        if device_id:
            return bool(obj.ratings.filter(device_id=device_id).count())
        return False

    class Meta:
        model = Joke
        fields = ('id', 'text', 'category', 'creator', 'email', 'likes', 'score', 'liked', 'rated', 'created_at')


# viewset for joke model
class JokeViewSet(viewsets.ModelViewSet):
    queryset = Joke.active.all()
    serializer_class = JokeSerializer

    # enable ascending and descending ordering/sorting by field 'created_at'
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('created_at',)

    # disable updating jokes with 'put' method
    http_method_names = ['get', 'post', 'head']

    # route action for like
    @detail_route(methods=['post'])
    def like(self, request, pk):
        obj = self.get_object()
        data = request.data
        data.update({'joke': obj.pk})
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            device_id = request.data.get('device_id', None)
            obj.likes.get_or_create(device_id=device_id)
            return Response({'error': False})
        else:
            return Response({'error': True}, status=status.HTTP_400_BAD_REQUEST)

    # route action for rating
    @detail_route(methods=['post'])
    def rate(self, request, pk):
        obj = self.get_object()
        data = request.data
        data.update({'joke': obj.pk})
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            device_id = request.data.get('device_id', None)
            rate = request.data.get('rate', None)
            obj.ratings.get_or_create(device_id=device_id, rate=rate)
            return Response({'error': False})
        else:
            return Response({'error': True}, status=status.HTTP_400_BAD_REQUEST)


# serializer for like model
class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('id', 'joke', 'device_id')


# serializer for rating model
class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ('id', 'joke', 'rate', 'device_id')


# serializer for category model
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name')


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None
