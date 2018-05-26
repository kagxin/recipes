from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from app.models import Snippet, Artile, Commit
from app.serializers import SnippetSerializer, AuthSerializer, ArtileSerializer, ArtileSerializer2
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.http import Http404
from rest_framework import permissions
from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework import generics, mixins
from rest_framework.pagination import PageNumberPagination


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class Login(APIView):

    def post(self, request, *args, **kwargs):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.data['username'], password=serializer.data['password'])
            if user is not None:
                if user.is_active:
                    login(self.request, user)
                    return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SnippetList(APIView):
    """
    列出所有的snippets或者创建一个新的snippet。
    """
    authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, format=None):
        print(list(request.GET.items()))
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):
    """
    检索，更新或删除一个snippet示例。
    """
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MyPaging(PageNumberPagination):

    page_size_query_param = 'page_size'
    page_size = 10


class ArtileView(generics.ListCreateAPIView):

    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    pagination_class = MyPaging
    queryset = Artile.objects.all()
    serializer_class = ArtileSerializer


class ArtileDetailView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ArtileSerializer
    queryset = Artile.objects.all()


class ArtileView2(generics.ListCreateAPIView):

    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    pagination_class = MyPaging
    queryset = Artile.objects.all()
    serializer_class = ArtileSerializer2


class ArtileDetailView2(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ArtileSerializer2
    queryset = Artile.objects.all()



