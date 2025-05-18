# --- START OF FILE serializer.py ---

from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Campos comuns para listagem: id, username, e talvez nome/email.
        # Você pode ajustar conforme sua necessidade.
        fields = ("id", "username", "first_name", "last_name", "email") # Sem a senha

class UserDetailSerializer(serializers.ModelSerializer):
    # Mantém o nome 'senha' para o campo de entrada da senha, para consistência
    # mas ele mapeará para o campo 'password' do modelo User.
    senha = serializers.CharField(
        write_only=True,
        required=False, # Torna a senha opcional na atualização
        style={"input_type": "password"}
    )

    class Meta:
        model = User
        # Adiciona os campos padrão do User. 'password' é tratado pelo campo 'senha'.
        fields = ("id", "username", "first_name", "last_name", "email", "senha")
        extra_kwargs = {
            'username': {'required': True}, # Username é obrigatório
            'email': {'required': False}, # Email pode ser opcional dependendo da sua configuração
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def create(self, validated_data):
        """Sobrescreve o método create para criar um usuário, aplicando hashing na senha."""
        # Remove 'senha' de validated_data se existir, caso contrário, None.
        password = validated_data.pop("senha", None)

        # O username é obrigatório para o modelo User.
        # Outros campos como email, first_name, last_name virão de validated_data.
        user = User.objects.create_user(**validated_data) # create_user lida com username e senha

        # Se a senha foi fornecida via 'senha', atualize-a (create_user pode já ter pedido)
        # create_user já espera 'password' em kwargs se não for None, mas aqui garantimos que
        # o campo 'senha' do nosso serializer seja usado se presente.
        if password:
            user.set_password(password) # set_password aplica hashing
            user.save()

        return user

    def update(self, instance, validated_data):
        """Sobrescreve o método update para atualizar um usuário, aplicando hashing na senha se fornecida."""
        password = validated_data.pop("senha", None)  # Tenta obter a senha

        # Atualiza outros campos do usuário
        # O username geralmente não é alterado em updates, mas pode ser, dependendo da política.
        # Se for permitir alteração de username, certifique-se das implicações (ex: unicidade).
        instance.username = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)

        if password is not None:
            instance.set_password(password)  # set_password aplica o hashing

        instance.save()
        return instance

# --- END OF FILE serializer.py ---
