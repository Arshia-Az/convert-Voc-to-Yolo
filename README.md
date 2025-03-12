# تبدیل VOC به YOLO

این اسکریپت برای تبدیل دیتاست با فرمت Pascal VOC به فرمت YOLO طراحی شده است.

## ویژگی‌ها
- تبدیل خودکار فایل‌های XML به فرمت YOLO
- ایجاد فایل `classes.txt` به صورت خودکار
- پشتیبانی از تصاویر JPG
- نمایش پیام‌های خطا و موفقیت

## نحوه استفاده

1. ساختار پوشه‌ها را به صورت زیر آماده کنید:
```
project_folder/
│
├── dataset/           # پوشه حاوی فایل‌های XML و تصاویر
│   ├── image1.jpg
│   ├── image1.xml
│   ├── image2.jpg
│   └── image2.xml
│
├── labels_yolo/       # پوشه خروجی (به صورت خودکار ایجاد می‌شود)
│
└── main.py           # اسکریپت اصلی
```

2. نیازمندی‌ها را نصب کنید:
```bash
pip install -r requirements.txt
```

3. اسکریپت را اجرا کنید:
```bash
python main.py
```

## نیازمندی‌ها
- Python 3.6+
- Pillow (PIL)

## خروجی
- فایل‌های txt در فرمت YOLO در پوشه `labels_yolo`
- فایل `classes.txt` حاوی لیست کلاس‌ها 