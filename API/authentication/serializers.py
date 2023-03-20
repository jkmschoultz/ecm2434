from rest_framework import serializers
from database.models import User

class RegisterUser(serializers.ModelSerializer):
    # Serializer for creating a user
    class Meta:
        # Metadata for the user instance to be created
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Create the user instance
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
