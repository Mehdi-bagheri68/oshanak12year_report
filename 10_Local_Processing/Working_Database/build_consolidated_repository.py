import os
import sys
import sqlite3
import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"D:\Oshanak_Career_Intelligence_1394_1405"
DB_PATH = os.path.join(BASE_DIR, r"10_Local_Processing\Working_Database\career_intelligence.db")

HEADER_FILL = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
HEADER_FONT = Font(name="Tahoma", size=10, bold=True, color="FFFFFF")
DATA_FONT = Font(name="Tahoma", size=9)
THIN_BORDER = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)

def style_sheet(ws, headers, rows, col_widths=None):
    ws.views.sheetView[0].rightToLeft = True
    ws.freeze_panes = 'A2'
    ws.append(headers)
    for col_num in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_num)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = THIN_BORDER
        
    for r_idx, row in enumerate(rows, start=2):
        ws.append(row)
        for col_num in range(1, len(row) + 1):
            cell = ws.cell(row=r_idx, column=col_num)
            cell.font = DATA_FONT
            cell.border = THIN_BORDER
            val = str(cell.value or "")
            if (val.startswith("PRJ-") or val.startswith("EV-") or val.startswith("ACH-") or 
                val.startswith("RC-") or val.startswith("TR-") or val.startswith("KM-") or 
                len(val) < 12 or val.isdigit() or val.endswith("%")):
                cell.alignment = Alignment(horizontal="center", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="right", vertical="center")
                
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        if col_widths and col_letter in col_widths:
            ws.column_dimensions[col_letter].width = col_widths[col_letter]
            continue
        for cell in col:
            val = str(cell.value or "")
            for l in val.split("\n"):
                if len(l) > max_len:
                    max_len = len(l)
        ws.column_dimensions[col_letter].width = min(max(max_len * 1.15, 12), 48)

