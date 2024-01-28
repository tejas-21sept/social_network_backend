from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.validators import EmailValidator
from django.db import models


class UserManager(BaseUserManager):
    use_in_migration = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email), **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30)
    mobile_number = models.CharField(max_length=15, blank=True)
    bio = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pics/", blank=True, null=True
    )
    cover_picture = models.ImageField(upload_to="cover_pics/", blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_of_birth = models.DateField(blank=True, null=True)
    last_active = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "date_of_birth"]

    objects = UserManager()

    def __str__(self):
        return self.email


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_requests"
    )
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_requests"
    )
    status = models.CharField(
        max_length=10,
        choices=(
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ),
    )
    created_at = models.DateTimeField(auto_now_add=True)
