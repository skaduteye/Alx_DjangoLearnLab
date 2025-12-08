from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for the Notification model."""
    actor = serializers.ReadOnlyField(source='actor.username')
    actor_id = serializers.ReadOnlyField(source='actor.id')
    recipient = serializers.ReadOnlyField(source='recipient.username')
    recipient_id = serializers.ReadOnlyField(source='recipient.id')
    target_type = serializers.SerializerMethodField()
    target_id = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'recipient_id', 'actor', 'actor_id', 'verb', 
                  'target_type', 'target_id', 'timestamp', 'read']
        read_only_fields = ['id', 'recipient', 'recipient_id', 'actor', 'actor_id', 
                           'verb', 'target_type', 'target_id', 'timestamp']

    def get_target_type(self, obj):
        """Get the type of the target object."""
        if obj.target_content_type:
            return obj.target_content_type.model
        return None

    def get_target_id(self, obj):
        """Get the ID of the target object."""
        return obj.target_object_id
