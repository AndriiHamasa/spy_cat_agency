from django.db import models


class Cat(models.Model):
    name = models.CharField(max_length=100)
    years = models.IntegerField()
    breed = models.CharField(max_length=100)
    salary = models.IntegerField()


class Mission(models.Model):
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE, related_name="Missions")
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Target(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    notes = models.TextField()
    is_complete = models.BooleanField(default=False)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name="targets")