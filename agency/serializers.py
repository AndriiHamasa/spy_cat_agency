# import datetime

# from django.db import transaction
# from django.shortcuts import get_object_or_404
from rest_framework import serializers
# from rest_framework.exceptions import ValidationError


from agency.models import Cat

class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = ("name", "years", "breed", "salary")

    def validate_breed(self, value):
        print("Validating of breed")
        return value

    def validate(self, data):

        if Cat.objects.filter(
                name=data["name"],
                years=data["years"],
                breed=data["breed"],
                salary=data["salary"]
        ).exists():
            raise serializers.ValidationError(
                "A cat with the same name, years, breed, and salary already exists."
            )
        return data


class CatListSerializer(CatSerializer):
    class Meta(CatSerializer.Meta):
        fields = CatSerializer.Meta.fields + ("id",)

