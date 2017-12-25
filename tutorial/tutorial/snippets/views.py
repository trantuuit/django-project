from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.response import Response

from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token
from snippets.custom import ExampleAuthentication
from datetime import datetime, timezone, date
from snippets.models import (
    UserModel, 
    MovieModel, 
    CFModel, 
    SModel, 
    UPModel, 
    LAModel, 
    WIPModel,
    TrendModel,
    ActorsProfileModel,
    DirectorsProfileModel,
    GenresProfileModel,
    WritersProfileModel,
    SpecificProfileModel,
    UserEventModel
)
from snippets.serializers import (
    UserModelSerializer,
    MovieModelSerializer,
    CFModelSerializer,
    SModelSerializer,
    UPModelSerializer,
    LAModelSerializer,
    WIPModelSerializer,
    GenresProfileModelSerializer,
    UserEventModelSerializer
)

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
"""
curl http://localhost:8000/user/ -X POST 
-H "Content-Type: application/json" 
-d '{"idx":"1002","user_id":"fsoft1002",
"email":"huynhthang@gmail.com","password":"123456",
"first_name":"thang","last_name":"huynh","url":"123434"}'
"""
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
        try:
            data = JSONParser().parse(request)
            user = UserModel.objects.get(user_id=data['userId'])
            if user is not None:
                return JsonResponse({'successfully':'false'}, status=201)
            pass
        except UserModel.DoesNotExist:
            idx = UserModel.objects.all().count()
            json = {
                'idx':idx + 1,
                'user_id':data['userId'],
                'email': data['email'],
                'first_name': data['firstname'],
                'lastname': data['lastname'],
                'password': data['password'],
                'url':'',
                'isnew':1
            }
            serializer = UserModelSerializer(data=json)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'successfully':'true'}, status=201)
            pass
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def userevent(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            print(data)
            json = {
                'idx_user': data['idx_user'],
                'idx_movie': data['idx_movie'],
                'time': int(datetime.now().timestamp()),
                'rating': data['rating'],
                'type_event': data['type_event']
            }
            serializer =UserEventModelSerializer(data=json)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'successfully':'true'}, status=201)
            pass
        except:
            return JsonResponse(serializer.errors, status=400)
            pass

@csrf_exempt
def registerSurvey(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            print(data)
            json = {
                'idx': data['idx'],
                'user_id': data['userId'],
                'email': data['email'],
                'first_name': data['firstname'],
                'lastname': data['lastname'],
                'password': data['password'],
                'url':data['url'],
                'isnew':data['isnew'],
                'survey': data['survey']
            }
            serializer = UserModelSerializer(data=json)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'successfully':'true'}, status=201)
            pass
        except:
            return JsonResponse(serializer.errors, status=400)
            pass

        
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
def login(request,userId,password):
    try:
        print(userId)
        print(password)
        user = UserModel.objects.get(user_id=userId,password=password)
        if user is not None:
            # print(user['isnew'])
            isNew=user['isnew']
            x= True
            idx_user = user['idx']

        pass
    except UserModel.DoesNotExist:
        x =False
        isNew = 0
        idx_user = -1
        # return HttpResponse(status=404)
        pass
    if request.method == 'GET':
        # serializer = UserModelSerializer(user)
        return JsonResponse({'match':x, 'isNew': isNew, 'idx_user': idx_user})
        pass
    pass

@csrf_exempt
def getMovieFromCollaborativeFilteringByUserId(request, id):
    try:
        user = UserModel.objects.get(user_id=id)
        cf = CFModel.objects.get(idx_user=user.idx)
        array =[]
        for i in cf.recommendations:
            words = i.split('|')
            idx_movie = words[0]
            score = words[1]
            print(score)
            movie = MovieModel.objects.get(idx=int(idx_movie))
            # print(type(movie))
            temp = dict(movie)
            temp['score'] = score
            # print(dict(movie)+dict({'score':score}))
            # print(dict(temp))
            array.append(temp)
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        # serializer = MovieModelSerializer(array, many=True)
        return JsonResponse(array, safe=False)
    pass

@csrf_exempt
def getMovieFromSimilarityByMovieId(request, id):
    try:
        list_movie_id = SModel.objects.get(movie_id=id)
        array =[]
        for i in list_movie_id.recommendations:
            words = i.split('|')
            idx_movie = words[0]
            similarity = words[1]
            movie = MovieModel.objects.get(movie_id=idx_movie)
            temp = dict(movie)
            temp['similarity'] = similarity
            array.append(temp)
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        # serializer = MovieModelSerializer(array, many=True)
        return JsonResponse(array, safe=False)
    pass