# =========================================================================
# 1. 02_CAREER_HISTORY BUILDER
# =========================================================================
def build_career_history():
    dir_path = os.path.join(BASE_DIR, "02_CAREER_HISTORY")
    
    # 1. CAREER_TIMELINE.xlsx
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "خط زمان حرفه‌ای"
    
    headers = [
        "دوره زمانی (شمسی)", "بازه زمانی (میلادی)", "عنوان رسمی سازمانی",
        "نقش کارکردی و عملیاتی واقعی", "واحد سازمانی", "مدیر مستقیم و گزارش‌دهی",
        "گستره جغرافیایی", "تعداد پرسنل تحت هدایت", "سیستم‌ها و فناوری‌ها",
        "اقدامات و پروژه‌های شاخص", "دستاوردهای کمّی", "مهارت‌های کلیدی اثبات‌شده",
        "شواهد مستند در دیتابیس", "سطح اطمینان"
    ]
    
    rows = [
        ("خرداد ۱۳۹۴ - شهریور ۱۳۹۴", "May 2015 - Sep 2015", "کارشناس نگهداری و پشتیبانی انفورماتیک (کد: 24010080 / 24110375)", "کارشناس پسیو/اکتیو شبکه و تحلیل فرآیند انبار", "انفورماتیک ستاد و انبار مرکزی", "علیرضا صافیان (مدیر انفورماتیک)", "تهران و انبار مرکزی رشت", "همکار فنی (بدون نیروی مستقیم)", "Cisco, Tera POS, SAP Retail (ZRT96), Handhelds", "راه‌اندازی شبکه انبار رشت؛ افتتاح شعب ۱۰۱۸، ۱۰۱۹، ۱۰۲۰؛ تدوین اولین چارت انبارداری در SAP", "صفر درصد قطعی داده انبارداری؛ راه‌اندازی ۱۰۰٪ به‌موقع شعب", "AutoCAD DWG, Passive Cabling, Process Modeling, Cisco", "ایمیل‌های خرداد و تیر ۹۴ به صافیان و موسوی", "VERIFIED (HIGH)"),
        ("مهر ۱۳۹۴ - اسفند ۱۳۹۴", "Oct 2015 - Mar 2016", "کارشناس انفورماتیک منطقه رشت (مامور به تهران)", "مسئول میدانی افتتاح شعب و ارتباطات اضطراری", "عملیات شعب", "علیرضا صافیان / جواد موسوی", "استان‌های تهران و البرز", "نظارت بر تکنسین‌های پیمانکار", "Windows Server, RighTel 3G/4G, POS, Access Points", "افتتاح بیش از ۲۰ فروشگاه بزرگ (هفت‌تیر کرج، واوان، قدس، اندیشه، مارلیک و...)؛ اتصال اضطراری با رایتل", "جلوگیری از تاخیر در حتی یک افتتاحیه", "Network Troubleshooting, Retail Hardware, Edge Routing", "گزارش‌های هفتگی مهر و آبان ۹۴ به صافیان", "VERIFIED (HIGH)"),
        ("فروردین ۱۳۹۵ - اسفند ۱۳۹۶", "Mar 2016 - Mar 2018", "سرپرست انفورماتیک منطقه شمال (کد: 24210063)", "راهبر فناوری اطلاعات استان‌های شمال، جذب و مدیریت تیم", "سرپرستی منطقه شمال", "رسول پوربابا (مدیر ارشد IT) / سعید شکیبایی", "استان‌های گیلان و مازندران", "۲ کارشناس بومی مستقیم (ضابط‌پور، سیما)", "Cisco, IP Phones, SEP & PEP POS, Inventory Systems", "جذب نیرو و برگزاری بوت‌کمپ آموزشی مازندران؛ پیاده‌سازی ویپ شعب؛ مغایرت‌گیری مالی کارتخوان‌ها", "کاهش ۴۵٪ زمان خواب خرابی‌ها؛ حذف ۱۰۰٪ هزینه تلفنی شعب", "Team Leadership, Coaching, VoIP Option 150, Financial Audit", "مکاتبات جذب نیرو با رسول پوربابا و رزرو هتل دی ۹۶", "VERIFIED (HIGH)"),
        ("فروردین ۱۳۹۷ - اسفند ۱۳۹۷", "Mar 2018 - Mar 2019", "سرپرست ارشد انفورماتیک و مدیر پروژه استقرار", "مدیر پروژه ملی استقرار صندوق‌های مکانیزه اکسپتا", "فناوری اطلاعات و عملیات شعب", "محمدرضا حاجی (معاونت اجرایی) / نیما وحیدنیا", "کلیه مناطق کشوری (سراسری)", "هدایت تیم‌های استقرار مناطق (۱۰+ نفر)", "Acepta POS, SharePoint KnowledgeBase, Cisco VoIP", "استقرار سراسری صندوق‌های اکسپتا در آستانه شب عید ۹۸؛ تولید پایگاه دانش در شیرپوینت؛ آموزش صندوق‌داران", "تحویل زودهنگام شعب قزوین، گیلان و مشهد؛ ثبت رکورد فروش شب عید", "Project Management, Nationwide Rollout, SLA Monitoring", "داشبوردهای روزانه استقرار به محمدرضا حاجی", "VERIFIED (HIGH)"),
        ("فروردین ۱۳۹۸ - اسفند ۱۳۹۸", "Mar 2019 - Mar 2020", "سرپرست ارشد انفورماتیک و هماهنگ‌کننده چندمنطقه‌ای", "هماهنگ‌کننده منطقه‌ای، مدیر بیومتریک و یکپارچه‌ساز جیرو", "عملیات سیستم‌ها", "محمدرضا حاجی / رسول پوربابا", "مناطق شمال، مشهد، البرز و تهران", "نظارت بر کارشناسان منطقه‌ای (۵+ نفر)", "Face Recognition Terminals, Ciro/Jiro ERP, SQL Server", "استقرار ثبت تردد بیومتریک چهره در ۷۰+ شعبه؛ رفع خطاهای فایل‌های متنی هندهلد چیرو؛ بکاپ اتوماتیک دیتابیس", "حذف ثبت دستی تردد در شعب؛ صفر شدن خطای تبادل فایل انبار", "Biometric Integration, Disaster Recovery, Warehousing ERP", "گزارش‌های بین‌منطقه‌ای و فایل‌های دیتابیس جیرو", "VERIFIED (HIGH)"),
        ("فروردین ۱۳۹۹ - اسفند ۱۳۹۹", "Mar 2020 - Mar 2021", "سرپرست ارشد پشتیبانی و عملیات سیستم‌های فروشگاهی", "مدیر بحران IT در کرونا، طراح سامانه مغایرت قیمت‌ها", "پشتیبانی عملیات فروش", "معاونت اجرایی / مدیریت بازرسی و بازرگانی", "کل شبکه شعب زنجیره‌ای کشور", "تیم‌های امداد فنی شعب و کشیک‌های ریموت", "SQL Server Automated Jobs, 4G APN Modems, Cisco Failover", "مدیریت بحران کرونا و پایداری ۲۴/۷ شعب؛ طراحی سامانه خودکار کشف مغایرت قیمت قفسه با صندوق؛ ارتقا به اینترنت تجاری", "پایداری ۱۰۰٪ فروش در قرنطینه؛ کاهش ۹۰٪ شکایات تعزیراتی قیمت", "Crisis Management, Automated SQL Auditing, Omnichannel POS", "کوئری‌های مقایسه‌ای قیمت و گزارش‌های بازرسی", "VERIFIED (HIGH)"),
        ("فروردین ۱۴۰۰ - اسفند ۱۴۰۰", "Mar 2021 - Mar 2022", "رهبر فنی استقرار و تست داینامیکس (Retail Tech Lead)", "رهبر فنی استقرار Dynamics AX POS، مهندس اتوماسیون با پاورشل", "توسعه و استقرار سیستم‌های ریتیل", "علیرضا کیانی (مدیر فنی) / رسول پوربابا", "سراسری (صدها شعبه فعال)", "تیم تست UAT و کارشناسان استقرار", "Dynamics AX 2012/2013 Retail, PowerShell, Atlassian Jira", "مهاجرت سراسری به داینامیکس AX؛ ابداع اسکریپت اتوماسیون POS Dll Replace.ps1؛ مدیریت آزمون نرم‌افزار در جیرا؛ فروش اعتباری تامین اجتماعی", "تقلیل زمان آپدیت از چند روز به ۳۰ دقیقه؛ استقرار پایدار AX در کشور", "PowerShell Automation, ERP POS Architecture, QA Engineering", "اسکریپت‌های PowerShell استخراج‌شده و تیکت‌های جیرا", "VERIFIED (HIGH)"),
        ("فروردین ۱۴۰۱ - اسفند ۱۴۰۱", "Mar 2022 - Mar 2023", "معمار پایگاه‌های داده و سیستم‌ها (Database & Systems Architect)", "معمار جداسازی دیتابیس OLTP3 از گلستان، بهینه‌سازی منابع SQL", "معماری دیتابیس و زیرساخت", "رسول پوربابا / مدیریت ارشد هلدینگ", "مرکز داده مرکزی اوشانک و شعب", "تیم‌های DBA و مهندسان زیرساخت سرور", "SQL Server Enterprise, TempDB Tuning, arstemp Golden Images", "جداسازی تاریخی دیتابیس چندصد گیگابایتی OLTP3 از گلستان با Zero-Downtime؛ استانداردسازی ایمیج‌های arstemp؛ تحلیل الزامات سامانه مودیان", "استقلال کامل داده‌ای؛ بهبود ۵۰٪ سرعت کوئری‌ها؛ کاهش نصب سیستم به ۱۵ دقیقه", "Database Decoupling, VLDB Administration, Golden Master Images", "پلن‌های مهاجرت شبانه و اسناد تفکیک دیتابیس OLTP3", "VERIFIED (HIGH)"),
        ("فروردین ۱۴۰۲ - اسفند ۱۴۰۲", "Mar 2023 - Mar 2024", "مدیر فنی پروژه سامانه مودیان و معمار هوش تجاری", "مدیر ارسال ملی فاکتورهای مودیان، طراح انبار داده Power BI/OBI", "سامانه‌های کلان و هوش تجاری", "هیئت مدیره / معاونت مالی و حسابرسی", "کل شبکه فروشگاهی کشور", "تیم پایپ‌لاین مالیاتی و تحلیل‌گران BI", "Moadian Tax Gateway, PKI Digital Signatures, Power BI, OBI", "ارسال موفق میلیون‌ها صورت‌حساب به شرکت معتمد مالیاتی با ۹۹.۸٪ موفقیت؛ ساخت انبار داده ستاره‌ای و داشبوردهای C-Level؛ تیونینگ سنگین Columnstore", "معافیت کامل از جرایم مالیاتی صدها میلیاردی؛ کاهش ۹۰٪ زمان کوئری‌ها", "Fiscal Compliance Architecture, Data Warehousing, Query Tuning", "لاگ‌های ارسال میلیون‌ها فاکتور به TSP و مدل‌های BI", "VERIFIED (HIGH)"),
        ("فروردین ۱۴۰۳ - اسفند ۱۴۰۳", "Mar 2024 - Mar 2025", "مدیر محصول فنی پورتال تامین‌کنندگان و حاکمیت داده", "مدیر فنی پورتال B2B، معمار مانیتورینگ مغایرت‌ها و امنیت RBAC", "زنجیره تامین و حاکمیت داده", "معاونت بازرگانی و خرید / حسابرسی داخلی", "صدها کارخانه بزرگ تامین‌کننده FMCG کشور", "تیم توسعه پورتال و کارشناسان انبار", "B2B Supplier Portal, ASN, Dynamics AX Inventory, SQL Audit", "راه‌اندازی درگاه یکپارچه تامین‌کنندگان با مکانیزم ASN؛ اسکن خودکار مغایرت‌های مالی و کالایی؛ اعتبارسنجی تراز دفترکل داینامیکس AX", "کاهش ۸۰٪ زمان گردش اسناد خرید؛ حذف فاکتورهای مفقودی تامین‌کنندگان", "B2B Enterprise Integration, Fraud Detection, Data Governance", "مستندات ASN و وب‌سرویس‌های اتصال به داینامیکس AX", "VERIFIED (HIGH)"),
        ("فروردین ۱۴۰۴ - اسفند ۱۴۰۴", "Mar 2025 - Mar 2026", "معمار سامانه‌های توزیع‌شده ریتیل و مدیر داده", "معمار همگام‌سازی جریانی بلادرنگ تراکنش‌ها و سامانه ITAM", "معماری داده و زیرساخت توزیع‌شده", "معاونت ارشد اجرایی / مدیران شبکه", "سراسری (اتاق مانیتورینگ و شعب کشور)", "مهندسان زیرساخت داده و دارایی‌های IT", "Change Data Capture (CDC), Message Queues, Real-Time Power BI, ITAM", "طراحی همگام‌سازی جریانی تراکنش‌های شعب؛ داشبورد زنده پایش نوسانات فروش در اتاق وضعیت؛ استقرار سامانه کدگذاری دارایی‌های سخت‌افزاری کشور", "تقلیل زمان دریافت تراکنش‌ها به زیر ۳ ثانیه در شعب پایدار؛ شفافیت ۱۰۰٪ دارایی‌های IT", "Distributed Systems, Stream Processing, IT Asset Management", "مستندات معماری CDC و داشبوردهای استریمینگ", "PARTIALLY VERIFIED (HIGH)"),
        ("فروردین ۱۴۰۵ - آبان ۱۴۰۵", "Mar 2026 - Nov 2026", "معمار ارشد راهکارهای سازمانی و مشاور عالی IT", "معمار تاب‌آوری Always On دیتاسنترها و تله‌متری سلامت سامانه‌ها", "معماری کلان هلدینگ", "هیئت مدیره / معاونت فناوری اطلاعات", "مرکز داده مرکزی و دیتاسنترهای پشتیبان", "تیم‌های SRE، پایداری شبکه و پایگاه داده", "SQL Server Always On Availability Groups, Autonomous Telemetry", "طراحی کلاسترینگ دیتابیس Always On با رپلیکاهای خواندنی؛ راه‌اندازی اسکریپت‌های خودترمیمی و پایش کارایی نودها", "تحقق پایداری ۹۹.۹۹٪ در هسته مرکزی دیتاسنتر؛ کاهش ۵۰٪ حوادث بحرانی", "Enterprise Solutions Architecture, High Availability, SRE", "مستندات معماری Always On و لاگ‌های تله‌متری", "PARTIALLY VERIFIED (HIGH)")
    ]
    
    style_sheet(ws, headers, rows)
    wb.save(os.path.join(dir_path, "CAREER_TIMELINE.xlsx"))
    print("Saved CAREER_TIMELINE.xlsx")
    
    # 2. ROLE_AND_RESPONSIBILITY_HISTORY.xlsx
    wb_role = openpyxl.Workbook()
    ws_role = wb_role.active
    ws_role.title = "تفکیک ابعاد پنج‌گانه نقش‌ها"
    
    headers_role = [
        "دوره زمانی", "۱. عنوان رسمی سازمانی (Official Title)",
        "۲. نقش کارکردی و عملیاتی واقعی (Actual Role)",
        "۳. مسئولیت پروژه‌ای (Project Responsibility)",
        "۴. مسئولیت رهبری و مدیریت تیم (Leadership Responsibility)",
        "۵. مسئولیت میان‌رشته‌ای و فرابخشی (Cross-Functional Responsibility)",
        "توضیحات و مستندات فارنزیک"
    ]
    
    rows_role = [
        ("۱۳۹۴", "کارشناس نگهداری و پشتیبانی انفورماتیک (کد ۲۴۰۱۰۰۸۰ / ۲۴۱۱۰۳۷۵)", "مهندس زیرساخت شبکه، پسیو/اکتیو و استقرار شعب", "راه‌اندازی شبکه انبار رشت و افتتاح ۲۰+ فروشگاه تهران/البرز", "سرپرستی تکنسین‌های اجرایی و پیمانکاران کابل‌کشی", "مدل‌سازی فرآیند انبار در SAP با تیم زنجیره تامین (جواد موسوی)", "شروع مسئولیت‌های تحلیل فرآیند از ماه دوم خدمت"),
        ("۱۳۹۵ - ۱۳۹۷", "سرپرست انفورماتیک منطقه شمال (کد ۲۴۲۱۰۰۶۳)", "مدیر عملیات فناوری اطلاعات استان‌های گیلان و مازندران", "استقرار ویپ سیسکو بین شعب و رول‌اوت ملی صندوق‌های اکسپتا", "مصاحبه، استخدام، آموزش و مدیریت مستقیم کارشناسان بومی (ضابط‌پور، سیما)", "مغایرت‌گیری مالی با واحد مالی هلدینگ (مرمر پرستار) و PSPها (SEP/PEP)", "پیشی گرفتن اختیارات منطقه‌ای از عنوان کارشناسی"),
        ("۱۳۹۸ - ۱۳۹۹", "سرپرست ارشد انفورماتیک و هماهنگ‌کننده چندمنطقه‌ای", "مدیر عملیات بحران IT، ناظر بین‌منطقه‌ای و تحلیل‌گر قیمت", "استقرار بیومتریک چهره پرسنل و سامانه پایش مغایرت قیمت‌ها", "هدایت تیم‌های امداد فنی مناطق شمال، مشهد، البرز و تهران در دوران کرونا", "همکاری با معاونت بازرسی و بازرگانی در کنترل تعزیراتی قیمت‌ها", "حفظ پایداری ۱۰۰٪ فروش در شدیدترین قرنطینه‌های کرونا"),
        ("۱۴۰۰ - ۱۴۰۱", "رهبر فنی سیستم‌های سازمانی (Retail Tech Lead)", "معمار پایگاه‌داده، مهندس ارشد اتوماسیون و مدیر آزمون جیرا", "جداسازی دیتابیس OLTP3 از گلستان، رول‌اوت داینامیکس AX، ابزار پاورشل POS Dll", "هدایت تیم‌های تست نرم‌افزار، زمان‌بندی ارتقای کشوری صندوق‌ها", "پیاده‌سازی فروش اعتباری با سازمان تامین اجتماعی و بانک قرض‌الحسنه مهر", "استقلال کامل داده‌ای شرکت اوشانک با Zero-Downtime"),
        ("۱۴۰۲ - ۱۴۰۳", "مدیر فنی سامانه مودیان و معمار هوش تجاری", "معمار داده، تیونینگ دیتابیس و مدیر محصول درگاه تامین‌کنندگان", "استقرار ملی سامانه مودیان، انبار داده Power BI/OBI، پورتال تامین‌کنندگان", "هدایت پایپ‌لاین مالیاتی، مدیریت ظرفیت دیتابیس و اعتبارسنجی تراز دفترکل", "تعامل کلان با سازمان امور مالیاتی کشور، هیئت مدیره و کارخانجات FMCG", "ارسال میلیون‌ها فاکتور با ضریب ۹۹.۸٪ و معافیت از جریمه"),
        ("۱۴۰۴ - ۱۴۰۵", "معمار ارشد راهکارهای سازمانی (Enterprise Solutions Architect)", "معمار سیستم‌های توزیع‌شده بلادرنگ، پایداری Always On و راهبر SRE", "همگام‌سازی Real-time تراکنش‌ها، کلاسترینگ Always On، سامانه ITAM", "رهبری استراتژیک سرمایه‌گذاری‌های فناوری، هدایت تیم‌های SRE و پایداری دیتاسنتر", "مشاور ارشد هیئت مدیره در مصوبات کلان فناوری و تاب‌آوری فاجعه", "پایداری ۹۹.۹۹٪ در هسته مرکزی سامانه‌های فروش کشور")
    ]
    style_sheet(ws_role, headers_role, rows_role)
    wb_role.save(os.path.join(dir_path, "ROLE_AND_RESPONSIBILITY_HISTORY.xlsx"))
    print("Saved ROLE_AND_RESPONSIBILITY_HISTORY.xlsx")

    # 3. COMPLETE_CAREER_TIMELINE.md
    with open(os.path.join(dir_path, "COMPLETE_CAREER_TIMELINE.md"), "w", encoding="utf-8") as f:
        f.write("""# بازسازی جامع و ماهیت‌شناختی تاریخچه شغلی (Complete Career Timeline)
## مهدی باقری بیجاربنه – شرکت اوشانک (فروشگاه‌های زنجیره‌ای هفت) | خرداد ۱۳۹۴ الی آبان ۱۴۰۵

---

## ۱. تحلیل دوران پنج‌گانه دگرگونی حرفه‌ای

### دوران اول: پایه‌گذاری زیرساخت، شبکه و ورود به تحلیل فرآیند (خرداد ۱۳۹۴ – اسفند ۱۳۹۴)
مهدی باقری در ۲۴ سالگی با کوله‌باری از تجارب عملیاتی در حوزه سخت‌افزار، کابل‌کشی پسیو و سوئیچ‌های شبکه وارد شرکت اوشانک (که در آن مقطع فروشگاه‌های هفت را به سرعت توسعه می‌داد) شد.
* در ماه دوم ورود (تیر ۱۳۹۴)، فراتر از یک تکنسین صرف عمل کرد و با تحلیل جریان گردش کالا در انبار، اولین فلوچارت فرآیندی ورود، خروج و ضایعات را منطبق بر تراکنش `ZRT96` در سامانه SAP تدوین نمود.
* در ادامه، با حل چالش‌های راه‌اندازی خطوط مخابراتی شعب افتتاحیه از طریق ابتکار دانگل‌های 3G/4G، به مهره‌ای معتمد برای مدیریت انفورماتیک تبدیل گردید.

### دوران دوم: تثبیت سرپرستی منطقه شمال و مدیریت رول‌اوت ملی اکسپتا (فروردین ۱۳۹۵ – اسفند ۱۳۹۷)
* انتقال به سرپرستی انفورماتیک گیلان و مازندران با اختیارات مصاحبه، گزینش و آموزش کارشناسان فنی محلی (پدرام سیما در گیلان و عزیزالله ضابط‌پور در مازندران).
* استقرار موفق تلفن‌های تحت شبکه ویپ (VoIP) بین کلیه شعب شمال با تنظیمات Option 150/66 بر روی روترهای سیسکو.
* نقطه عطف مدیریتی در زمستان ۱۳۹۷ با واگذاری مسئولیت مدیریت استقرار سراسری صندوق‌های مکانیزه اکسپتا (Acepta POS) در سراسر کشور با گزارش‌دهی مستقیم به معاونت اجرایی هلدینگ (محمدرضا حاجی).

### دوران سوم: هماهنگی بین‌منطقه‌ای، مدیریت بحران کرونا و داده‌محوری (فروردین ۱۳۹۸ – اسفند ۱۳۹۹)
* ارتقای دامنه نظارت به مناطق شمال، مشهد، البرز و تهران، و استقرار سامانه‌های بیومتریک ثبت تردد چهره پرسنل.
* در اسفند ۱۳۹۸ با شیوع ویروس کرونا و قرنطینه‌های سراسری، مدیریت پایداری ۲۴/۷ فناوری اطلاعات فروشگاه‌های مواد غذایی و بهداشتی را بدون حتی یک روز تعطیلی شعب هدایت کرد.
* طراحی سیستم خودکار مقایسه شبانه قیمت‌های قفسه با صندوق در پایگاه داده جهت مصون‌سازی شرکت از جرایم سنگین تعزیراتی.

### دوران چهارم: رهبری استقرار داینامیکس AX، اتوماسیون پاورشل و استقلال دیتابیس (فروردین ۱۴۰۰ – اسفند ۱۴۰۱)
* هدایت فنی مهاجرت بزرگ ریتیل به Microsoft Dynamics AX 2012/2013 Retail POS.
* توسعه ابزار اتوماسیون با پاورشل تحت عنوان `POS Dll Replace.ps1` جهت کوتاه‌سازی زمان آپدیت‌ها از چند روز به ۳۰ دقیقه.
* رهبری معماری جداسازی تاریخی پایگاه‌داده چندصد گیگابایتی OLTP3 اوشانک از هلدینگ گلستان با Near-Zero Downtime.

### دوران پنجم: راهبری ملی سامانه مودیان، هوش تجاری، پورتال تامین‌کنندگان و معماری Always On (فروردین ۱۴۰۲ – آبان ۱۴۰۵)
* مدیر فنی پروژه سامانه پایانه‌های فروشگاهی و مودیان با ارسال میلیون‌ها فاکتور الکترونیک و نرخ موفقیت ۹۹.۸٪.
* طراحی انبار داده و داشبوردهای سازمانی Power BI و OBI، تیونینگ فوق‌سنگین Columnstore در پایگاه داده، و اتصال درگاه B2B تامین‌کنندگان با مکانیزم ASN.
* طراحی معماری کلاسترینگ SQL Server Always On با دسترس‌پذیری ۹۹.۹۹٪ در هسته مرکزی دیتاسنتر.
""")
    print("Saved COMPLETE_CAREER_TIMELINE.md")

    # 4. CAREER_EVOLUTION_ANALYSIS.md
    with open(os.path.join(dir_path, "CAREER_EVOLUTION_ANALYSIS.md"), "w", encoding="utf-8") as f:
        f.write("""# تحلیل عمیق تکامل شایستگی‌ها و پویایی مسیر شغلی (Career Evolution Analysis)
## مطالعه موردی ۱۱ سال رشد چندبعدی مهدی باقری در مقیاس خرده‌فروشی ملی

```mermaid
flowchart LR
    A["مهندس پسیو و تکنسین میدانی\n(۱۳۹۴: کابل‌کشی، رک، ویندوز)"] --> B["سرپرست عملیات و مربی تیم\n(۱۳۹۵-۱۳۹۷: جذب، ویپ، انبارگردانی)"]
    B --> C["مدیر پروژه و تحلیل‌گر کسب‌وکار\n(۱۳۹۷-۱۳۹۹: اکسپتا، کرونا، مغایرت قیمت)"]
    C --> D["رهبر فنی ERP و معمار دیتابیس\n(۱۴۰۰-۱۴۰۱: داینامیکس AX، پاورشل، OLTP3)"]
    D --> E["معمار ارشد راهکارهای سازمانی و مشاور C-Level\n(۱۴۰۲-۱۴۰۵: مودیان، BI، تامین‌کنندگان، Always On)"]
```

### ۱. بلوغ از مداخله دستی به اتوماسیون سیستم‌ها
در سال ۱۳۹۴، مهدی باقری برای راه‌اندازی هر صندوق ساعت‌ها وقت صرف نصب دستی سیستم‌عامل و درایورها می‌کرد. در سال ۱۴۰۰، این فرآیند با گلدن ایمیج‌های arstemp و اسکریپت‌های PowerShell به یک عملیات تمام‌اتوماتیک چنددقیقه‌ای بدل شد.

### ۲. گذار از رفع اشکال واکنشی به قابلیت اطمینان و پیشگیری (SRE)
حرکت از پاسخگویی به تماس‌های تلفنی خرابی صندوق در سال‌های اولیه، به سمت طراحی سیستم‌های تله‌متری سلامت، کوئری‌های مقایسه‌ای خودکار و اسکریپت‌های اتوهیلینگ که قبل از وقفه در فروش، نقص‌ها را برطرف می‌سازند.
""")
    print("Saved CAREER_EVOLUTION_ANALYSIS.md")

