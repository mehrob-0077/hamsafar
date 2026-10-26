from django.contrib.auth.models import BaseUserManager

class CostumUserManager(BaseUserManager):
    def _create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError("Необходимо указать имя пользователя")
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password) 
        user.save(using=self._db)
        return user

    def create_user(self,email,password,**extra_fields):
        extra_fields.setdefault("is_active",False)

        if extra_fields.get('is_active') is not False:
            extra_fields.setdefault("is_active",False)

        return self._create_user(email,password,**extra_fields)

    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault("is_active",True)
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)

        if extra_fields.get('is_active') is not True:
            raise ValueError("Суперпользователь должен быть активен")
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Поле is_staff должно быть True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Поле is_superuser должно быть True")

        return self._create_user(email,password,**extra_fields)
                     