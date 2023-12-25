from django.urls import path, include
from rest_framework import routers
from .views import *

routerA = routers.SimpleRouter()
routerA.register(r'author', AuthorListAndDetailAPI)

routerB = routers.SimpleRouter()
routerB.register(r'books', BookListAndDetailAPI)

urlpatterns = [
    path('rest/api/', include(routerA.urls)),
    path('rest/api/', include(routerB.urls)),
    path('rest/api/add_book', AddBookAPI.as_view()),
]
