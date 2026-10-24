# -*- coding: utf-8 -*-
"""
app.py — نقطة الدخول الرئيسية لمنصة إدارة أعمال الفايبر والتحويل النحاسي FTTH
يجمع نظام تسجيل الدخول، الداشبورد التفاعلي، محرر البيانات، وإدارة المستخدمين
"""
import streamlit as st

# ══════════════════════════════════════════════
# إعداد الصفحة الأساسي (يجب أن يكون أول استدعاء)
# ══════════════════════════════════════════════
st.set_page_config(
    page_title="WE | منصة إدارة الفايبر FTTH",
    page_icon="🟣",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "منصة إدارة مشاريع تحويل الخطوط النحاسية للألياف الضوئية — v2.0"
    }
)

# ══════════════════════════════════════════════
# استيراد الوحدات بعد set_page_config
# ══════════════════════════════════════════════
import database
import auth
import styling
import config
from components import dashboard, data_editor, user_management

# ══════════════════════════════════════════════
# تهيئة قاعدة البيانات والمستخدمين الافتراضيين
# ══════════════════════════════════════════════
@st.cache_resource
def initialize_system():
    """تُشغَّل مرة واحدة فقط عند أول تشغيل للتطبيق"""
    database.init_db()
    auth.init_default_users()
    return True

initialize_system()

# ══════════════════════════════════════════════
# تطبيق التنسيقات والخطوط العصرية
# ══════════════════════════════════════════════
styling.apply_custom_css()

# ══════════════════════════════════════════════
# منطق تسجيل الدخول — عرض نموذج الدخول إذا لم يكن مسجلاً
# ══════════════════════════════════════════════
if not auth.is_authenticated():
    auth.render_login_form()
    st.stop()

# ══════════════════════════════════════════════
# الحصول على بيانات المستخدم الحالي
# ══════════════════════════════════════════════
current_user = auth.current_user()
user_role = current_user.get("role", "viewer")
assigned_sector = current_user.get("assigned_sector")

# ══════════════════════════════════════════════
# الشريط الجانبي (Sidebar Navigation)
# ══════════════════════════════════════════════
with st.sidebar:
    # شعار وعنوان المنصة في الشريط الجانبي
    st.markdown("""
    <div style=\"text-align:center; padding: 10px 0 14px 0;\">
        <div style=\"background:#662D91; width:80px; height:80px; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto;\">
            <span style=\"color:#ffffff; font-weight:800; font-size:28px;\">WE</span>
        </div>
        <div style=\"font-weight:800; font-size:1.05rem; color:#ffffff; line-height:1.3; margin-top:6px;\">
            منصة إدارة الفايبر FTTH
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # بطاقة المستخدم الحالي
    role_badge = {"admin": "badge-admin", "editor": "badge-editor", "viewer": "badge-viewer"}.get(user_role, "badge-viewer")
    role_name = config.ROLES_NAMES.get(user_role, user_role)
    sector_disp = assigned_sector or "جميع القطاعات"

    st.markdown(f"""
    <div class="user-status-card">
        <div style="font-size:0.8rem; color:#cbd5e1; margin-bottom:4px;">👤 المستخدم الحالي</div>
        <div style="font-weight:800; color:#ffffff; font-size:0.95rem;">{current_user.get("full_name", "")}</div>
        <div style="font-size:0.78rem; color:#cbd5e1; margin:2px 0;">@{current_user.get("username", "")}</div>
        <span class="user-role-badge {role_badge}">{role_name}</span>
        <div style="font-size:0.75rem; color:#e2e8f0; margin-top:6px;">📍 {sector_disp}</div>
    </div>
    """, unsafe_allow_html=True)

    # قائمة التنقل الرئيسية
    st.markdown("#### 📋 قائمة التنقل")

    pages = {
        "🏠 لوحة المؤشرات الرئيسية": "dashboard",
        "✏️ إدخال وتعديل البيانات": "data_editor",
    }

    # إضافة صفحة إدارة المستخدمين للمدير فقط
    if user_role == config.ROLE_ADMIN:
        pages["👥 إدارة المستخدمين والصلاحيات"] = "user_management"

    # تهيئة الصفحة الافتراضية
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "dashboard"

    for label, page_key in pages.items():
        is_active = st.session_state["current_page"] == page_key
        btn_type = "primary" if is_active else "secondary"
        if st.button(label, key=f"nav_{page_key}", use_container_width=True, type=btn_type):
            st.session_state["current_page"] = page_key
            st.rerun()

    st.divider()

    # معلومات الملف والمزامنة
    import os
    if os.path.exists(config.DEFAULT_EXCEL_PATH):
        mtime = os.path.getmtime(config.DEFAULT_EXCEL_PATH)
        from datetime import datetime
        mtime_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
        st.markdown(f"""
        <div style="font-size:0.75rem; color:#cbd5e1; text-align:center; padding:8px; background: rgba(0,0,0,0.25); border-radius:8px; border:1px solid rgba(255,255,255,0.1);">
            📄 <b>FTTH مشروع.xlsx</b><br>
            آخر مزامنة: {mtime_str}
        </div>
        """, unsafe_allow_html=True)
        st.write("")

    # زر تسجيل الخروج
    if st.button("🚪 تسجيل الخروج", use_container_width=True, key="logout_btn"):
        auth.logout_user()

# ══════════════════════════════════════════════
# عرض الصفحة المحددة مع التحقق الأمني
# ══════════════════════════════════════════════
current_page = st.session_state.get("current_page", "dashboard")

# إذا حاول مستخدم غير مصرح له الدخول لصفحة المستخدمين يتم تحويله للرئيسية
if current_page == "user_management" and user_role != config.ROLE_ADMIN:
    st.session_state["current_page"] = "dashboard"
    current_page = "dashboard"

if current_page == "dashboard":
    dashboard.show_dashboard(current_user)

elif current_page == "data_editor":
    data_editor.render_data_editor(current_user)

elif current_page == "user_management":
    user_management.render_user_management(current_user)

else:
    st.error("الصفحة غير موجودة.")

