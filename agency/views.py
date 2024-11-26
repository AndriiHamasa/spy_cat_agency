from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from agency.models import Cat
from agency.serializers import CatSerializer, CatListSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CatListSerializer
        return CatSerializer

    def destroy(self, request, *args, **kwargs):
        # cat = self.get_object()
        print("checkin if cat is busy")
        # if cat.Missions.exists():
        #     return Response(
        #         {
        #             "error": "Cannot delete cat because it is assigned to a mission"},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if "id" in request.data:
            return Response(
                {"error": "'id' field should not be provided for updates"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().update(request, *args, **kwargs)
