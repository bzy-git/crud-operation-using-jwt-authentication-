from rest_framework import serializers, status
from . models import * 

class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = '__all__'
        
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'name', 'email', 'password', 'confirm_password'
        ]
        read_only_fields = ['confirm_password']

    def create(self, validated_data):

        if not validated_data.get('password') or not validated_data.get(
                'confirm_password'):
            error_null_pass = {
                'error': True,
                'message': "Password or confirm password cannot be blank.",
                'status': status.HTTP_400_BAD_REQUEST
            }
            raise serializers.ValidationError(error_null_pass)

        if validated_data.get('password') != validated_data.get(
                'confirm_password'):
            error_mismatch_pass = {
                'error': True,
                'message': "Password and confirm password do not match.",
                'status': status.HTTP_400_BAD_REQUEST
            }
            raise serializers.ValidationError(error_mismatch_pass)

        user = User.objects.create_user(
            name=validated_data.get('name'),
            email=validated_data.get('email'),
            password=validated_data.get('password'),
        )
        return user




class PostUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ['title', 'content']