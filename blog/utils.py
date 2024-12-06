import re

def persian_slugify(text):
    """تبدیل متن فارسی به اسلاگ"""
    # حذف کاراکترهای خاص و جایگزینی با خط تیره
    text = re.sub(r'[^\w\s-]', '', text)
    # جایگزینی فاصله‌ها با خط تیره
    text = re.sub(r'[-\s]+', '-', text)
    # حذف خط تیره‌های اضافی از ابتدا و انتها
    return text.strip('-')
