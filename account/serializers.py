import profile
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


from .models import Profile


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'},)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()
        Profile(user=user).save()
        return user



class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(max_length=255, read_only=True)
    refresh = serializers.CharField(max_length=255, read_only=True)
    id = serializers.IntegerField(read_only=True)
    email = serializers.CharField(max_length=255, read_only=True)
    profile_image = serializers.ImageField(read_only=True)
    following = serializers.ListField(child=serializers.CharField(), read_only=True)


    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                {'data' : 'A user with this username and password is not found.'}
            )
        try:
            token = self.get_tokens_for_user(user)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {'data' : 'User with given username and password does not exists'}
            )

        return {
            'id': user.id,
            'username':user.username,
            'email':user.email,
            "refresh": token['refresh'], 
            'access': token['access']
        }
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        user = User.objects.get(id=instance['id'])
        if user.profile.profile_image:
            rep['profile_image'] = user.profile.profile_image.url
        else:
            rep['profile_image'] = ""
        rep['following'] = user.profile.following.values_list('id', flat=True)
        return rep


    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username')


class ProfileUpdateSerializer(serializers.ModelSerializer):
    user = UpdateUserSerializer()

    class Meta:
        model = Profile
        exclude = ('created_at', 'updated_at', 'following', 'followers')

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('user').get('first_name', instance.first_name)
        instance.last_name = validated_data.get('user').get('last_name', instance.last_name)
        instance.save()

        profile = instance.profile
        profile.dob = validated_data.get('dob', profile.dob)
        profile.phone = validated_data.get('phone', profile.phone)
        profile.about = validated_data.get('about', profile.about)
        profile.city = validated_data.get('city', profile.city)
        profile.full_address = validated_data.get('full_address', profile.full_address)
        profile.state = validated_data.get('state', profile.state)
        profile.country = validated_data.get('country', profile.country)
        profile.postcode = validated_data.get('postcode', profile.postcode)
        profile.relationship = validated_data.get('relationship', profile.relationship)
        profile.save()

        return instance


class ProfileImageUploadSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=False)
    cover_image = serializers.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ('profile_image', 'cover_image',)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6,max_length=50)