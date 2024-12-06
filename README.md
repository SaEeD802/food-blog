# وبلاگ آشپزی فارسی 🍳

یک پلتفرم وبلاگ آشپزی با جنگو که به کاربران اجازه می‌دهد دستورهای پخت خود را به اشتراک بگذارند، نظر دهند و امتیاز بدهند.

## ویژگی‌ها ✨

- 👤 سیستم احراز هویت کاربران
- 📝 ایجاد، ویرایش و حذف دستورهای پخت
- 🏷️ دسته‌بندی و برچسب‌گذاری دستورها
- ⭐ سیستم امتیازدهی و نظرات
- ❤️ لایک و نشان‌گذاری دستورها
- 🔍 جستجوی پیشرفته در دستورها
- 📱 رابط کاربری ریسپانسیو
- 🇮🇷 پشتیبانی کامل از زبان فارسی و RTL

## پیش‌نیازها 📋

- Python 3.8+
- Django 4.2+
- pip (مدیر بسته پایتون)

## نصب و راه‌اندازی 🚀

1. کلون کردن مخزن:
```bash
git clone https://github.com/YOUR-USERNAME/food-blog.git
cd food-blog
```

2. ساخت محیط مجازی:
```bash
python -m venv venv
source venv/bin/activate  # برای لینوکس/مک
venv\Scripts\activate     # برای ویندوز
```

3. نصب وابستگی‌ها:
```bash
pip install -r requirements.txt
```

4. اعمال مایگریشن‌ها:
```bash
python manage.py migrate
```

5. ساخت کاربر ادمین:
```bash
python manage.py createsuperuser
```

6. اجرای سرور توسعه:
```bash
python manage.py runserver
```

حالا می‌توانید به آدرس `http://127.0.0.1:8000` مراجعه کنید.

## ساختار پروژه 📁

```
food-blog/
├── accounts/          # اپ مدیریت کاربران
├── blog/              # اپ اصلی وبلاگ
├── food_blog/         # تنظیمات اصلی پروژه
├── media/            # فایل‌های آپلود شده
├── static/           # فایل‌های استاتیک
├── templates/        # قالب‌های عمومی
├── manage.py
└── requirements.txt
```

## مدل‌های داده 💾

- **Post**: دستورهای پخت
- **Category**: دسته‌بندی‌ها
- **Tag**: برچسب‌ها
- **Ingredient**: مواد اولیه
- **RecipeIngredient**: ارتباط بین دستور و مواد
- **Comment**: نظرات کاربران

## مشارکت 🤝

1. Fork کردن پروژه
2. ساخت یک branch جدید (`git checkout -b feature/amazing-feature`)
3. Commit کردن تغییرات (`git commit -m 'Add some amazing feature'`)
4. Push کردن به branch (`git push origin feature/amazing-feature`)
5. ایجاد یک Pull Request

## تماس 📧

لینک پروژه: [https://github.com//SaEeD802/food-blog](https://github.com//SaEeD802/food-blog)
