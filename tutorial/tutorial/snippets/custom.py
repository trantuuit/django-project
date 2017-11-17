from snippets.models import UserModel
from rest_framework import authentication
from rest_framework import exceptions

class ExampleAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        userid = request['userid']
        password = request['password']
        print(userid)
        if not ( userid and password ):
            return None
        try:
            user = UserModel.objects.get(user_id=userid, password = password)
            print(user)
        except UserModel.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return user