from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from agency.models import Cat, Mission, Target
from agency.serializers import (
    CatSerializer,
    CatListSerializer,
    MissionListSerializer,
    MissionCreateSerializer,
    MissionDetailSerializer,
    MissionAssignCatSerializer,
    TargetSerializer
)


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CatListSerializer
        return CatSerializer

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.method != "PATCH":
            return Response(
                {"error": "Only PATCH method is allowed for updating salary"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

        if any(field not in ["salary"] for field in request.data.keys()):
            return Response(
                {"error": "Only 'salary' field can be updated"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cat = self.get_object()

        if "salary" in request.data:
            cat.salary = request.data["salary"]
            cat.save()


class TargetViewSet(viewsets.ModelViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer

    def get_queryset(self):
        mission_id = self.kwargs.get("mission_id")
        return Target.objects.filter(mission_id=mission_id)

    def update(self, request, *args, **kwargs):
        target = self.get_object()

        if target.target_completed:
            return Response({"error": "Target is already completed. Cannot update."}, status=status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)


class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return MissionListSerializer
        elif self.action == "create":
            return MissionCreateSerializer
        elif self.action == "assign_cat":
            print("We are choosing to assign cat")
            return MissionAssignCatSerializer
        return MissionDetailSerializer

    @action(detail=True, methods=["patch"], url_path="assign-cat")
    def assign_cat(self, request, pk=None):
        print("In assign_cat action")
        mission = self.get_object()
        cat_id = request.data.get("cat")
        if cat_id:
            try:
                cat = Cat.objects.get(id=cat_id)
                mission.cat = cat
                mission.save()
                serializer = MissionDetailSerializer(mission)
                return Response(serializer.data)
                # return Response({"status": "cat assigned"})
            except Cat.DoesNotExist:
                return Response({"error": "Cat not found"}, status=404)
        return Response({"error": "No cat provided"}, status=400)

    @action(detail=True, methods=["patch"], url_path="complete_mission")
    def assign_cat(self, request, pk=None):
        mission = self.get_object()
        if not mission.cat:
            return Response({"error": "could not be completed without a cat"}, status=400)
        if mission.mission_completed:
            return Response({"error": "Mission already completed"}, status=400)

        mission.mission_completed = True
        mission.save()
        serializer = MissionDetailSerializer(mission)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"], url_path=r"target/(?P<target_id>\d+)")
    def update_target(self, request, pk=None, target_id=None):
        mission = Mission.objects.get(id=pk)

        if mission.mission_completed:
            return Response(
                {"error": "Mission is already completed. Cannot update."},
                status=status.HTTP_400_BAD_REQUEST)
        try:
            target = Target.objects.get(id=target_id, mission=mission)
        except Target.DoesNotExist:
            return Response({"error": "Target not found"},
                            status=status.HTTP_404_NOT_FOUND)

        if target.target_completed:
            return Response(
                {"error": "Target is already completed. Cannot update."},
                status=status.HTTP_400_BAD_REQUEST)

        serializer = TargetSerializer(target, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        mission = self.get_object()
        if mission.cat:
            return Response(
                {
                    "error": "Mission cannot be deleted because it is assigned to a cat"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)
