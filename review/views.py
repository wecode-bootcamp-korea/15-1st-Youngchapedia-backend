import json

from django.shortcuts import render
from django.utils     import timezone
from django.views     import View

from review.models  import Review
from user.models    import User
from user.utils     import id_auth
from content.models import Content


class ReviewView(View):
    @id_auth
    def post(self, request, content_pk):
        try:
            data    = json.loads(request.body)
            user    = request.user
            content = Content.objects.get(id = content_pk)
            body    = data['body']
