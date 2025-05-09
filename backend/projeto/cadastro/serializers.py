from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

usuario = get_user_model()


class registroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = usuario
        fields = '__all__'

    def validate_tipo(self, value):
        if value not in usuario.TipoUsuario.values:
            raise serializers.ValidationError("Tipo de usuário inválido.")
        return value

    def create(self, validated_data):
        groups = validated_data.pop('groups', None)
        user = usuario.objects.create_user(**validated_data)
        user_permissions = validated_data.pop('user_permissions', None)
        
        if groups:
            user.groups.set(groups)
        
        if user_permissions:
            user.user_permissions.set(user_permissions)  
        
        return user
        
    

class loginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(username = email, password = password)

        if user is None:
            raise serializers.ValidationError("credenciais inválidas")
        
        if not user.is_active:
            raise serializers.ValidationError("Usuário inativo")
        
        data["user"] = user

        return data
    


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = usuario
        fields = ['id', 'nome', 'sobrenome', 'email', 'tipo']
