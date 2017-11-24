from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.response import Response

from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token
from snippets.custom import ExampleAuthentication

from snippets.models import (
    UserModel, 
    MovieModel, 
    CFModel, 
    SModel, 
    UPModel, 
    LAModel, 
    WIPModel
)
from snippets.serializers import (
    UserModelSerializer,
    MovieModelSerializer,
    CFModelSerializer,
    SModelSerializer,
    UPModelSerializer,
    LAModelSerializer,
    WIPModelSerializer
)

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

#curl http://localhost:8000/user/ -X POST 
# -H "Content-Type: application/json" 
# -d '{"idx":"1002","user_id":"fsoft1002",
# "email":"huynhthang@gmail.com","password":"123456",
# "first_name":"thang","last_name":"huynh","url":"123434"}'

# curl http://localhost:8000/user/fsoft1001/ -X PUT 
# -H "Content-Type: application/json" 
# -d '{"idx":"1003","user_id":"fsoft1003",
# "email":"trantu.uit@gmail.com","password":"tu",
# "first_name":"tu","last_name":"tran"}'

@csrf_exempt
def userList(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = UserModel.objects.all()
        serializer = UserModelSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserModelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def user_detail(request,id):
    """
    Retrieve, update or delete a code snippet.
    """
    print('-----:%s'%id)
    try:
        user = UserModel.objects.get(user_id=id)
    except UserModel.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = UserModelSerializer(user)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        print('put')
        data = JSONParser().parse(request)
        serializer = UserModelSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(status=204)

@csrf_exempt
def getMovieFromCollaborativeFilteringByUserId(request, id):
    try:
        user = UserModel.objects.get(user_id=id)
        cf = CFModel.objects.get(idx_user=user.idx)
        array =[]
        for i in cf.recommendations:
            words = i.split('|')
            idx_movie = words[0]
            movie = MovieModel.objects.get(idx=int(idx_movie))
            array.append(movie)
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = MovieModelSerializer(array, many=True)
        return JsonResponse(serializer.data, safe=False)
    pass

@csrf_exempt
def getMovieFromSimilarityByMovieId(request, id):
    try:
        list_movie_id = SModel.objects.get(movie_id=id)
        array =[]
        for i in list_movie_id.recommendations:
            words = i.split('|')
            idx_movie = words[0]
            movie = MovieModel.objects.get(movie_id=idx_movie)
            array.append(movie)
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = MovieModelSerializer(array, many=True)
        return JsonResponse(serializer.data, safe=False)
    pass

@csrf_exempt
def getMovieFromLastActionByUserId(request, id):
    try:
        user = UserModel.objects.get(user_id=id)
        print(user)   
        list_movie_id = LAModel.objects.get(idx_user=user.idx)
        print(list_movie_id)
        array =[]
        for i in list_movie_id.recommendations:
            words = i.split('|')
            idx_movie = words[0]
            print(idx_movie)
            movie = MovieModel.objects.get(idx=idx_movie)
            print(movie)
            array.append(movie)
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = MovieModelSerializer(array, many=True)
        return JsonResponse(serializer.data, safe=False)
    pass

@csrf_exempt
def getMovieFromWhatIsPupular(request):
    try:
        list_movie_id = WIPModel.objects.all()
        array =[]
        for i in list_movie_id:
            idx_movie = i.idx_movie
            movie = MovieModel.objects.get(idx=idx_movie)
            array.append(movie)
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = MovieModelSerializer(array, many=True)
        return JsonResponse(serializer.data, safe=False)
    pass

@csrf_exempt
def login(request):

    if request.method == 'POST':
        # user = authenticate(username=username, password=password)
        data = JSONParser().parse(request)
        obj = ExampleAuthentication()
        user = obj.authenticate(data)
        # print(user)
        if not user:
            print('error')
            return Response({"error": "Login failed"}, status=HTTP_401_UNAUTHORIZED)
            
        token = Token.objects.get_or_create(user=user)
        print(token)
        return Response({"token": token.key})
        # return 'hello'

@csrf_exempt
def getMovie(request, id):
    try:
        movie = MovieModel.objects.get(movie_id=id)
        print(movie)  
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        if movie:
            serializer = MovieModelSerializer(movie)
            return JsonResponse(serializer.data, safe=False)
        else:
            return HttpResponse(status=404)