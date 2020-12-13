import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render
from django.http import JsonResponse
from .models import Message, Chat
from django.contrib.auth.models import User
from django.db.models import Q


class MessageData:
    def __init__(self, last_name, message_text, img_url=None):
        self.last_name = last_name
        self.message_text = message_text
        self.img_url = img_url


def messenger(request):
    chat_list = Chat.objects.filter(Q(message__message_from=request.user.socialprofile) |
                                    Q(message__message_to=request.user.socialprofile)).distinct()
    return render(request, 'messaging/messenger_main.html', {
        'chat_list': chat_list
    })


def chat_messenger(request, chat_id):
    chat = Chat.objects.get(pk=chat_id)
    return render(request, 'messaging/chat.html', {
        'chat': chat
    })


def send_modal_message(request):
    message_text = request.POST['message']
    channel_layer = get_channel_layer()
    send_to_id = request.POST['send_to_id']
    group_name = 'listener_%s' % send_to_id

    list_id = []
    list_id.append(str(send_to_id))
    list_id.append(str(request.user.id))
    list_id.sort()

    chat_name = list_id[0] + '_' + list_id[1]
    chat, created = Chat.objects.get_or_create(chat_name=chat_name)

    message = Message(
        message_text=message_text,
        message_from=request.user.socialprofile,
        message_to=User.objects.get(pk=send_to_id).socialprofile,
        chat=chat
    )
    message.save()

    if request.user.socialprofile.profile_img:
        message_data = MessageData(last_name=request.user.socialprofile.last_name,
                                   message_text=message_text, img_url=request.user.socialprofile.profile_img.url)
    else:
        message_data = MessageData(last_name=request.user.socialprofile.last_name,
                                   message_text=message_text)

    message_data_json = json.dumps(message_data.__dict__)

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "modal.message",
            "text": message_data_json,
        }
    )
    return JsonResponse({'': ''}, safe=False)

