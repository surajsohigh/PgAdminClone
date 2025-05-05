from rest_framework import serializers
from .models import MyUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only':True}
        }

    def create(self, validate_data):
        return MyUser.objects.create_user(**validate_data)

    def validate_email(self, email):
        print("h")
        if MyUser.objects.filter(email=email):
            raise serializers.ValidationError("Email Already Exist")  

        return email
    
    
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = MyUser
        exclude = ("role",)  # Use a tuple (or a list ["modified"])


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        exclude = ("password",)  # Use a tuple (or a list ["modified"])
