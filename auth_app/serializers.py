# auth_app/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from gyms.models import Gym, GymMembership

User = get_user_model()


# === TOKEN SERIALIZER ===
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Claims extra ligeros
        token["role"] = getattr(user, "effective_role", None)
        token["current_gym_id"] = getattr(user, "current_gym_id", None)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user  # type: ignore[assignment]
        data["user"] = {
            "id": user.id,
            "email": user.email,
            "fullName": user.get_full_name() or user.get_username(),
            "avatar": user.photo.url if getattr(user, "photo", None) else None,
            "role": getattr(user, "effective_role", None),
        }
        return data


# === ME SERIALIZER (multi-gim) ===
class GymBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = ("id", "name", "slug")


class GymMembershipSerializer(serializers.ModelSerializer):
    gym = GymBriefSerializer(read_only=True)

    class Meta:
        model = GymMembership
        fields = (
            "gym",
            "role",
            "can_manage_clients",
            "can_manage_cash",
            "can_manage_activities",
            "can_manage_bonuses",
        )


class MeSerializer(serializers.ModelSerializer):
    fullName = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    memberships = serializers.SerializerMethodField()
    currentGym = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "fullName",
            "avatar",
            "role",
            "memberships",
            "currentGym",
        )

    # ----- getters -----
    def get_fullName(self, obj):
        return obj.get_full_name() or obj.email

    def get_avatar(self, obj):
        return obj.photo.url if getattr(obj, "photo", None) else None

    def get_role(self, obj):
        return getattr(obj, "effective_role", None)

    def get_memberships(self, obj):
        qs = GymMembership.objects.select_related("gym").filter(user=obj, is_active=True)
        return GymMembershipSerializer(qs, many=True).data

    def get_currentGym(self, obj):
        # Usa current_gym si es válido (y el user tiene membresía allí)
        cg = getattr(obj, "current_gym", None)
        if cg and GymMembership.objects.filter(user=obj, gym=cg, is_active=True).exists():
            return {"id": cg.id, "name": cg.name, "slug": cg.slug}

        # Si no, toma la primera membresía activa
        m = GymMembership.objects.select_related("gym").filter(user=obj, is_active=True).first()
        if m:
            return {"id": m.gym.id, "name": m.gym.name, "slug": m.gym.slug}
        return None

