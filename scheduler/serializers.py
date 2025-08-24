from rest_framework import serializers
from .models import ScheduledSession, Reservation

class ScheduledSessionSerializer(serializers.ModelSerializer):
    reservation_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ScheduledSession
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    session_detail = serializers.StringRelatedField(source='session', read_only=True)
    client_name = serializers.StringRelatedField(source='client', read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'