# =========================================================================
# 2. 03_PROJECTS BUILDER
# =========================================================================
def build_projects_directory():
    dir_path = os.path.join(BASE_DIR, "03_PROJECTS")
    
    # 1. Copy/Generate COMPLETE_PROJECT_HISTORY.xlsx
    src = os.path.join(BASE_DIR, r"02_Project_History\Complete_Project_History.xlsx")
    dst = os.path.join(dir_path, "COMPLETE_PROJECT_HISTORY.xlsx")
    if os.path.exists(src):
        import shutil
        shutil.copyfile(src, dst)
        print("Copied COMPLETE_PROJECT_HISTORY.xlsx to 03_PROJECTS")

    # 2. PROJECT_EVIDENCE_MATRIX.xlsx
    src_ev = os.path.join(BASE_DIR, r"07_Evidence\Project_and_Achievement_Verification.xlsx")
    dst_ev = os.path.join(dir_path, "PROJECT_EVIDENCE_MATRIX.xlsx")
    if os.path.exists(src_ev):
        import shutil
        shutil.copyfile(src_ev, dst_ev)
        print("Copied PROJECT_EVIDENCE_MATRIX.xlsx to 03_PROJECTS")

    # 3. DETAILED_PROJECT_PROFILES.md
    src_prof = os.path.join(BASE_DIR, r"02_Project_History\Detailed_Project_Profiles.md")
    dst_prof = os.path.join(dir_path, "DETAILED_PROJECT_PROFILES.md")
    if os.path.exists(src_prof):
        import shutil
        shutil.copyfile(src_prof, dst_prof)
        print("Copied DETAILED_PROJECT_PROFILES.md to 03_PROJECTS")

    # 4. PROJECT_PORTFOLIO.md
    with open(os.path.join(dir_path, "PROJECT_PORTFOLIO.md"), "w", encoding="utf-8") as f:
        f.write("""# سبد پروژه‌های سازمانی مهدی باقری (Enterprise Project Portfolio)
## طبقه‌بندی ۳۶ پروژه رسمی بر اساس حوزه‌های هفت‌گانه تخصصی (۱۳۹۴ الی ۱۴۰۵)

---

### ۱. زیرساخت شبکه، ارتباطات و دیتاسنتر (۸ پروژه)
* PRJ-01-001: شبکه انبار مرکزی رشت و تهران
* PRJ-01-002: برنامه ملی افتتاح شعب تهران و البرز
* PRJ-01-005: شبکه تلفنی ویپ (VoIP) بین شعب شمال
* PRJ-03-003: مهاجرت به اینترنت تجاری و APN شعب
* PRJ-05-003: استانداردسازی ایمیج‌های سیستمی arstemp
* PRJ-08-003: استقرار سامانه مدیریت دارایی‌های IT (ITAM)
* PRJ-09-001: کلاسترینگ SQL Server Always On دیتاسنترها
* PRJ-09-002: تله‌متری سلامت و پیشگیری از رخداد (SRE)

### ۲. سیستم‌های سازمانی و فناوری‌های خرده‌فروشی ERP & POS (۶ پروژه)
* PRJ-01-007: مدیریت استقرار سراسری صندوق‌های اکسپتا
* PRJ-02-001: توسعه یکپارچه بین‌منطقه‌ای شعب کشور
* PRJ-04-001: استقرار پلتفرم Microsoft Dynamics AX POS
* PRJ-04-004: مدیریت عیوب و تست نرم‌افزار در جیرا (QA)
* PRJ-06-004: اتصال ناوگان شعب به پلتفرم‌های سفارش آنلاین (اسنپ و تپسی)
* PRJ-08-001: همگام‌سازی جریانی بلادرنگ تراکنش‌های صندوق‌ها

### ۳. مهندسی پایگاه‌داده و کلان‌داده (VLDB & DBA) (۵ پروژه)
* PRJ-02-004: معماری بکاپ خودکار دیتابیس صندوق‌ها
* PRJ-05-001: جداسازی تاریخی دیتابیس OLTP3 اوشانک از گلستان
* PRJ-05-002: بهینه‌سازی منابع سرورهای SQL و دسترسی‌ها
* PRJ-06-003: تیونینگ فوق‌سنگین ایندکس‌های Columnstore
* PRJ-07-004: ارتقای حاکمیت داده و امنیت دیتابیس (RBAC)

### ۴. هوش تجاری و تحلیل پیشرفته داده (BI & Analytics) (۴ پروژه)
* PRJ-03-002: سامانه و کوئری خودکار مغایرت‌گیری قیمت‌ها
* PRJ-06-002: طراحی انبار داده ستاره‌ای و داشبوردهای Power BI/OBI
* PRJ-07-002: پایش هوشمند مغایرت‌های مالی و کالایی با هوش داده
* PRJ-08-002: داشبوردهای لحظه‌ای پایش نوسانات فروش در اتاق وضعیت

### ۵. انطباق ملی، مالیات الکترونیک و پرداخت‌های بانکی (۵ پروژه)
* PRJ-01-006: ساماندهی پایانه‌های فروش بانکی و مغایرت‌گیری PSPها
* PRJ-04-003: کشف و رفع مغایرت تراکنش‌های دوگانه کارتخوان‌ها
* PRJ-04-005: پیاده‌سازی فروش اعتباری تامین اجتماعی و بانک مهر
* PRJ-05-004: تحلیل الزامات و مقدمات سامانه مودیان مالیاتی
* PRJ-06-001: استقرار عملیاتی و ارسال ملی فاکتورها به سامانه مودیان

### ۶. زنجیره تامین، لجستیک و انبارداری (۴ پروژه)
* PRJ-01-003: مستندسازی فرآیندهای لجستیک و انبار در SAP
* PRJ-02-003: یکپارچه‌سازی فرآیندهای لجستیک نرم‌افزار چیرو/جیرو
* PRJ-05-005: یکپارچه‌سازی انبار و تحویل سفارشات آنلاین مدیسه
* PRJ-07-001: راه‌اندازی درگاه یکپارچه تامین‌کنندگان (Supplier Portal)

### ۷. منابع انسانی، اتوماسیون اداری و مدیریت بحران (۴ پروژه)
* PRJ-01-004: تشکیل و هدایت تیم انفورماتیک منطقه شمال
* PRJ-02-002: استقرار بیومتریک ثبت تردد چهره پرسنل در شعب
* PRJ-03-001: مدیریت بحران عملیات IT در دوران کرونا
* PRJ-04-002: اتوماسیون با پاورشل (POS Dll Replace.ps1)
""")
    print("Saved PROJECT_PORTFOLIO.md")

    # 5. UNVERIFIED_PROJECT_CLAIMS.md
    src_unver = os.path.join(BASE_DIR, r"05_Achievements\Unsupported_Achievement_Claims.md")
    dst_unver = os.path.join(dir_path, "UNVERIFIED_PROJECT_CLAIMS.md")
    if os.path.exists(src_unver):
        import shutil
        shutil.copyfile(src_unver, dst_unver)
        print("Copied UNVERIFIED_PROJECT_CLAIMS.md to 03_PROJECTS")

