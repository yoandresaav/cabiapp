from django.contrib.auth import get_user_model

class EmailOrUsernameModelBackend(object):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = UserModel.objects.get(**kwargs)
            
            # Verifico si es texto plano o esta encriptada
            if user.password == password or user.check_password(password):
                return user
            else:
                print("NO EXISTE ESE USUAIRO")
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None