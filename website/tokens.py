"""
تولید و اعتبارسنجی توکن بازیابی رمز عبور — پیاده‌سازی کاملاً سفارشی.

به‌جای استفاده از PasswordResetTokenGenerator آماده‌ی جنگو، اینجا از
django.core.signing (یک ابزار عمومی امضای داده در جنگو، نه چیزی مخصوص
auth) استفاده شده تا خودمان منطق تولید/اعتبارسنجی توکن را بنویسیم:

- توکن شامل شناسه‌ی کاربر (pk) و بخشی از هش رمز عبور فعلی اوست.
- امضا با کلید مخفی SECRET_KEY پروژه انجام می‌شود، پس بدون آن قابل جعل نیست.
- یک مهر زمانی (timestamp) هم داخل امضا هست، برای همین بعد از MAX_AGE
  (پیش‌فرض ۲۴ ساعت) توکن به‌صورت خودکار منقضی می‌شود.
- چون بخشی از هش رمز عبور فعلی در توکن قرار گرفته، به‌محض اینکه کاربر با
  همین توکن رمزش را عوض کند (یا خودش از جای دیگری رمز را عوض کند)، هش عوض
  می‌شود و توکن قبلی دیگر معتبر نیست؛ یعنی هر توکن فقط یک‌بار قابل استفاده است.
"""

from django.core import signing

RESET_TOKEN_SALT = "website.password-reset-confirm"
RESET_TOKEN_MAX_AGE = 60 * 60 * 24  # 24 ساعت، بر حسب ثانیه


def generate_reset_token(user):
    payload = {
        "pk": user.pk,
        "pwd": user.password[-20:],
    }
    return signing.dumps(payload, salt=RESET_TOKEN_SALT)


def verify_reset_token(user, token):
    if not token:
        return False
    try:
        data = signing.loads(token, salt=RESET_TOKEN_SALT, max_age=RESET_TOKEN_MAX_AGE)
    except signing.BadSignature:
        return False

    if data.get("pk") != user.pk:
        return False
    if data.get("pwd") != user.password[-20:]:
        return False
    return True