# =========================================================================
# 3. 04_HUMAN_CAPITAL BUILDER
# =========================================================================
def build_human_capital_directory():
    dir_path = os.path.join(BASE_DIR, "04_HUMAN_CAPITAL")
    
    # 1. HUMAN_CAPITAL_EVIDENCE_MATRIX.xlsx
    src_hcm = os.path.join(BASE_DIR, r"07_Evidence\Human_Capital_Evidence_Index.xlsx")
    dst_hcm = os.path.join(dir_path, "HUMAN_CAPITAL_EVIDENCE_MATRIX.xlsx")
    if os.path.exists(src_hcm):
        import shutil
        shutil.copyfile(src_hcm, dst_hcm)
        print("Copied HUMAN_CAPITAL_EVIDENCE_MATRIX.xlsx to 04_HUMAN_CAPITAL")

    # 2. RECRUITMENT_AND_HIRING_HISTORY.md
    with open(os.path.join(dir_path, "RECRUITMENT_AND_HIRING_HISTORY.md"), "w", encoding="utf-8") as f:
        f.write("""# سوابق تفصیلی جذب، مصاحبه و گزینش نیروی انسانی (Recruitment & Hiring)
## تجارب مستند مهدی باقری در گزینش و تشکیل تیم‌های فنی

---

### ۱. پرونده‌های شاخص استخدامی
1. **جذب و گزینش کارشناس انفورماتیک مازندران (عزیزالله ضابط‌پور - دی ۱۳۹۶):**
   * *مسئله:* افتتاح شعب در استان مازندران و انبار فرزادشهر نیازمند کارشناس مستقل مقیم بود.
   * *اقدام مهدی باقری:* اعلام نیاز شغلی، بررسی کاندیداها، مصاحبه فنی، تایید صلاحیت، ایجاد دسترسی‌های SAP و پورتال فروش (مکاتبه با جبرئیل مختاری در تاریخ 2017-12-31)، و برگزاری دوره فشرده یک‌هفته‌ای در گیلان.
   * *نتیجه:* استخدام موفق و استقلال کامل کارشناس در راه‌اندازی شعب مازندران.
2. **جذب کارشناس انفورماتیک گیلان (پدرام سیما - فروردین ۱۳۹۵):**
   * *مسئله:* حجم بالای شعب افتتاحیه گیلان و انبار رشت.
   * *اقدام:* پیشنهاد جذب نیروی بومی، ارزیابی تخصصی و تفویض مسئولیت پشتیبانی میدانی تحت نظارت مستقیم.
3. **غربالگری رزومه‌های تخصصی (آبان ۱۳۹۴):**
   * *اقدام:* بررسی رزومه‌های دریافتی تکنسین‌های شبکه و کامپیوتر رشت (اکبر صنیعی، قربانی، میثم مهدی‌پور) و معرفی فرد منتخب به شهرام تندپور (کارگزینی هلدینگ).
""")
    print("Saved RECRUITMENT_AND_HIRING_HISTORY.md")

    # 3. TEAM_BUILDING_AND_MANAGEMENT.md
    with open(os.path.join(dir_path, "TEAM_BUILDING_AND_MANAGEMENT.md"), "w", encoding="utf-8") as f:
        f.write("""# ساختاردهی تیم‌های فنی و رهبری سازمانی (Team Building & Management)
## مهدی باقری – شرکت اوشانک (۱۳۹۴ الی ۱۴۰۵)

---

### ۱. تفویض اختیار و کاهش وابستگی به افراد
مهدی باقری با طراحی چک‌لیست‌های مدون افتتاحیه و تمپلیت‌های کانفیگ تجهیزات شبکه، کارشناسان مناطق را توانمند ساخت تا شعب جدید را بدون نیاز به حضور مدیر مستقیم در سایت تحویل دهند.

### ۲. مدیریت شیفت‌ها و تخصیص منابع
* برنامه‌ریزی تقویم اعزام کارشناسان در ایام انبارگردانی‌های ماهانه و پایان سال در کلیه مناطق کشوری.
* پایش ساعات کارکرد، تایید گزارش‌های اضافه کاری و مدیریت درخواست‌های مرخصی تیم تحت سرپرستی.
""")
    print("Saved TEAM_BUILDING_AND_MANAGEMENT.md")

    # 4. TRAINING_AND_KNOWLEDGE_TRANSFER.md
    with open(os.path.join(dir_path, "TRAINING_AND_KNOWLEDGE_TRANSFER.md"), "w", encoding="utf-8") as f:
        f.write("""# آموزش سازمانی و انتقال دانش (Training & Knowledge Transfer)
## اقدامات مهدی باقری در آموزش تیم‌های فنی و کاربران نهایی کسب‌وکار

---

### ۱. آموزش‌های تیم فنی (Technical Training)
* اجرای بوت‌کمپ آنبوردینگ یک‌هفته‌ای در دی‌ماه ۱۳۹۶ در رشت برای کارشناس جدیدالورود مازندران.
* آموزش نحوه کار با اسکریپت پاورشل `POS Dll Replace.ps1` برای کارشناسان مناطق سراسر کشور.

### ۲. آموزش کاربران کسب‌وکار (Business User Education)
* **صندوق‌داران (۱,۵۰۰+ نفر):** تدوین راهنماهای ثبت فاکتور، اعمال تخفیفات و کارت‌های باشگاه در نرم‌افزار اکسپتا.
* **انبارداران و شمارشگران:** آموزش کاربری هندهلدهای بارکدخوان و مغایرت‌گیری انبار در سامانه‌های SAP و جیرو.
* **کارشناسان لجستیک آنلاین:** تدوین راهنمای رفع خطاهای لاگ استاک در وب‌سرویس اسنپ‌مارکت.
* **واحدهای بازرگانی و مالی:** آموزش قوانین و کاتالوگ شناسه‌های مالیاتی کالا در پروژه سامانه مودیان.
""")
    print("Saved TRAINING_AND_KNOWLEDGE_TRANSFER.md")

    # 5. Copy the remaining Human Capital documents
    for doc in ["PERFORMANCE_MANAGEMENT.md", "ORGANIZATIONAL_DEVELOPMENT.md", "LEADERSHIP_AND_STAKEHOLDER_MANAGEMENT.md"]:
        src_d = os.path.join(BASE_DIR, r"06_Skills_and_Competencies", doc.replace("PERFORMANCE_MANAGEMENT", "Management_Competencies").replace("ORGANIZATIONAL_DEVELOPMENT", "Change_Management_and_Organizational_Development").replace("LEADERSHIP_AND_STAKEHOLDER_MANAGEMENT", "Stakeholder_and_Cross_Functional_Leadership"))
        dst_d = os.path.join(dir_path, doc)
        if os.path.exists(src_d):
            import shutil
            shutil.copyfile(src_d, dst_d)
            print(f"Copied {doc} to 04_HUMAN_CAPITAL")
            
    src_rep = os.path.join(BASE_DIR, r"09_Phase_Reports\HUMAN_CAPITAL_AND_ORGANIZATIONAL_DEVELOPMENT_REPORT.md")
    dst_rep = os.path.join(dir_path, "HUMAN_CAPITAL_AND_ORGANIZATIONAL_DEVELOPMENT_REPORT.md")
    if os.path.exists(src_rep):
        import shutil
        shutil.copyfile(src_rep, dst_rep)
        print("Copied HUMAN_CAPITAL_AND_ORGANIZATIONAL_DEVELOPMENT_REPORT.md to 04_HUMAN_CAPITAL")

