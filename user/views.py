import re
import json
import bcrypt
import jwt

from django.http  import JsonResponse
from django.views import View

from user.models  import User, Language, Country
from my_settings  import SECRET_KEY, ALGORITHM

REGEX_EMAIL     = '([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+(\.[a-zA-Z]{2,4}))'
REGEX_PASSWORD  = '^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'


class SignUpView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            name     = data['name']
            email    = data['email']
            password = data['password']

            language = Language.objects.get(name=data.get('language', 'ko'))
            country  = Country.objects.get(name=data.get('country', 'KR'))

            assert re.match(REGEX_EMAIL, email), "INVALID_EMAIL_FORMAT"
            assert re.match(REGEX_PASSWORD, password), "INVALID_PASSWORD_FORMAT"

            assert not User.objects.filter(email=email), "ALREADY_EXISTS_ACCOUNT"
            assert not User.objects.filter(username=name), "ALREADY_EXISTS_USERNAME"

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()

            User.objects.create(
                    email    = email,
                    password = hashed_password,
                    language = language,
                    country  = country,
                    username = name
            )
            return JsonResponse({"message": "SUCCESS"}, status = 201)

        except json.JSONDecodeError as e:
            return JsonResponse({"message": f"{e}"}, status = 400)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)
        except AssertionError as e:
            return JsonResponse({"message": f"{e}"}, status = 400)
        except Language.DoesNotExist:
            return JsonResponse({"message": "UNSUPPORTED_LANGUAGE"}, status = 400)
        except Country.DoesNotExist:
            return JsonResponse({"message": "UNSUPPORTED_COUNTRY"}, status = 400)

