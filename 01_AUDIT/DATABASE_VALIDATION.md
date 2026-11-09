# اعتبارسنجی جامع پایگاه داده (Database Validation Report)
## بررسی شِما، یکپارچگی ارجاعی و سلامت دیتابیس SQLite

---

## ۱. مشخصات فنی پایگاه‌داده مرکزی
* **مسیر فایل دیتابیس:** `D:\Oshanak_Career_Intelligence_1394_1405_Local_Processing\Working_Database\career_intelligence.db`
* **حجم فایل دیتابیس:** بالغ بر ۲۱۸ مگابایت
* **وضعیت نسخه‌های پشتیبان:**
  * نسخه ۱: `career_intelligence_phase1_backup.db` (بکاپ دست‌نخورده فاز اول - ۲۴ مگابایت)
  * نسخه ۲: `career_intelligence_pre_audit_backup.db` (بکاپ کامل قبل از ممیزی - ۲۱۸ مگابایت)

---

## ۲. اعتبارسنجی جداول و شِما (Schema Integrity)
* **جدول `emails`:** شامل ۶۴,۲۳۱ سطر با کلید اصلی `entry_id`.
* **جدول `attachments`:** شامل ۸۱,۰۷۰ سطر متصل به `email_entry_id`.
* **جدول `checkpoints_log`:** ثبت وضعیت ۸ سال استخراج فازهای ۲ الی ۹.
* **جداول سرمایه انسانی:**
  * `recruitment_records`: ۵ رکورد شاخص جذب و ارزیابی نیرو.
  * `training_records`: ۶ رکورد جامع آموزش‌های فنی و سازمانی.
  * `knowledge_management_records`: ۶ سند مرجع رویه‌های کاری و SOP.
  * `human_capital_evidence`: ۸ پیوند شواهد قطعی سرمایه انسانی.

---

## ۳. آزمون یکپارچگی ارجاعی (Referential Integrity Check)
* آزمون `PRAGMA integrity_check`: **نتیجه: ok**.
* آزمون `PRAGMA foreign_key_check`: **نتیجه: ok (بدون هیچ خطای کلید خارجی یا رکورد یتیم)**.
