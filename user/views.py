import re
import json
import bcrypt

from django.http  import JsonResponse
from django.views import View

from user.models  import User
from my_settings  import SECRET_KEY, ALGORITHM

REGEX_EMAIL        = '([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+(\.[a-zA-Z]{2,4}))'
REGEX_PASSWORD     = '^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            name     = data['name']
            email    = data['email']
            password = data['password']
            language = 'ko-kr'
            country  = 'South Korea'
            
            
            assert not User.objects.filter(name = name), "ALREADY_EXISTS_ACCOUNT"
            assert re.match(REGEX_EMAIL, email), "INVALID_EMAIL_FORMAT"
            assert re.match(REGEX_PASSWORD, password), "INVALID_PASSWORD_FORMAT"

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()

            User.objects.create(email = email, password = hashed_pasword, language = language, country = country, username = name)
            return JsonResponse({"message": "SUCCESS"}, status = 201)
        except json.JSONDecodeError as e:
            return JsonResponse({"message": f"{e}"}, status = 400)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)
        except AssertionError as e:
            return JsonResponse({"message": f"{e}"}, status = 400)

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            email    = data['email']
            password = data['password']

            signin_user = User.objects.get(email = email)

            if bcrypt.checkpw(password.encode('utf-8'), signin_user.password.encode('utf-8')):
                access_token = jwt.encode({'user_id': signin_user.id}, SECRET_KEY, algorithm = ALGORITHM)
                return JsonResponse({"message": "SUCCESS", "access_token": access_token.decode('utf-8')}, status = 200)
            else:
                return JsonResponse({"message": "INVALID_USER_NAME_OR_PASSWORD"}, status = 401)
