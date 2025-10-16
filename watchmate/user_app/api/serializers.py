from rest_framework import serializers
from django.contrib.auth.models import User

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'}, min_length=8, max_length=128)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8, 'max_length': 128, 'style': {'input_type': 'password'}},
        }

    def save(self, **kwargs):
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        if User.objects.filter(username=self.validated_data['username']).exists():
            raise serializers.ValidationError({"username": "Username is already taken."})

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({"email": "Email is already registered."})
        
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        user.set_password(password)
        user.save()
        return user

