from . import views
from django.urls import path

urlpatterns = [
    path('watchlist/', views.WatchList.as_view(), name='watchlist'),
    path('watchlist/<int:pk>/', views.WatchListDetail.as_view(), name='single-watchlist'),
    path('stream/list/', views.StreamPlatformList.as_view(), name='stream-list'),
    path('stream/<int:pk>/', views.StreamPlatformDetail.as_view(), name='streamplatform-detail'),
    path('watchlist/<int:pk>/reviews/', views.ReviewList.as_view(), name='review-list'),
    path('watchlist/<int:pk>/create-review/', views.ReviewCreate.as_view(), name='review-create'),
    path('watchlist/<int:pk>/review/<int:review_pk>/', views.ReviewDetail.as_view(), name='review-detail'),
    path('user-reviews/<str:username>/', views.UserReview.as_view(), name='user-review'),
    path('query-reviews/', views.UserReviewQueryParams.as_view(), name='user-review-query-params'),
]