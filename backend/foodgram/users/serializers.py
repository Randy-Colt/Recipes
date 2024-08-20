from rest_framework import serializers
from users import models


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Subscription
        fields = ('author', 'user', )
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=models.Subscription.objects.all(),
                fields=['author', 'user', ]
            )
        ]

    def create(self, validated_data):
        return models.Subscription.objects.create(
            user=self.context.get('request').user, **validated_data)

    def validate_author(self, value):
        if self.context.get('request').user == value:
            raise serializers.ValidationError(
                'You cant subscribe to yourself!')
        return value
