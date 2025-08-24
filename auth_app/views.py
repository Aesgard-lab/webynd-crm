# auth_app/views.py
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import MyTokenObtainPairSerializer, MeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from gyms.models import Gym, GymMembership


class SetCurrentGymView(APIView):
    """
    Cambia la sede activa del usuario (current_gym).
    Reglas:
    - superadmin: puede fijar cualquier gym.
    - admin/staff: solo puede fijar gyms donde tenga GymMembership activa.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        gym_id = request.data.get("gym_id")
        if not gym_id:
            return Response({"detail": "gym_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            gym = Gym.objects.get(pk=gym_id)
        except Gym.DoesNotExist:
            return Response({"detail": "Gym not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        # Si no es superadmin, validar membresía activa en ese gym
        if getattr(user, "effective_role", None) != "superadmin":
            has_membership = GymMembership.objects.filter(
                user=user, gym=gym, is_active=True
            ).exists()
            if not has_membership:
                return Response(
                    {"detail": "No tienes membresía activa en ese gimnasio."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        user.current_gym = gym
        user.save(update_fields=["current_gym"])

        return Response(
            {"currentGym": {"id": gym.id, "name": gym.name, "slug": gym.slug}},
            status=status.HTTP_200_OK,
        )


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class MyTokenRefreshView(TokenRefreshView):
    pass


class MeView(APIView):
    authentication_classes = [JWTAuthentication]   # ← fuerza JWT
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(MeSerializer(request.user).data)