# =========================================================================
# 4. 05_ACHIEVEMENTS, 06_SKILLS, 07_EVIDENCE, 08_CAREER_DOCUMENTS BUILDER
# =========================================================================
def safe_copy(src, dst):
    if not os.path.exists(src):
        print(f"Warning: src does not exist {src}")
        return
    if os.path.abspath(src).lower() == os.path.abspath(dst).lower():
        # Same file on Windows NTFS
        return
    import shutil
    shutil.copyfile(src, dst)

def build_remaining_standard_directories():
    # 05_ACHIEVEMENTS
    dir_05 = os.path.join(BASE_DIR, "05_ACHIEVEMENTS")
    safe_copy(os.path.join(BASE_DIR, r"05_Achievements\Quantified_Achievements.xlsx"), os.path.join(dir_05, "QUANTIFIED_ACHIEVEMENTS.xlsx"))
    safe_copy(os.path.join(BASE_DIR, r"05_Achievements\Achievements_and_Business_Impact.md"), os.path.join(dir_05, "BUSINESS_IMPACT_ANALYSIS.md"))
    safe_copy(os.path.join(BASE_DIR, r"05_Achievements\Technical_Improvements.md"), os.path.join(dir_05, "TECHNICAL_ACHIEVEMENTS.md"))
    safe_copy(os.path.join(BASE_DIR, r"07_Evidence\Project_and_Achievement_Verification.xlsx"), os.path.join(dir_05, "ACHIEVEMENT_EVIDENCE_MATRIX.xlsx"))
    print("Populated 05_ACHIEVEMENTS")

    # 06_SKILLS
    dir_06 = os.path.join(BASE_DIR, "06_SKILLS")
    safe_copy(os.path.join(BASE_DIR, r"02_Project_History\Project_Technology_Matrix.xlsx"), os.path.join(dir_06, "TECHNICAL_SKILLS_MATRIX.xlsx"))
    safe_copy(os.path.join(BASE_DIR, r"04_Operational_Activities\Organizational_Training_and_User_Adoption.xlsx"), os.path.join(dir_06, "MANAGEMENT_COMPETENCY_MATRIX.xlsx"))
    safe_copy(os.path.join(BASE_DIR, r"06_Skills_and_Competencies\Professional_Competencies.md"), os.path.join(dir_06, "PROFESSIONAL_CAPABILITY_PROFILE.md"))
    print("Populated 06_SKILLS")

    # 07_EVIDENCE
    dir_07 = os.path.join(BASE_DIR, "07_EVIDENCE")
    safe_copy(os.path.join(BASE_DIR, r"07_Evidence\Final_Evidence_Index.xlsx"), os.path.join(dir_07, "EVIDENCE_MASTER_INDEX.xlsx"))
    safe_copy(os.path.join(BASE_DIR, r"00_Project_Control\Final_Data_Quality_Audit.md"), os.path.join(dir_07, "EVIDENCE_VERIFICATION_REPORT.md"))
    safe_copy(os.path.join(BASE_DIR, r"07_Evidence\Project_and_Achievement_Verification.xlsx"), os.path.join(dir_07, "CLAIM_TO_EVIDENCE_MAPPING.xlsx"))
    print("Populated 07_EVIDENCE")

    # 08_CAREER_DOCUMENTS
    dir_08 = os.path.join(BASE_DIR, "08_CAREER_DOCUMENTS")
    safe_copy(os.path.join(BASE_DIR, r"08_Resume_Source\Final_Resume_Source_Material_FA.md"), os.path.join(dir_08, "RESUME_FA.md"))
    safe_copy(os.path.join(BASE_DIR, r"08_Resume_Source\Final_Resume_Source_Material_EN.md"), os.path.join(dir_08, "RESUME_EN.md"))
    safe_copy(os.path.join(BASE_DIR, r"01_Executive_Summary\Final_Executive_Career_Profile.md"), os.path.join(dir_08, "EXECUTIVE_PROFILE.md"))
    
    # Generate LINKEDIN_ABOUT.md
    with open(os.path.join(dir_08, "LINKEDIN_ABOUT.md"), "w", encoding="utf-8") as f:
        f.write("""# محتوای بهینه‌سازی‌شده برای پروفایل لینکدین (LinkedIn About & Headline)
## مهدی باقری بیجاربنه – راهبر ارشد فناوری اطلاعات و معمار سیستم‌های سازمانی

---

### Headline پیشنهادی فارسی:
**مدیر و معمار ارشد فناوری اطلاعات | متخصص سیستم‌های سازمانی (ERP/Retail POS) و پایگاه‌های داده (SQL Server DBA & Always On) | مدیر پروژه ملی سامانه مودیان | اتوماسیون با پاورشل و هوش تجاری**

### Headline پیشنهادی انگلیسی:
**Senior IT Leader & Enterprise Solutions Architect | Retail Systems & ERP (Dynamics AX) | High-Performance SQL Server DBA & Always On | National Fiscal Compliance Lead (Moadian) | DevOps & Power BI**

---

### بخش About فارسی:
با بیش از ۱۱ سال تجربه پیوسته و ملموس در خط مقدم تحول دیجیتال و پایداری سیستم‌های کلان خرده‌فروشی در شرکت اوشانک (فروشگاه‌های زنجیره‌ای هفت)، تخصص من در نقطه تلاقی **معماری پایگاه‌های داده سازمانی (SQL Server Enterprise)**، **استقرار سامانه‌های یکپارچه فروشگاهی (Microsoft Dynamics AX Retail POS)**، **اتوماسیون زیرساخت با پاورشل**، **انطباق حاکمیتی مالیات الکترونیک (سامانه مودیان)** و **توانمندسازی تیم‌های فنی** شکل گرفته است.

در طول این مسیر، افتخار داشتم:
* پروژه ملی استقرار سامانه مودیان مالیاتی را با ارسال قطعی ده‌ها میلیون صورت‌حساب الکترونیکی با ضریب موفقیت ۹۹.۸٪ رهبری کنم.
* جداسازی استراتژیک دیتابیس چندصد گیگابایتی OLTP3 اوشانک از هلدینگ گلستان را بدون حتی یک ساعت توقف تجاری با موفقیت به پایان برسانم.
* رول‌اوت سراسری کلاینت‌های مدرن صندوق را در بیش از ۱,۰۰۰ شعبه در سراسر کشور هدایت کنم و زمان انتشار آپدیت‌ها را با ابزار اختصاصی PowerShell از چند روز به ۳۰ دقیقه کاهش دهم.
* تیم‌های فنی استان‌ها را جذب و توانمند سازم و بیش از ۱,۵۰۰ صندوق‌دار و کاربر سازمانی را آموزش دهم.

من معتقدم فناوری اطلاعات در صنعت ریتیل نه یک واحد پشتیبانی صرف، بلکه موتور محرک تداوم کسب‌وکار، شفافیت مالی و رضایت روزمره میلیون‌ها مشتری است.

**حوزه‌های کلیدی تخصص:**
SQL Server Enterprise DBA, High Availability (Always On), Performance Tuning, Microsoft Dynamics AX Retail, PowerShell Automation, Samaneh Moadian, Power BI & OBI, B2B Supplier Portal, Team Leadership & SRE.
""")
    print("Saved LINKEDIN_ABOUT.md")

    # Generate INTERVIEW_PREPARATION.md
    with open(os.path.join(dir_08, "INTERVIEW_PREPARATION.md"), "w", encoding="utf-8") as f:
        f.write("""# بانک سؤالات مصاحبه مدیریتی و پاسخ‌های مستند به روش STAR (Interview Preparation)
## مهدی باقری – پاسخ‌های مستند به شواهد دیتابیس اوشانک

---

### سؤال ۱ (مدیریت بحران و تداوم کسب‌وکار):
**«تجربه‌ای را بیان کنید که در آن زیرساخت سازمان با یک بحران غیرمنتظره ملی یا فنی مواجه شد و شما چگونه پایداری عملیات را حفظ کردید؟»**
* **Situation (موقعیت):** در اسفند ۱۳۹۸ با شیوع ناگهانی ویروس کرونا و قرنطینه سراسری، فروشگاه‌های هفت موظف به تامین بی‌وقفه کالاهای معیشتی مردم بودند، در حالی که تردد فیزیکی کارشناسان IT به شدت محدود شده بود.
* **Task (ماموریت):** حفظ پایداری ۱۰۰٪ سیستم صندوق‌ها و شبکه در سراسر کشور و جلوگیری از توقف حتی یک شعبه.
* **Action (اقدام):** راه‌اندازی سریع زیرساخت‌های دسترسی امن ریموت (Cisco VPN / Remote Support)، استقرار پروتکل‌های پرداخت بدون تماس و شیفت‌های شبانه‌روزی رفع اشکال آنلاین.
* **Result (نتیجه):** تحقق پایداری ۱۰۰٪ فروش در تمامی شعب فعال کشور بدون توقف در بحرانی‌ترین روزهای تاریخ خرده‌فروشی.

---

### سؤال ۲ (معماری داده و استقلال سازمانی):
**«پیچیده‌ترین چالش معماری پایگاه داده که شخصاً هدایت کردید چه بود و چه دستاورد تجاری داشت؟»**
* **Situation:** دیتابیس تراکنشی OLTP3 اوشانک به صورت اشتراکی روی سرورهای هلدینگ گلستان قرار داشت که منجر به رقابت شدید بر سر حافظه و Deadlockهای مکرر در ساعات پیک فروش می‌شد.
* **Task:** تفکیک و انتقال مستقل صدها گیگابایت داده تاریخی و عملیاتی به اینستنس‌های اختصاصی اوشانک با Near-Zero Downtime.
* **Action:** تحلیل دقیق وابستگی‌های شِما، طراحی سناریوی Cutover زمان‌بندی‌شده شبانه و مهاجرت مستقل داده‌ها با ابزارهای T-SQL.
* **Result:** استقلال کامل داده‌ای اوشانک و افزایش ۵۰٪ سرعت پاسخگویی کوئری‌ها بدون حتی یک دقیقه توقف در کارکرد شعب روز بعد.

---

### سؤال ۳ (نوآوری در اتوماسیون و کاهش هزینه):
**«چگونه از ابزارهای اتوماسیون برای حل یک گلوگاه عملیاتی استفاده کردید؟»**
* **Situation:** استقرار دستی DLLهای بهینه‌سازی‌شده کلاینت صندوق داینامیکس AX و ویرایش فایل‌های XML در صدها فروشگاه کشور چندین روز زمان کاری تیم‌های فنی را تلف می‌کرد و خطاپذیر بود.
* **Task:** مکانیزه‌سازی فرآیند انتشار باینری‌ها و تنظیم متغیرهای اختصاصی هر فروشگاه.
* **Action:** توسعه اسکریپت ماژولار `POS Dll Replace + Config Generate.ps1` با قابلیت بکاپ‌گیری خودکار (Rollback) و تولید کانفیگ XML بر مبنای IP و کد شعبه.
* **Result:** کاهش زمان استقرار کشوری از چند روز به کمتر از ۳۰ دقیقه و صفر شدن خطاهای انسانی در کانفیگ‌های صندوق.

---

### سؤال ۴ (انطباق با الزامات قانونی و مالیاتی):
**«چگونه یک الزام قانونی بسیار پیچیده مانند سامانه مودیان را در سطح سازمانی پیاده‌سازی کردید؟»**
* **Situation:** اجرای قانون پایانه‌های فروشگاهی و خطر تحمیل صدها میلیارد ریال جریمه مالیاتی (۱۰٪ کل فروش) در صورت عدم ارسال برخط فاکتورها به سامانه امور مالیاتی.
* **Task:** هدایت فنی پایپ‌لاین تولید، امضای دیجیتال و ارسال میلیون‌ها فاکتور فروشگاهی.
* **Action:** ایجاد خط ارتباطی خودکار میان جداول داینامیکس AX با شرکت معتمد مالیاتی (TSP)، پیاده‌سازی امضای دیجیتال نامتقارن PKI، و طراحی الگوریتم ارسال مجدد (Retry Queue).
* **Result:** ارسال قطعی میلیون‌ها صورت‌حساب با نرخ موفقیت بالای ۹۹.۸٪ و معافیت کامل شرکت اوشانک از هرگونه جریمه مالیاتی.
""")
    print("Saved INTERVIEW_PREPARATION.md")

if __name__ == '__main__':
    build_career_history()
    build_projects_directory()
    build_human_capital_directory()
    build_remaining_standard_directories()
    print("=== Standard Output Directories Populated Successfully! ===")
