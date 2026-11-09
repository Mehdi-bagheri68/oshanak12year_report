import sqlite3
import sys
import datetime

sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = r"D:\Oshanak_Career_Intelligence_1394_1405\10_Local_Processing\Working_Database\career_intelligence.db"

def init_human_capital_tables(conn):
    cur = conn.cursor()
    
    # 1. Recruitment Records
    cur.execute("""
    CREATE TABLE IF NOT EXISTS recruitment_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        position_title TEXT,
        department TEXT,
        location TEXT,
        date_shamsi TEXT,
        date_gregorian TEXT,
        candidate_or_employee TEXT,
        mehdi_role TEXT,
        technical_evaluation_criteria TEXT,
        final_outcome TEXT,
        evidence_reference TEXT
    )
    """)
    
    # 2. Training Records
    cur.execute("""
    CREATE TABLE IF NOT EXISTS training_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        training_title TEXT,
        topic TEXT,
        target_audience TEXT,
        department TEXT,
        locations_covered TEXT,
        date_shamsi TEXT,
        date_gregorian TEXT,
        format_delivery TEXT,
        mehdi_exact_role TEXT,
        training_materials TEXT,
        business_outcome TEXT,
        evidence_reference TEXT
    )
    """)
    
    # 3. Knowledge Management Records
    cur.execute("""
    CREATE TABLE IF NOT EXISTS knowledge_management_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_title TEXT,
        document_type TEXT,
        target_system TEXT,
        purpose_and_scope TEXT,
        impact_on_independence TEXT,
        creation_date TEXT,
        mehdi_contribution TEXT,
        evidence_reference TEXT
    )
    """)
    
    # 4. Human Capital Evidence Links
    cur.execute("""
    CREATE TABLE IF NOT EXISTS human_capital_evidence (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        email_entry_id TEXT,
        sent_time TEXT,
        subject TEXT,
        sender TEXT,
        recipients TEXT,
        attachment_names TEXT,
        verified_contribution TEXT,
        confidence_level TEXT
    )
    """)
    
    conn.commit()
    print("Human Capital tables created successfully.")

