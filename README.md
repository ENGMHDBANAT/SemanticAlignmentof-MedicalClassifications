# تشغيل المشروع

## 1. المتطلبات المسبقة
Python 3.14.6 على Windows.

## 2. فتح مجلد المشروع
```cmd
cd /d "D:\project\SemanticAlignmentof MedicalClassifications"
```

## 3. إنشاء البيئة الافتراضية
```cmd
python -m venv .venv
```

## 4. تفعيل البيئة الافتراضية
```cmd
.venv\Scripts\activate
```

## 5. تحديث pip
```cmd
python -m pip install --upgrade pip
```

## 6. تثبيت جميع المكتبات
```cmd
pip install -r requirements.txt
```

## 7. إعداد ملفات البيئة
لا يوجد ملف `.env` مستقل في النسخة الحالية.

## 8. إعداد قاعدة البيانات
لا توجد قاعدة بيانات مستقلة أو migrations مطلوبة.

## 9. إعداد Frontend
لا يوجد Frontend مستقل؛ واجهة المشروع تعمل عبر Streamlit مباشرة.

## 10. تشغيل المشروع
```cmd
streamlit run icd_app.py
```

## 11. فتح المشروع
فتح هذا الرابط في المتصفح:
```cmd
http://localhost:8501
```

## 12. اختبار التشغيل
1. افتح الصفحة المحلية.
2. اكتب عدة Terms في مربع الإدخال.
3. اضغط Start Fetching.
4. تأكد من ظهور الجدول وكتابة الملف `search_results.csv`.

## 13. إيقاف المشروع
اضغط `Ctrl + C` داخل نافذة CMD التي تعمل فيها Streamlit، ثم أكد الإيقاف إذا طُلب منك ذلك.

## 14. إعادة التشغيل لاحقًا
```cmd
cd /d "D:\project\SemanticAlignmentof MedicalClassifications"
.venv\Scripts\activate
streamlit run icd_app.py
```