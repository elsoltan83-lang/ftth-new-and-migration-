# -*- coding: utf-8 -*-
"""
إعدادات التطبيق وثوابت مشروع الفايبر FTTH
Application Configuration and Constants
"""

APP_TITLE = "منصة إدارة أعمال الفايبر والتحويل النحاسي | FTTH & Migration"
APP_SUBTITLE = "نظام ذكي متكامل لمتابعة مؤشرات الإنجاز، التحويل، والعمليات الميدانية"
APP_VERSION = "2.0.0"

# مسارات الملفات وقاعدة البيانات
DB_PATH = "fiber_management.db"
DEFAULT_EXCEL_PATH = "FTTH مشروع.xlsx"

# أعمدة البيانات ومسمياتها بالعربية
COLUMN_MAP = {
    "Senior_Sector": "الرئاسة / الإدارة العليا",
    "Sector": "القطاع",
    "Region": "المنطقة / السنترال",
    "Type": "نوع الخط / النمط",
    # شبكة جديدة New FTTH
    "New_Completed_YTD": "منجز جديد تراكمي (YTD)",
    "New_Survey_Done_YTD": "معاينات جديدة تراكمي (YTD)",
    "New_Last_7_Days": "جديد آخر 7 أيام",
    "New_Yesterday": "جديد الأمس",
    "New_Pending_Survey": "معاينات جديدة معلقة",
    # تحويل من نحاس إلى فايبر Migration
    "Migration_Completed_YTD": "تحويل منجز تراكمي (YTD)",
    "Migration_Survey_Done_YTD": "معاينات تحويل تراكمي (YTD)",
    "Migration_Last_7_Days": "تحويل آخر 7 أيام",
    "Migration_Yesterday": "تحويل الأمس",
    "Migration_Pending_Survey": "معاينات تحويل معلقة",
    # المؤشرات والمستهدف Flagged
    "Flagged_2026": "المستهدف الكلي 2026 (Flagged)",
    "Flagged_Last_7_Days": "مؤشر آخر 7 أيام",
    "Flagged_Yesterday": "مؤشر الأمس"
}

NUMERIC_COLUMNS = [
    "New_Completed_YTD", "New_Survey_Done_YTD", "New_Last_7_Days", "New_Yesterday", "New_Pending_Survey",
    "Migration_Completed_YTD", "Migration_Survey_Done_YTD", "Migration_Last_7_Days", "Migration_Yesterday", "Migration_Pending_Survey",
    "Flagged_2026", "Flagged_Last_7_Days", "Flagged_Yesterday"
]

ALL_COLUMNS = [
    "id", "Senior_Sector", "Sector", "Region", "Type",
    "New_Completed_YTD", "New_Survey_Done_YTD", "New_Last_7_Days", "New_Yesterday", "New_Pending_Survey",
    "Migration_Completed_YTD", "Migration_Survey_Done_YTD", "Migration_Last_7_Days", "Migration_Yesterday", "Migration_Pending_Survey",
    "Flagged_2026", "Flagged_Last_7_Days", "Flagged_Yesterday", "last_updated"
]

# الأدوار المعتمدة
ROLE_ADMIN = "admin"
ROLE_EDITOR = "editor"
ROLE_VIEWER = "viewer"

ROLES_NAMES = {
    ROLE_ADMIN: "مدير النظام (كامل الصلاحيات)",
    ROLE_EDITOR: "محرر بيانات / مدير قطاع (تعديل وإضافة)",
    ROLE_VIEWER: "مستعرض (قراءة فقط)"
}

# ثابت القطاع الكامل (Admin بدون قيود)
SECTOR_ALL = "جميع القطاعات"

# قائمة القطاعات الكاملة (مطابقة لأسماء القطاعات في قاعدة البيانات)
# هذه القائمة تُستخدم كـ Fallback في حالة عدم وجود بيانات في DB بعد
ALL_SECTORS = [
    "قطاع شرق القاهرة",
    "قطاع غرب القاهرة",
    "قطاع مناطق القاهرة الجديدة",
    "قطاع الجيزة",
    "قطاع أكتوبر",
    "قطاع جنوب الصعيد",
    "قطاع شمال الصعيد",
    "قطاع وسط الصعيد",
    "شرق الدلتا 1",
    "شرق الدلتا 2",
    "قطاع الاسماعيلية وشمال سيناء",
    "قطاع السويس",
    "قطاع الأسكندرية",
    "قطاع الساحل الشمالى ومطروح",
    "قطاع غرب الدلتا",
    "قطاع وسط الدلتا",
]