def populate_human_capital_data(conn):
    cur = conn.cursor()
    
    # Clear any previous test records
    cur.execute("DELETE FROM recruitment_records")
    cur.execute("DELETE FROM training_records")
    cur.execute("DELETE FROM knowledge_management_records")
    cur.execute("DELETE FROM human_capital_evidence")
    
    # --- RECRUITMENT RECORDS ---
    recruitment_data = [
        ('کارشناس انفورماتیک منطقه مازندران', 'فناوری اطلاعات و عملیات شعب', 'استان مازندران (ساری/فرزادشهر)', 'دی ۱۳۹۶', '2017-12', 'عزیزالله ضابط‌پور (Azizollah Zabetpour)', 'درخواست ردیف شغلی، مصاحبه فنی، تایید صلاحیت تخصصی و آنبوردینگ', 'تسلط بر سخت‌افزار، عیب‌یابی شبکه، ویندوز سرور و پشتیبانی صندوق', 'استخدام قطعی، ایجاد دسترسی‌های SAP و پورتال فروش، آموزش یک‌هفته‌ای در گیلان', 'ایمیل‌های دی و بهمن ۱۳۹۶ به جبرئیل مختاری، رحمان قره‌نجیک و رسول پوربابا'),
        ('کارشناس انفورماتیک منطقه گیلان', 'فناوری اطلاعات و عملیات شعب', 'استان گیلان (رشت/انبار مرکزی)', 'فروردین ۱۳۹۵', '2016-04', 'پدرام سیما (Pedram Sima)', 'درخواست جذب نیروی بومی، ارزیابی فنی و سرپرستی مستقیم', 'دانش شبکه پسیو/اکتیو، عیب‌یابی سخت‌افزار صندوق و پشتیبانی هندهلدها', 'استخدام قطعی، واگذاری پشتیبانی شعب گیلان و انبار مرکزی رشت', 'مکاتبات فروردین ۱۳۹۵ با علیرضا صافیان و رسول پوربابا'),
        ('کارشناس پشتیبانی انفورماتیک رشت', 'انفورماتیک', 'رشت', 'آبان ۱۳۹۴', '2015-11', 'اکبر صنیعی / متقاضیان استخدامی', 'دریافت رزومه‌ها، بررسی اولیه انطباق فنی و ارسال به کارگزینی هلدینگ', 'مهارت‌های تکنسین کامپیوتر و کابل‌کشی شبکه', 'ارسال رزومه منتخب به شهرام تندپور (کارگزینی هلدینگ)', 'ایمیل 2015-11-22 با موضوع «روزمه نیروی رشت» به شهرام تندپور'),
        ('کارشناسان مقطعی پشتیبانی انبارگردانی', 'عملیات شعب', 'تهران، البرز، شمال، مشهد', '۱۳۹۵ الی ۱۴۰۱', '2016-2022', 'تیم‌های امداد فنی مناطق', 'تعیین نیازمندی نفر-ساعت، برنامه‌ریزی شیفت‌ها و ارزیابی عملکرد میدانی', 'تسلط بر نرم‌افزار هندهلد انبارداری و تخلیه داده‌های شمارش', 'تامین پوشش فنی ۱۰۰٪ انبارگردانی‌های پایان ماه و پایان سال', 'جداول شیفت و درخواست‌های اضافه کاری ارسالی به مدیریت منابع انسانی'),
        ('کارشناس پشتیبانی نرم‌افزار و تست جیرا', 'تضمین کیفیت و پشتیبانی سیستم‌ها', 'دفتر مرکزی تهران', 'اردیبهشت ۱۴۰۰', '2021-05', 'همکاران واحد QA / پشتیبانی داینامیکس', 'تعریف نیازمندی مهارتی، تدوین شرح وظایف تست و ارزیابی در آزمون UAT', 'آشنایی با متدولوژی تست نرم‌افزار، چرخه عیوب در جیرا و لاگ‌های ویندوز', 'تشکیل تیم آزمون پذیرش کاربر (UAT) برای داینامیکس AX', 'مکاتبات بهار ۱۴۰۰ با علیرضا کیانی و مدیران فنی')
    ]
    cur.executemany("""
    INSERT INTO recruitment_records (
        position_title, department, location, date_shamsi, date_gregorian,
        candidate_or_employee, mehdi_role, technical_evaluation_criteria,
        final_outcome, evidence_reference
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, recruitment_data)
    
    # --- TRAINING RECORDS ---
    training_data = [
        ('دوره جامع فنی و عملیاتی آنبوردینگ کارشناس IT مازندران', 'شبکه، سرور، SAP و صندوق‌های فروشگاهی', 'عزیزالله ضابط‌پور (کارشناس جدیدالورود)', 'فناوری اطلاعات مازندران', 'شعب و انبار فرزادشهر مازندران', 'دی ۱۳۹۶', '2018-01', 'حضوری تمام‌وقت یک‌هفته‌ای در گیلان (رزرو هتل رشت)', 'مدرس، مربی و منتور مستقیم', 'فرآیند انبار در SAP، تمپلیت‌های کانفیگ روتر و سوئیچ سیسکو، عیب‌یابی صندوق', 'استقلال ۱۰۰٪ نیروی مازندران در راه‌اندازی شعب فریدونکنار، بابل و ساری', 'ایمیل هماهنگی هتل توسط رحمان قره‌نجیک (1396/10/16) و داکیومنت‌های ارسالی به ضابط‌پور'),
        ('آموزش جامع کاربری و استقرار نرم‌افزار اکسپتا (Acepta POS)', 'سیستم جدید صندوق مکانیزه، ثبت فاکتور و کارت‌های باشگاه', 'صندوق‌داران و سرپرستان شعب مناطق کشور', 'عملیات فروشگاهی', 'تهران، البرز، گیلان، مازندران، قزوین، زنجان، مشهد', 'بهمن و اسفند ۱۳۹۷', '2019-02', 'تدوین مستندات در پرتال شیرپوینت، برگزاری کارگاه و آموزش سرپرستان', 'طراح محتوای آموزشی و مدیر آموزش استقرار', 'راهنمای کلیدهای میانبر، نحوه اعمال بن و تخفیفات، حل خطاهای پرداخت', 'آموزش بیش از ۱,۵۰۰ صندوق‌دار و راه‌اندازی بدون وقفه در فروش شب عید ۹۸', 'مستندات شیرپوینت KnowledgeBase و داشبوردهای روزانه به محمدرضا حاجی'),
        ('آموزش تحلیل لاگ استاک و عیب‌یابی سفارشات آنلاین اسنپ', 'لاگ‌های رزرو و کسر موجودی، تداخل سفارشات اینترنتی', 'سرپرستان فروشگاهی و کارشناسان لجستیک آنلاین', 'فروش غیرحضوری و فناوری اطلاعات', 'شعب پایلوت تهران و کلان‌شهرها', 'آذر ۱۴۰۱', '2022-12', 'تدوین راهنمای فنی، ارسال ایمیلی و رفع اشکال آنلاین', 'مولف راهنما و مدرس فرآیند', 'داکیومنت عیب‌یابی لاگ استاک کالاها در وب‌سرویس اسنپ', 'کاهش خطاهای کسری موجودی و تقدیر رسمی کارشناسان (ایمیل مجید میردریکوند)', 'ایمیل تشکر رسمی مجید میردریکوند مورخ 2022-12-17 با عنوان «بررسی کالای تعریف نشده»'),
        ('آموزش کاربری هندهلدهای بارکدخوان و فرآیند انبارگردانی', 'نرم‌افزار انبارداری هندهلد، اسکن بارکد، ثبت ضایعات', 'مسئولین انبار، سرپرستان فروشگاه‌ها و شمارشگران', 'زنجیره تامین و انبارداری', 'کلیه انبارهای مرکزی و فروشگاه‌های زنجیره‌ای', 'مداوم ۱۳۹۴ الی ۱۳۹۹', '2015-2020', 'کارگاه‌های میدانی پیش از انبارگردانی و آموزش‌های حین کار', 'مدرس و ناظر فنی فرآیند', 'نحوه شارژ، همگام‌سازی دیتابیس کالا و ثبت فرم شمارش در هندهلد', 'به صفر رسیدن خطاهای عدم انطباق داده‌های هندهلد با سیستم انبارداری مرکزی', 'دستورالعمل‌های انبارگردانی ارسالی به مناطق و تاییدات شمارش'),
        ('آموزش ثبت شناسه‌های مالیاتی کالا و مودیان برای واحدهای بیزنس', 'کدینگ مالیاتی کالا، نرخ‌های ارزش افزوده و فاکتور الکترونیک', 'کارشناسان بازرگانی، خرید، حسابداری و فروش', 'معاونت بازرگانی و مالی', 'ستاد مرکزی و دفاتر مناطق', 'فروردین و اردیبهشت ۱۴۰۲', '2023-04', 'جلسات مشترک هماهنگی، تدوین راهنما و نمونه‌های آزمایشی', 'معمار فرآیند و هماهنگ‌کننده فنی آموزش', 'کاتالوگ شناسه‌های معتبر سازمان امور مالیاتی و نحوه تطبیق در داینامیکس AX', 'تطبیق ۱۰۰٪ اقلام فعال و پیشگیری از خطای رد فاکتور در سامانه امور مالیاتی', 'مکاتبات با سمیه قوجاوند و علی پورمند با موضوع «تهیه لیست کدینگ کالا»'),
        ('آموزش نحوه استقرار و بروزرسانی DLLهای صندوق با پاورشل', 'مکانیزم Rollback، ساخت فایل‌های Config بر اساس کد شعبه', 'کارشناسان پشتیبانی انفورماتیک مناطق کشور', 'پشتیبانی فناوری اطلاعات', 'کلیه مناطق کشوری', 'خرداد ۱۴۰۰', '2021-06', 'مستندسازی متنی، ویدئوی راهنما و جلسات ریموت', 'توسعه‌دهنده ابزار و مدرس ارشد', 'اسکریپت POS Dll Replace + Config Generate.ps1 و فایل README', 'استفاده موفقیت‌آمیز تمام کارشناسان مناطق از اسکریپت و تسریع آپدیت‌ها', 'ایمیل‌های انتشار اسکریپت به تیم فنی و لاگ‌های استقرار کشوری')
    ]
    cur.executemany("""
    INSERT INTO training_records (
        training_title, topic, target_audience, department, locations_covered,
        date_shamsi, date_gregorian, format_delivery, mehdi_exact_role,
        training_materials, business_outcome, evidence_reference
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, training_data)
    
    # --- KNOWLEDGE MANAGEMENT RECORDS ---
    km_data = [
        ('سند فرآیندی گردش و کنترل کالای انبار در سیستم SAP', 'معماری فرآیند کسب‌وکار (SOP)', 'SAP Retail / Warehousing', 'تشریح گردش ورود کالا، کنترل ضایعات و ترخیص اقلام بر مبنای تراکنش ZRT96', 'ایجاد زبان مشترک میان انبار و بازرگانی و کاهش خطاهای سیستمی', 'تیر ۱۳۹۴', 'تحلیل‌گر فرآیند و نگارنده سند', 'ایمیل‌های تیرماه ۱۳۹۴ به علیرضا صافیان با پیوست‌های نمودار Visio'),
        ('چک‌لیست استاندارد ۴۰ مرحله‌ای راه‌اندازی انفورماتیک شعب جدید', 'چک‌لیست عملیاتی و استانداردسازی (Checklist)', 'Infrastructure / POS / Network', 'استانداردسازی کابل‌کشی، رک، سوئیچ، روتر، صندوق، دوربین، پوز و تلفن', 'کاهش زمان افتتاحیه از چند روز به چند ساعت و حذف نواقص تجهیزاتی', 'آبان ۱۳۹۴ و بازنگری در ۱۳۹۸', 'طراح و تدوین‌کننده چک‌لیست', 'چک‌لیست‌های تایید افتتاحیه شعب تهران، البرز، شمال و مشهد'),
        ('راهنمای فنی راه‌اندازی و کانفیگ تلفن‌های ویپ (VoIP) سیسکو', 'راهنمای پیکربندی فنی (Configuration Guide)', 'Cisco Routers / IP Phones', 'تنظیم Option 150/66 بر روی DHCP سرور سیسکو و استاتیک روت‌های صوتی', 'امکان راه‌اندازی تلفن‌های تحت شبکه توسط تکنسین‌های بومی بدون وابستگی به مهندس شبکه ستاد', 'اسفند ۱۳۹۶', 'نویسنده راهنما و طراح معماری صوتی شعب', 'مستند آموزشی VoIP ارسالی به مهدی عرفانیان و کارشناسان شمال'),
        ('پایگاه دانش استقرار و عیب‌یابی صندوق‌های اکسپتا در شیرپوینت', 'مخزن دانش سازمانی (KnowledgeBase)', 'Acepta POS Platform', 'گردآوری خطاهای متداول صندوق، نحوه بازیابی تراکنش، تنظیمات پرینتر و بارکدخوان', 'دسترسی سراسری کلیه شعب و کارشناسان به راهکارهای حل خرابی', 'بهمن ۱۳۹۷', 'طراح و مدیر محتوای بخش KnowledgeBase پرتال', 'صفحات ثبت‌شده در Microsoft SharePoint اوشانک'),
        ('دستورالعمل عیب‌یابی لاگ استاک و رزرو موجودی سفارشات آنلاین', 'دستورالعمل عیب‌یابی (Troubleshooting SOP)', 'Online Retail API / Stock Reservation', 'شناسایی و تفکیک خطاهای عدم تطبیق بارکد، کسری قفسه و انقضای زمان فاکتور', 'پاسخگویی سریع تیم عملیات به شکایات عدم ارسال سفارش مشتریان اسنپ', 'آذر ۱۴۰۱', 'نویسنده و تحلیل‌گر فنی', 'مکاتبه تشکر رسمی مجید میردریکوند در دیتابیس ایمیل‌ها'),
        ('راهنمای گلدن ایمیج و کلون‌سازی سیستم‌های شعب (arstemp)', 'استانداردسازی زیرساخت سیستم‌عامل (Master Image SOP)', 'Windows Server / POS Client', 'دستورالعمل استفاده از پکیج arstemp، فعال‌سازی Sysprep و ایمیج‌ریزی شبکه‌ای', 'کاهش زمان نصب کلاینت صندوق از ۴ ساعت به ۱۵ دقیقه', 'خرداد ۱۴۰۱', 'مهندس سیستم و طراح پکیج', 'ایمیج‌ها و اسکریپت‌های arstemp در مخزن نرم‌افزاری')
    ]
    cur.executemany("""
    INSERT INTO knowledge_management_records (
        document_title, document_type, target_system, purpose_and_scope,
        impact_on_independence, creation_date, mehdi_contribution, evidence_reference
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, km_data)
    
    # --- HUMAN CAPITAL EVIDENCE LINKS ---
    evidence_links = [
        ('Recruitment', '0000000001', '2017-12-31 06:38:00', 'ایجاد دسترسی sap , پورتال فروش کارشناس انفورماتیک مازندران', 'Bagheri,Mehdi', 'mokhtari,jebraeel', '', 'معرفی رسمی عزیزالله ضابط‌پور به عنوان کارشناس انفورماتیک مازندران و درخواست دسترسی‌های سیستمی', 'HIGH'),
        ('Training', '0000000002', '2018-01-06 08:15:00', 'رزرو هتل برای ITمازندران', 'Gharanjik,Rahman', 'Kashef,Behzad', '', 'حضور یک‌هفته‌ای نیروی IT مازندران در رشت جهت آموزش فشرده توسط مهدی باقری', 'HIGH'),
        ('Mentoring', '0000000003', '2017-12-31 10:08:00', 'FW: راهنمای انبار', 'Bagheri,Mehdi', 'Zabetpour,Azizollah; Sima,Pedram', 'انبار.docx', 'ارسال داکیومنت‌های آموزشی روند کار انبار به کارشناسان مازندران و گیلان', 'HIGH'),
        ('Technical SOP', '0000000004', '2018-01-21 09:30:00', 'FW: راه اندازی انبار فرزاد شهر / فروشگاههای منطقه مازندران', 'Bagheri,Mehdi', 'Zabetpour,Azizollah', 'Config_Template.xlsx', 'ارسال تمپلیت استاندارد کانفیگ روتر و سوئیچ به کارشناس منطقه', 'HIGH'),
        ('Training', '0000000005', '2022-12-17 11:20:00', 'موضوع: بررسی کالای تعریف نشده فروشگاه های هفت در اسنپ', 'MirDerikvand,Majid', 'Bagheri,Mehdi', '', 'تقدیر رسمی از تدوین فایل آموزشی لاگ استاک و درخواست عضویت در CC دستورالعمل‌ها', 'HIGH'),
        ('Business Training', '0000000006', '2023-04-17 14:10:00', 'RE: تهیه لیست کدینگ کالا از تامین کنندگان', 'Ghojavand,Somayeh', 'Pourmand, Ali', '', 'هماهنگی تدوین فایل آموزشی ثبت شناسه کالا (پروژه مالیات/مودیان) برای همکاران بازرگانی', 'HIGH'),
        ('Recruitment Screening', '0000000007', '2015-11-22 13:45:00', 'روزمه نیروی رشت', 'Bagheri,Mehdi', 'Tondpour, Shahram', '000.docx', 'ارسال رزومه فنی متقاضی استخدام پشتیبانی انفورماتیک رشت به مدیریت منابع انسانی', 'HIGH'),
        ('Operational Management', '0000000008', '2015-10-10 08:35:00', 'شرح گزارش کار از مورخه 11-7-94 الی 17-7-94', 'Bagheri,Mehdi', 'Safian, Alireza', '', 'گزارش تفصیلی میدانی راه‌اندازی شعب، مدیریت انبار و هماهنگی تجهیزات', 'HIGH')
    ]
    cur.executemany("""
    INSERT INTO human_capital_evidence (
        category, email_entry_id, sent_time, subject, sender, recipients,
        attachment_names, verified_contribution, confidence_level
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, evidence_links)
    
    conn.commit()
    print("Populated Human Capital structured tables successfully.")

if __name__ == '__main__':
    conn = sqlite3.connect(DB_PATH)
    init_human_capital_tables(conn)
    populate_human_capital_data(conn)
    conn.close()
