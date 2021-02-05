from rest_framework import viewsets
from django.http import JsonResponse
from catalog.serializers import DoctorSerializer
from catalog.models import Doctor, DataLoad
from django.utils import timezone
# Create your views here.


class CatalogViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


def load_data_view(request):
    try:
        data, new = DataLoad.update_data()
        date = timezone.localtime(data.created_at).strftime('%d-%m-%y  %H:%M:%S')
        if new:
            message = "Данные успешно обновлены. "
            message_type = 'success'
        else:
            message = "Данные не изменились. "
            message_type = "info"
        message += f"Дата последнего обновления {date}"
    except Exception as err:
        message = f"Ошибка обновления. Попробуйте позже или обратитесь к администратору"
        message_type = "danger"
    return JsonResponse({
        "result": "ok",
        "message": message,
        "message_type": message_type
    }, status=200)


