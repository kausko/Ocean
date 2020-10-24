import requests
import json
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from user.models import User
from .models import Chat


class ChatView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_queryset(self):
        query_set = Chat.objects.filter(user=self.request.user).order_by('createdAt')
        return query_set

    def get(self, request, *args, **kwargs):
        try:
            query_set = self.get_queryset()
            chats = get_chats(query_set)
            return Response({
                'success': True,
                'chats': chats
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'message': e.__str__()
            }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            text = data['text']
            chat = Chat(user=request.user, text=text, type=1)
            user = User.objects.get(email=request.user)
            if user.counter % 2 != 0:
                data = {
                    "email": "tanmaypardeshi@gmail.com",
                    "key": "7fce33c1921f253fc71df92912d274d5",
                    "counter": user.counter,
                    "string1": text,
                    "string2": '',
                    "string3": ''
                }
            else:
                string1 = get_text(1)
                string2 = get_text(2)
                data = {
                    "email": "tanmaypardeshi@gmail.com",
                    "key": "7fce33c1921f253fc71df92912d274d5",
                    "counter": user.counter,
                    "string1": string1,
                    "string2": string2,
                    "string3": text
                }
            chat.save()
            url = "http://127.0.0.1:5000/api/chat/"

            user.counter = user.counter + 1
            user.save()
            send = requests.post(url, json=data)
            chat = Chat(user=request.user, text=json.loads(send.text)[0]['reply'], type=2)
            chat.save()
            return Response({
                '_id': chat.pk,
                'createdAt': chat.createdAt,
                'text': json.loads(send.text)[0]['reply'],
                'user': {
                    '_id': chat.type
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'message': e.__str__()
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email=request.user)
            chat = Chat.objects.filter(user=user)
            chat.delete()
            return  Response({
                'success': True,
                'message': 'Cleared Chat history'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return  Response({
                'success': False,
                'message': e.__str__()
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_chats(chats):
    chat_list = []
    objects = {}
    user = {}
    for chat in chats:
        user['_id'] = chat.type
        objects['_id'] = chat.pk
        objects['createdAt'] = chat.createdAt
        objects['text'] = chat.text
        objects['user'] = user
        chat_list.append(objects)
        user = {}
        objects = {}
    return chat_list


def get_text(num):
    obj = Chat.objects.filter(type=num).order_by('createdAt')
    total = obj.count()
    temp = obj[total - 1]
    return temp.text
