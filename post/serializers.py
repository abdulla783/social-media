from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    class Meta:
        model = Post
        fields = '__all__'
        # exclude = ('created_at', 'updated_at')

    def to_representation(self, instance):
        import json
        rep = super().to_representation(instance)
        rep['user'] = instance.user.username
        rep['user_id'] = instance.user.id
        if instance.user.profile.profile_image:
            rep['profile_image'] = instance.user.profile.profile_image.url
        else:
            rep['profile_image'] = ""
        return rep