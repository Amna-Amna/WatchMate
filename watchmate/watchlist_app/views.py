# from django.shortcuts import render
# from watchlist_app.models import Movie
# from django.http import JsonResponse

# def movie_list(request):
#     movies = Movie.objects.all()
#     data = {
#         "movies": list(movies.values()) 
#     }
#     return JsonResponse(data, safe=False)

# def single_movie(request, pk):
#     movie = Movie.objects.get(pk=pk)
#     data = {
#         "name": movie.name,
#         "about": movie.about,
#         "active": movie.active
#     }
#     return JsonResponse(data)