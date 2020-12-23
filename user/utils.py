import jwt
import json
from functools import wraps

from django.http import JsonResponse

from user.models import User
from my_settings import SECRET_KEY, ALGORITHM

def id_auth(func):
    @wraps(func)
    def decorated_function(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization')
            print(access_token)
            payload      = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
            login_user   = User.objects.get(id = payload['user_id'])
            request.user = login_user
            return func(self, request, *args, **kwargs)

        except jwt.exceptions.DecodeError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status = 401)
        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status = 401)
    return decorated_function
