import requests
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.conf import settings


from agency.models import Cat, Target, Mission


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = ("name", "years", "breed", "salary")

    def validate_breed(self, breed_name):
        response = requests.get(settings.CAT_API_BASE_URL)
        if response.status_code != 200:
            raise ValidationError("Unable to connect to TheCatAPI.")

        breeds = response.json()
        breed_names = [breed["name"].lower() for breed in breeds]
        if breed_name.lower() not in breed_names:
            raise ValidationError(f"Breed '{breed_name}' does not exist.")

        return breed_name

    def validate(self, data):

        if Cat.objects.filter(
            name=data["name"],
            years=data["years"],
            breed=data["breed"],
            salary=data["salary"],
        ).exists():
            raise serializers.ValidationError(
                "A cat with the same name, years, breed, and salary already exists."
            )
        return data


class CatListSerializer(CatSerializer):
    class Meta(CatSerializer.Meta):
        fields = CatSerializer.Meta.fields + ("id",)


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ("name", "country", "notes", "target_completed")


class TargetReadSerializer(TargetSerializer):
    class Meta(TargetSerializer.Meta):
        fields = TargetSerializer.Meta.fields + ("id",)


class MissionDetailSerializer(serializers.ModelSerializer):
    targets = TargetReadSerializer(many=True)
    cat = CatSerializer()

    class Meta:
        model = Mission
        fields = (
            "id",
            "cat",
            "mission_completed",
            "targets",
            "created_at",
            "updated_at",
        )


class MissionListSerializer(MissionDetailSerializer):
    targets = serializers.SerializerMethodField()
    cat = serializers.PrimaryKeyRelatedField(read_only=True)

    def get_targets(self, obj):
        return [target.name for target in obj.targets.all()]


class MissionCreateSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True)

    class Meta:
        model = Mission
        fields = ("cat", "targets")

    def create(self, validated_data):
        targets_data = validated_data.pop("targets")
        mission = Mission.objects.create(**validated_data)

        if not 1 <= len(targets_data) <= 3:
            raise serializers.ValidationError(
                "Count of targets should be within 1 to 3.", code="invalid_target_count"
            )

        target_names = [target["name"] + target["country"] for target in targets_data]
        if len(target_names) != len(set(target_names)):
            raise serializers.ValidationError(
                "Targets should be unique in one mission.",
                code="duplicate_target_names",
            )

        for target_data in targets_data:
            Target.objects.create(mission=mission, **target_data)
        return mission


class MissionAssignCatSerializer(serializers.ModelSerializer):
    cat = serializers.PrimaryKeyRelatedField(queryset=Cat.objects.all())

    class Meta:
        model = Mission
        fields = ("cat",)