@csrf_exempt
def getMovieFromLastActionByUserId(request, id):
    try:
        user = UserModel.objects.get(user_id=id)
        print(user)   
        list_movie_id = LAModel.objects.get(idx_user=user.idx)
        print('-------')
        print(list_movie_id.recommendations)
        array =[]
        for i in list_movie_id.recommendations:
            if i != '':
                words = i.split('|')
                print(words)
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
            movie_id = i.movie_id
            count = i.views
            movie = MovieModel.objects.get(movie_id=movie_id)
            temp = dict(movie)
            temp['like'] = count
            array.append(temp)
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        # serializer = MovieModelSerializer(array, many=True)
        return JsonResponse(array, safe=False)
    pass

# @csrf_exempt
# def login(request):

#     if request.method == 'POST':
#         # user = authenticate(username=username, password=password)
#         data = JSONParser().parse(request)
#         obj = ExampleAuthentication()
#         user = obj.authenticate(data)
#         # print(user)
#         if not user:
#             print('error')
#             return Response({"error": "Login failed"}, status=HTTP_401_UNAUTHORIZED)
            
#         token = Token.objects.get_or_create(user=user)
#         print(token)
#         return Response({"token": token.key})
        # return 'hello'

@csrf_exempt
def getMovie(request, id):
    try:
        movie = MovieModel.objects.get(movie_id=id)
        # print(movie)  
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        if movie:
            serializer = MovieModelSerializer(movie)
            return JsonResponse(serializer.data, safe=False)
        else:
            return HttpResponse(status=404)

