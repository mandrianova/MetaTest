from rest_framework import serializers

from catalog.models import Doctor, Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['full', 'small', 'large', 'small_source_url', 'large_source_url']


class DoctorSerializer(serializers.ModelSerializer):
    photo = PhotoSerializer(read_only=True)
    methods = serializers.StringRelatedField(many=True)

    class Meta:
        model = Doctor
        fields = ['id', 'name', 'photo', 'methods']



