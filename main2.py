import os
import xml.etree.ElementTree as ET
from PIL import Image

# تنظیم مسیر اصلی که شامل همه XML و تصاویر است
dataset_dir = "dataset"  # همه فایل‌ها (XML + تصاویر) در اینجا هستند
yolo_dir = "labels_yolo"  # مسیر خروجی فایل‌های YOLO
classes_file = "classes.txt"  # فایل ذخیره لیست کلاس‌ها

# ایجاد پوشه خروجی در صورت عدم وجود
if not os.path.exists(yolo_dir):
    os.makedirs(yolo_dir)

# لیست کلاس‌های یکتا
classes = set()

# **مرحله 1: خواندن فایل‌های XML و استخراج کلاس‌ها**
for file in os.listdir(dataset_dir):
    if file.endswith(".xml"):  # فقط فایل‌های XML را پردازش کن
        tree = ET.parse(os.path.join(dataset_dir, file))
        root = tree.getroot()

        for obj in root.findall("object"):
            class_name = obj.find("name").text.strip()
            classes.add(class_name)

# ذخیره کلاس‌ها در `classes.txt`
classes = sorted(list(classes))  # مرتب‌سازی کلاس‌ها
with open(classes_file, "w", encoding="utf-8") as f:
    for cls in classes:
        f.write(cls + "\n")

print(f"✅ لیست کلاس‌ها در '{classes_file}' ذخیره شد.")

# **مرحله 2: پردازش فایل‌های XML و تبدیل به فرمت YOLO**
for file in os.listdir(dataset_dir):
    if not file.endswith(".xml"):
        continue  # فقط XML ها را بررسی کن

    tree = ET.parse(os.path.join(dataset_dir, file))
    root = tree.getroot()
    
    # استفاده از نام فایل XML برای نام تصویر
    base_name = os.path.splitext(file)[0]  # حذف ".xml"
    image_name = base_name + ".jpg"  # فرض می‌کنیم تصویر فرمت JPG دارد
    image_path = os.path.join(dataset_dir, image_name)

    # بررسی وجود تصویر متناظر
    if not os.path.exists(image_path):
        print(f"🚨 تصویر '{image_name}' پیدا نشد! از پردازش رد شد.")
        continue

    # دریافت ابعاد تصویر
    with Image.open(image_path) as img:
        image_width, image_height = img.size

    txt_filename = os.path.join(yolo_dir, base_name + ".txt")

    with open(txt_filename, "w") as out_file:
        for obj in root.findall("object"):
            class_name = obj.find("name").text.strip()
            if class_name not in classes:
                print(f"🚨 کلاس '{class_name}' در لیست کلاس‌ها نیست! رد شد.")
                continue
            class_id = classes.index(class_name)

            xml_box = obj.find("bndbox")
            xmin = int(xml_box.find("xmin").text)
            ymin = int(xml_box.find("ymin").text)
            xmax = int(xml_box.find("xmax").text)
            ymax = int(xml_box.find("ymax").text)

            # تبدیل مختصات به فرمت YOLO
            x_center = (xmin + xmax) / 2.0 / image_width
            y_center = (ymin + ymax) / 2.0 / image_height
            width = (xmax - xmin) / image_width
            height = (ymax - ymin) / image_height

            # ذخیره در فایل YOLO
            out_file.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

    print(f"✅ فایل '{txt_filename}' ایجاد شد.")

print("🚀 تبدیل تمام شد! فایل‌های YOLO در 'labels_yolo' قرار دارند.")
