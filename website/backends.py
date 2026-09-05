from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

UserModel = get_user_model()


class EmailOrUsernameModelBackend(ModelBackend):
    """
    این بک‌اند اجازه می‌دهد کاربر هم با نام کاربری و هم با ایمیل وارد شود.
    مقداری که کاربر در فیلد ورودی می‌نویسد، هم با username و هم با email
    مقایسه می‌شود (با or) و هر کدام مطابقت داشت همان کاربر بازگردانده می‌شود.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return None

        try:
            user = UserModel._default_manager.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
        except UserModel.DoesNotExist:
            return None
        except UserModel.MultipleObjectsReturned:
            # اگر بیش از یک کاربر با این شرط پیدا شد (مثلاً ایمیل تکراری قدیمی)
            user = UserModel._default_manager.filter(
                Q(username__iexact=username) | Q(email__iexact=username)
            ).order_by('id').first()

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
