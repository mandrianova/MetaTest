import requests
from django.conf import settings
from django.db import models
from django.core.files.base import ContentFile


# Create your models here.

class Method(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


def get_image_path(instance, filename):
    return '{0}/{1}'.format(instance.id, filename)


class Photo(models.Model):
    source_url = models.URLField(null=True)
    full_source_url = models.URLField(null=True)
    small_source_url = models.URLField(null=True)
    large_source_url = models.URLField(null=True)
    source_file = models.ImageField(upload_to=get_image_path, null=True)
    full = models.ImageField(upload_to=get_image_path, null=True)
    small = models.ImageField(upload_to=get_image_path, null=True)
    large = models.ImageField(upload_to=get_image_path, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    source_id = models.CharField(max_length=20, unique=True)

    @staticmethod
    def get_photo_from_url(url: str) -> ContentFile:
        response = requests.get(url)
        if response.status_code != 200 or not response.content:
            raise LoadException('Load photo failed')
        return ContentFile(response.content)


class Doctor(models.Model):
    name = models.CharField(max_length=255)
    photo = models.OneToOneField(Photo, null=True, related_name='doctor', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    methods = models.ManyToManyField(Method, related_name='doctors')
    source_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class LoadException(Exception):
    pass


class DataLoad(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.created_at.strftime("%d-%m-%Y")

    @classmethod
    def _save_photo(cls, data: dict) -> Photo:
        photo = Photo.objects.filter(source_id=data['id']).first()
        if not photo:
            photo = Photo()
            photo.source_id = data['id']
            photo.save()
        thumbnails = data['thumbnails']
        photo.source_url = data['url']
        photo.full_source_url = thumbnails['full']['url']
        photo.large_source_url = thumbnails['large']['url']
        photo.small_source_url = thumbnails['small']['url']
        if not photo.source_file:
            photo.source_file.save('source.jpg', Photo.get_photo_from_url(data['url']), save=True)
            photo.full.save('full.jpg', Photo.get_photo_from_url(thumbnails['full']['url']), save=True)
            photo.large.save('large.jpg', Photo.get_photo_from_url(thumbnails['large']['url']), save=True)
            photo.small.save('small.jpg', Photo.get_photo_from_url(thumbnails['small']['url']), save=True)
        photo.save()
        return photo

    @classmethod
    def update_data(cls):
        """
        Load and update doctor's data
        :return: last DataLoad object, is new (bool)
        """
        url = f'https://api.airtable.com/v0/{settings.AIR_APP}/Psychotherapists'
        headers = {"Authorization": f"Bearer {settings.AIR_API_KEY}"}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise LoadException(f'{response.status_code} - {response.text}')
        last_data = DataLoad.objects.last()
        if last_data and last_data.data == response.json():
            return last_data, False
        new_data = DataLoad(data=response.json())
        if not new_data.data['records']:
            raise LoadException("No data")

        # Get deleted doctors
        if last_data:
            last_data_ids = set([doctor['id'] for doctor in last_data.data['records']])
        else:
            last_data_ids = set()
        new_data_ids = set([doctor['id'] for doctor in new_data.data['records']])
        deleted_doctors = last_data_ids - new_data_ids
        if deleted_doctors:
            Doctor.objects.filter(
                source_id__in=list(deleted_doctors)
            ).delete()

        # Get updated and new info
        for doctor_info in new_data.data['records']:
            doctor = Doctor.objects.filter(source_id=doctor_info["id"]).first()
            if not doctor:
                doctor = Doctor()
                doctor.source_id = doctor_info["id"]
            if not doctor_info['fields']:
                doctor.save()
                continue
            doctor.name = doctor_info['fields']['Имя']
            if doctor_info["fields"]["Методы"]:
                methods = [Method.objects.get_or_create(name=i)[0] for i in doctor_info["fields"]["Методы"]]
                doctor.save()
                doctor.methods.set(methods)
            if doctor_info["fields"]['Фотография'][0]:
                doctor.photo = cls._save_photo(doctor_info["fields"]['Фотография'][0])
            doctor.save()
        new_data.save()
        return new_data, True

    class Meta:
        ordering = ['created_at']
