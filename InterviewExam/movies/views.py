from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from django_filters import rest_framework as filters
from .models import Movie
from .serializers import MovieSerializer
from .pagination import CustomPagination
from .filters import MovieFilter

# Removes permissions from views

class ListCreateMovieAPIView(ListCreateAPIView):
    serializer_class = MovieSerializer
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MovieFilter

    def perform_create(self, serializer):
        # Assign the user who created the movie
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        queryset = Movie.objects.all()
        filtered = {}
        if not self.request._user.is_superuser:
            filtered['creator'] = self.request._auth['user_id']
        return queryset.filter(**filtered)


class RetrieveUpdateDestroyMovieAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        queryset = Movie.objects.all()
        filtered = {}
        if not self.request._user.is_superuser:
            filtered['creator'] = self.request._auth['user_id']
        return queryset.filter(**filtered)






