import os
import xml.etree.ElementTree as ET
from PIL import Image

# تنظیم مسیرها
xml_dir = "Annotations"  # مسیر فایل‌های XML
image_dir = "Images"  # مسیر تصاویر
yolo_dir = "labels_yolo"  # مسیر خروجی YOLO
classes_file = "classes.txt"  # فایل ذخیره کلاس‌ها

# ایجاد پوشه خروجی اگر وجود ندارد
if not os.path.exists(yolo_dir):
    os.makedirs(yolo_dir)

# لیست کلاس‌های یکتا
classes = set()

# مرحله 1: استخراج کلاس‌ها از فایل‌های XML
for xml_file in os.listdir(xml_dir):
    if not xml_file.endswith(".xml"):
        continue

    tree = ET.parse(os.path.join(xml_dir, xml_file))
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

# مرحله 2: تبدیل XML به YOLO
for xml_file in os.listdir(xml_dir):
    if not xml_file.endswith(".xml"):
        continue

    tree = ET.parse(os.path.join(xml_dir, xml_file))
    root = tree.getroot()
    
    # استفاده از نام فایل XML به‌عنوان نام تصویر
    image_name = os.path.splitext(xml_file)[0] + ".jpg"
    image_path = os.path.join(image_dir, image_name)

    if not os.path.exists(image_path):
        print(f"🚨 تصویر {image_name} پیدا نشد! از پردازش رد شد.")
        continue

    with Image.open(image_path) as img:
        image_width, image_height = img.size

    txt_filename = os.path.join(yolo_dir, image_name.replace(".jpg", ".txt"))

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

            # تبدیل مختصات به YOLO
            x_center = (xmin + xmax) / 2.0 / image_width
            y_center = (ymin + ymax) / 2.0 / image_height
            width = (xmax - xmin) / image_width
            height = (ymax - ymin) / image_height

            # ذخیره در فایل YOLO
            out_file.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

    print(f"✅ فایل '{txt_filename}' ایجاد شد.")

print("🚀 تبدیل تمام شد! بررسی کنید که فایل‌های YOLO در 'labels_yolo' قرار دارند.")
