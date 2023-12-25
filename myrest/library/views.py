from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Book, Author
from .serializers import BookSerializer, AddBookSerializer, AuthorSerializer


class AddBookAPI(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        serializer = AddBookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if Book.objects.filter(title=serializer.validated_data['title']).exists():
            queryset = Book.objects.filter(title=serializer.validated_data['title'])
            flag = True

            if serializer.validated_data['category'] == 'hud':
                for i in queryset:
                    if serializer.validated_data['category'] == 'hud' and i.publisher != serializer.validated_data[
                            'publisher']:
                        flag = False
                    else:
                        flag = True
                        break

            if serializer.validated_data['category'] == 'uch':
                for i in queryset:
                    if serializer.validated_data['category'] == 'uch' and i.yearOfRel != serializer.validated_data[
                            'yearOfRel']:
                        flag = False
                    else:
                        flag = True
                        break

            if flag:
                raise ValidationError('В БД уже есть книга с таким названием.')
            else:
                serializer.save()
                return Response({'post': "Запись успешно добавлена."})

        serializer.save()
        return Response({'post': "Запись успешно добавлена."})


class BookListAndDetailAPI(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'genre']


class AuthorListAndDetailAPI(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'lastName', 'middle_name']
