import datetime

import requests
from django.core.cache import cache
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from rest_framework import viewsets, filters, status, views
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import FoodSerializer
from .models import Food


def image_upload(request):
    if request.method == "POST" and request.FILES["image_file"]:
        image_file = request.FILES["image_file"]
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        image_url = fs.url(filename)
        print(image_url)
        return render(request, "upload.html", {
            "image_url": image_url
        })
    return render(request, "upload.html")

# TODO: environment variable
TELEGRAM_BOT_TOKEN = '1115783483:AAE2pJLsDCIc0x4HosJmrFKuUI0uw_yePtI'
@api_view(['GET'])
def notify_user_about_missing_expiry_date(request):
    item_name = request.GET.get('item')
    if not item_name:
        return Response({'message': 'item not specified'}, status=status.HTTP_204_NO_CONTENT)

    # TODO: Change the hardcoded chat id
    chat_id = request.GET.get('chat_id', '392671187')
    notification_text = 'Please /setExpiry for {}'.format(item_name)
    send_msg_url = 'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={notification_text}'.format(
        bot_token=TELEGRAM_BOT_TOKEN,
        chat_id=chat_id,
        notification_text=notification_text
    )
    response = requests.get(url=send_msg_url)
    if response.status_code != status.HTTP_200_OK:
        raise Exception('Error pushing notification to Telegram bot endpoint!')


    return Response({
        'message': 'Notification pushed!'
        # 'data': request.data
    })


class ExpiryDate(views.APIView):
    def get(self, request, format=None):
        default_expiry_date = (datetime.datetime.today() + datetime.timedelta(days=3)).date()
        expiry_date = cache.get('expiry_date', default=default_expiry_date)
        return Response({
            'expiry_date': expiry_date
        }, status=status.HTTP_200_OK)


class SetExpiryDate(views.APIView):
    def get(self, request, format=None):
        expiry_date = request.GET.get('date')
        cache.set('expiry_date', expiry_date)
        return Response({
            'message': 'Expiry date set!'
        }, status=status.HTTP_200_OK)


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    
    # def create(self, request, *args, **kwargs):
    #     if request.data['expiry_date'] == '':
    #         modified_request_data = request.data.copy()
    #         # TODO: this is a dummy response from Telegram
    #         # TODO: logger
    #         modified_request_data['expiry_date'] = prompt_expiry_date_from_user(request.data['name'], request.data['image'])
    #         serializer = self.get_serializer(data=modified_request_data)
    #     else:
    #         serializer = self.get_serializer(data=request.data)
    #     serializer = self.get_serializer(data=request.data)
    #
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# # TODO: environment variable
# TELEGRAM_BOT_TOKEN = '1115783483:AAE2pJLsDCIc0x4HosJmrFKuUI0uw_yePtI'
# def prompt_expiry_date_from_user(item_name, image):
#     '''
#     Returns a date object from telegram user
#     '''
#     print(item_name)
#     print(image)
#     # TODO: prompt user input from telegram
#
#     # TODO: Change the hardcoded chat id
#     chat_id = '392671187'
#     notification_text = 'Please /setExpiry for {}'.format(item_name)
#     send_msg_url = 'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={notification_text}'.format(
#         bot_token=TELEGRAM_BOT_TOKEN,
#         chat_id=chat_id,
#         notification_text=notification_text
#     )
#     response = requests.get(url=send_msg_url)
#     if response.status_code != status.HTTP_200_OK:
#         raise Exception('Error pushing notification to Telegram bot endpoint!')
#
#
#     # get_updates_url = 'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}'.format(
#     #     bot_token=TELEGRAM_BOT_TOKEN,
#     #     chat_id=chat_id
#     # )
#     # response = requests.get(url=get_updates_url)
#
#
#     return datetime.datetime.today().date()