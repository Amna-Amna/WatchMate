from watchlist_app import models
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework import generics
from rest_framework import serializers 
from watchlist_app.api.permissions import AdminorReadOnly, ReviewUserOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle

class StreamPlatformList(APIView):
    permission_classes = [AdminorReadOnly]
    def get(self, request):
        platform = models.StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform, many=True, context={'request': request})
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformDetail(APIView):
    permission_classes = [AdminorReadOnly]
    def get(self, request, pk):
        try: 
            platform = models.StreamPlatform.objects.get(pk=pk)
        except models.StreamPlatform.DoesNotExist:
            return Response({'Error': "Not found"}, status= status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        platform = models.StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        platform = models.StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WatchList(APIView):
    permission_classes = [AdminorReadOnly]
    def get(self, request):
        watchlist = models.WatchList.objects.all()
        serializer = WatchListSerializer(watchlist, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class WatchListDetail(APIView):
    permission_classes = [AdminorReadOnly]
    def get(self, request, pk):
        try: 
            watchlist = models.WatchList.objects.get(pk=pk)
        except models.WatchList.DoesNotExist:
            return Response({'Error': "Not found"}, status= status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(watchlist)
        return Response(serializer.data)

    def put(self, request, pk):
        watchlist = models.WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(watchlist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        watchlist = models.WatchList.objects.get(pk=pk)
        watchlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self):
        watchlist_pk = self.kwargs.get('pk')
        return models.Review.objects.filter(watchlist_id=watchlist_pk)
    
    def perform_create(self, serializer):
        watchlist = models.WatchList.objects.get(pk=self.kwargs.get('pk'))

        review_user = self.request.user
        review_queryset = models.Review.objects.filter(watchlist=watchlist, review_user=review_user)
        if review_queryset.exists():
            raise serializers.ValidationError("You have already reviewed this watchlist!")

        serializer.save(watchlist=watchlist, review_user=review_user)

class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]

    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        watchlist_pk = self.kwargs.get('pk')
        return models.Review.objects.filter(watchlist_id=watchlist_pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'


    lookup_url_kwarg = 'review_pk'
    def get_queryset(self):
        watchlist_pk = self.kwargs.get('pk')    
        return models.Review.objects.filter(watchlist_id=watchlist_pk)
        

class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        username = self.kwargs.get('username')
        return models.Review.objects.filter(review_user__username=username)

class UserReviewQueryParams(generics.ListAPIView):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        username = self.request.query_params.get('username')
        return models.Review.objects.filter(review_user__username=username)