@csrf_exempt
def getMovieTrending(request):
    try:
        list_movie_id = TrendModel.objects.all()
        # print(list_movie_id)
        array =[]
        for i in list_movie_id:
            movie_id = i.movie_id
            # print(movie_id)
            movie = MovieModel.objects.get(movie_id=movie_id)
            # print(movie)
            if movie != None:
                array.append(movie)
        # print(array)
        # print(movie)  
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = MovieModelSerializer(array, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def getGenresMoviesByUserId(request, id):
    try:
        user = UserModel.objects.get(user_id=id)
        # print(user)   
        list_genres = GenresProfileModel.objects.get(idx_user=user.idx)
        genre = list_genres.recommendations[0].split('|')[0]
        list_movies = SpecificProfileModel.objects.get(identifier=genre)
        # print(list_movies.recommendations)
        array =[]
        for i in list_movies.recommendations:
            words = i.split('|')
            # print(words)
            movie_id = words[0]
            # print(movie_id)
            movie = MovieModel.objects.get(movie_id=movie_id)
        #         print(movie)
            array.append(movie)
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = MovieModelSerializer(array, many=True)
        return JsonResponse(serializer.data, safe=False)
    pass

@csrf_exempt
def getTopGenresProfileByUserId(request, id):
    try:
        user = UserModel.objects.get(user_id=id)
        # print(user)   
        list_genres = GenresProfileModel.objects.get(idx_user=int(user.idx))
        genre = list_genres.recommendations[0].split('|')[0]
        # print(list_genres.recommendations)
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        # serializer = GenresProfileModelSerializer(list_genres)
        # return Response({"message": "Will not appear in schema!"})
        return JsonResponse({"genre": genre}, safe=False)
    pass

@csrf_exempt
def getDirectorMoviesByUserId(request, id):
    try:
        user = UserModel.objects.get(user_id=id)
        # print(user)   
        list_genres = DirectorsProfileModel.objects.get(idx_user=user.idx)
        # director = list_genres.recommendations[0].split('|')[0]
        array =[]
        for row in list_genres.recommendations[0:4]:
            director = row.split('|')[0]
            list_movies = SpecificProfileModel.objects.get(identifier=director)
            for i in list_movies.recommendations:
                words = i.split('|')
                # print(words)
                movie_id = words[0]
                # print(movie_id)
                movie = MovieModel.objects.get(movie_id=movie_id)
            #         print(movie)
                array.append(movie)
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = MovieModelSerializer(array, many=True)
        return JsonResponse(serializer.data, safe=False)
    pass

@csrf_exempt
def getTopDirectorProfileByUserId(request, id):
    try:
        user = UserModel.objects.get(user_id=id)
        # print(user)   
        list_director = DirectorsProfileModel.objects.get(idx_user=int(user.idx))
        # print(list_director.recommendations)
        # director = list_director.recommendations[0].split('|')[0]
        array = list_director.recommendations[0].split('|')[0]
        # print(array)
        for row in list_director.recommendations[1:3]:
            # print(row)
            writer = row.split('|')[0]
            # print(writer)
            array =array + ', ' + writer
        # print(list_genres.recommendations)
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        # serializer = GenresProfileModelSerializer(list_genres)
        # return Response({"message": "Will not appear in schema!"})
        return JsonResponse({"director": array}, safe=False)
    pass

@csrf_exempt
def getWriterMoviesByUserId(request, id):
    try:
        user = UserModel.objects.get(user_id=id)
        # print(user)   
        list_writer = WritersProfileModel.objects.get(idx_user=user.idx)
        array =[]
        for row in list_writer.recommendations[0:4]:
            writer = row.split('|')[0]
            list_movies = SpecificProfileModel.objects.get(identifier=writer)
            for i in list_movies.recommendations:
                words = i.split('|')
                # print(words)
                movie_id = words[0]
                # print(movie_id)
                movie = MovieModel.objects.get(movie_id=movie_id)
            #         print(movie)
                array.append(movie)

        # writer = list_writer.recommendations[0].split('|')[0]
        # list_movies = SpecificProfileModel.objects.get(identifier=writer)
        # # print(list_movies.recommendations)
        # array =[]
        # for i in list_movies.recommendations:
        #     words = i.split('|')
        #     # print(words)
        #     movie_id = words[0]
        #     # print(movie_id)
        #     movie = MovieModel.objects.get(movie_id=movie_id)
        # #         print(movie)
        #     array.append(movie)
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = MovieModelSerializer(array, many=True)
        return JsonResponse(serializer.data, safe=False)
    pass

@csrf_exempt
def getTopWriterProfileByUserId(request, id):
    try:
        user = UserModel.objects.get(user_id=id)
        # print(user)   
        list_writer = WritersProfileModel.objects.get(idx_user=int(user.idx))
        # writers = list_writer.recommendations[0].split('|')

        array = list_writer.recommendations[0].split('|')[0]
        for row in list_writer.recommendations[1:3]:
            writer = row.split('|')[0]
            array =array + ', ' + writer
        # print(list_genres.recommendations)
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        # serializer = GenresProfileModelSerializer(list_genres)
        # return Response({"message": "Will not appear in schema!"})
        return JsonResponse({"writer": array}, safe=False)
    pass

@csrf_exempt
def getDrama(request):
    try:
        list_movies = SpecificProfileModel.objects.get(identifier='Drama')
        array=[]
        for i in list_movies.recommendations:
            words = i.split('|')
            movie_id = words[0]
            movie = MovieModel.objects.get(movie_id=movie_id)
            array.append(movie)
        pass
    except:
        return HttpResponse(status=404)
        pass
    if request.method == 'GET':
        serializer = MovieModelSerializer(array, many=True)
        return JsonResponse(serializer.data, safe=False)
    pass

@csrf_exempt
def getAction(request):
    try:
        list_movies = SpecificProfileModel.objects.get(identifier='Action')
        array=[]
        for i in list_movies.recommendations:
            words = i.split('|')
            movie_id = words[0]
            movie = MovieModel.objects.get(movie_id=movie_id)
            array.append(movie)
        pass
    except:
        return HttpResponse(status=404)
        pass
    if request.method == 'GET':
        serializer = MovieModelSerializer(array, many=True)
        return JsonResponse(serializer.data, safe=False)
    pass

@csrf_exempt
def getAnimation(request):
    try:
        list_movies = SpecificProfileModel.objects.get(identifier='Animation')
        array=[]
        for i in list_movies.recommendations:
            words = i.split('|')
            movie_id = words[0]
            movie = MovieModel.objects.get(movie_id=movie_id)
            array.append(movie)
        pass
    except:
        return HttpResponse(status=404)
        pass
    if request.method == 'GET':
        serializer = MovieModelSerializer(array, many=True)
        return JsonResponse(serializer.data, safe=False)
    pass

@csrf_exempt
def getComedy(request):
    try:
        list_movies = SpecificProfileModel.objects.get(identifier='Comedy')
        array=[]
        for i in list_movies.recommendations:
            words = i.split('|')
            movie_id = words[0]
            movie = MovieModel.objects.get(movie_id=movie_id)
            array.append(movie)
        pass
    except:
        return HttpResponse(status=404)
        pass
    if request.method == 'GET':
        serializer = MovieModelSerializer(array, many=True)
        return JsonResponse(serializer.data, safe=False)
    pass

@csrf_exempt
def getSci_Fi(request):
    try:
        list_movies = SpecificProfileModel.objects.get(identifier='Sci-Fi')
        array=[]
        for i in list_movies.recommendations:
            words = i.split('|')
            movie_id = words[0]
            movie = MovieModel.objects.get(movie_id=movie_id)
            array.append(movie)
        pass
    except:
        return HttpResponse(status=404)
        pass
    if request.method == 'GET':
        serializer = MovieModelSerializer(array, many=True)
        return JsonResponse(serializer.data, safe=False)
    pass

@csrf_exempt
def getDocumentary(request):
    try:
        list_movies = SpecificProfileModel.objects.get(identifier='Documentary')
        array=[]
        for i in list_movies.recommendations:
            words = i.split('|')
            movie_id = words[0]
            movie = MovieModel.objects.get(movie_id=movie_id)
            array.append(movie)
        pass
    except:
        return HttpResponse(status=404)
        pass
    if request.method == 'GET':
        serializer = MovieModelSerializer(array, many=True)
        return JsonResponse(serializer.data, safe=False)
    pass

@csrf_exempt
def getRomance(request):
    try:
        list_movies = SpecificProfileModel.objects.get(identifier='Romance')
        array=[]
        for i in list_movies.recommendations:
            words = i.split('|')
            movie_id = words[0]
            movie = MovieModel.objects.get(movie_id=movie_id)
            array.append(movie)
        pass
    except:
        return HttpResponse(status=404)
        pass
    if request.method == 'GET':
        serializer = MovieModelSerializer(array, many=True)
        return JsonResponse(serializer.data, safe=False)
    pass

@csrf_exempt
def getHorror(request):
    try:
        list_movies = SpecificProfileModel.objects.get(identifier='Horror')
        array=[]
        for i in list_movies.recommendations:
            words = i.split('|')
            movie_id = words[0]
            movie = MovieModel.objects.get(movie_id=movie_id)
            array.append(movie)
        pass
    except:
        return HttpResponse(status=404)
        pass
    if request.method == 'GET':
        serializer = MovieModelSerializer(array, many=True)
        return JsonResponse(serializer.data, safe=False)
    pass
@csrf_exempt
def getThriller(request):
    try:
        list_movies = SpecificProfileModel.objects.get(identifier='Thriller')
        array=[]
        for i in list_movies.recommendations:
            words = i.split('|')
            movie_id = words[0]
            movie = MovieModel.objects.get(movie_id=movie_id)
            array.append(movie)
        pass
    except:
        return HttpResponse(status=404)
        pass
    if request.method == 'GET':
        serializer = MovieModelSerializer(array, many=True)
        return JsonResponse(serializer.data, safe=False)
    pass
@csrf_exempt
def getAdventure(request):
    try:
        list_movies = SpecificProfileModel.objects.get(identifier='Adventure')
        array=[]
        for i in list_movies.recommendations:
            words = i.split('|')
            movie_id = words[0]
            movie = MovieModel.objects.get(movie_id=movie_id)
            array.append(movie)
        pass
    except:
        return HttpResponse(status=404)
        pass
    if request.method == 'GET':
        serializer = MovieModelSerializer(array, many=True)
        return JsonResponse(serializer.data, safe=False)
    pass

@csrf_exempt
def getFantasy(request):
    try:
        list_movies = SpecificProfileModel.objects.get(identifier='Fantasy')
        array=[]
        for i in list_movies.recommendations:
            words = i.split('|')
            movie_id = words[0]
            movie = MovieModel.objects.get(movie_id=movie_id)
            array.append(movie)
        pass
    except:
        return HttpResponse(status=404)
        pass
    if request.method == 'GET':
        serializer = MovieModelSerializer(array, many=True)
        return JsonResponse(serializer.data, safe=False)
    pass

@csrf_exempt
def getLastLike(request,id):
    try:
        user_event = UserEventModel.objects(idx_user=id, rating=5).order_by("-time").limit(1)[0]
        idx_movie = user_event['idx_movie']
        movie = MovieModel.objects.get(idx=idx_movie)
    except:
        return HttpResponse(status=404)
    if request.method == 'GET':
        if movie:
            serializer = MovieModelSerializer(movie)
            return JsonResponse(serializer.data, safe=False)
        else:
            return HttpResponse(status=404)