# -*- coding: utf-8 -*-
"""
نظام إدارة المستخدمين، تسجيل الدخول، وتوزيع الصلاحيات
Authentication and Role-Based Access Control (RBAC)
"""
import hashlib
import sqlite3
import streamlit as st
import config
import database

def hash_password(password: str) -> str:
    """تشفير كلمة المرور باستخدام SHA-256 مع Salt ثابت للنظام"""
    salt = "FTTH_EGYPT_FIBER_2026_SECURE"
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """التحقق من صحة كلمة المرور المدخلة"""
    return hash_password(password) == hashed

def init_default_users():
    """
    تهيئة المستخدمين الافتراضيين:
    - يضمن دائماً وجود حساب Admin بغض النظر عن حالة الجدول.
    - يُضيف مستخدمين تجريبيين شاملين لجميع القطاعات الميدانية إن كان الجدول فارغاً.
    """
    conn = database.get_connection()
    cursor = conn.cursor()

    # ضمان وجود حساب المدير العام دائماً (INSERT OR IGNORE)
    cursor.execute("""
        INSERT OR IGNORE INTO users (username, password_hash, full_name, role, assigned_sector)
        VALUES (?, ?, ?, ?, ?)
    """, ("admin", hash_password("admin123"), "مدير النظام العام", config.ROLE_ADMIN, None))
    conn.commit()

    # إضافة مستخدمين افتراضيين للقطاعات فقط إذا كان الجدول شبه فارغ (مدير فقط)
    cursor.execute("SELECT COUNT(*) FROM users;")
    count = cursor.fetchone()[0]

    if count <= 1:
        # مستخدمون افتراضيون يغطون أبرز القطاعات الميدانية
        default_editors = [
            # (username, password, full_name, role, assigned_sector)
            ("editor_cairo_east",  hash_password("cairo_e123"),  "مهندس قطاع شرق القاهرة",              config.ROLE_EDITOR, "قطاع شرق القاهرة"),
            ("editor_cairo_west",  hash_password("cairo_w123"),  "مهندس قطاع غرب القاهرة",              config.ROLE_EDITOR, "قطاع غرب القاهرة"),
            ("editor_new_cairo",   hash_password("new_cairo123"), "مهندس قطاع مناطق القاهرة الجديدة",   config.ROLE_EDITOR, "قطاع مناطق القاهرة الجديدة"),
            ("editor_giza",        hash_password("giza123"),      "مهندس قطاع الجيزة",                   config.ROLE_EDITOR, "قطاع الجيزة"),
            ("editor_october",     hash_password("oct123"),       "مهندس قطاع أكتوبر",                   config.ROLE_EDITOR, "قطاع أكتوبر"),
            ("editor_saeed_south", hash_password("saeed_s123"),  "مهندس قطاع جنوب الصعيد",              config.ROLE_EDITOR, "قطاع جنوب الصعيد"),
            ("editor_saeed_north", hash_password("saeed_n123"),  "مهندس قطاع شمال الصعيد",              config.ROLE_EDITOR, "قطاع شمال الصعيد"),
            ("editor_saeed_mid",   hash_password("saeed_m123"),  "مهندس قطاع وسط الصعيد",               config.ROLE_EDITOR, "قطاع وسط الصعيد"),
            ("editor_delta_e1",    hash_password("delta_e1_123"), "مهندس شرق الدلتا 1",                  config.ROLE_EDITOR, "شرق الدلتا 1"),
            ("editor_delta_e2",    hash_password("delta_e2_123"), "مهندس شرق الدلتا 2",                  config.ROLE_EDITOR, "شرق الدلتا 2"),
            ("editor_ismailia",    hash_password("ismailia123"),  "مهندس قطاع الإسماعيلية وشمال سيناء", config.ROLE_EDITOR, "قطاع الاسماعيلية وشمال سيناء"),
            ("editor_suez",        hash_password("suez123"),      "مهندس قطاع السويس",                   config.ROLE_EDITOR, "قطاع السويس"),
            ("editor_alex",        hash_password("alex123"),      "مهندس قطاع الأسكندرية",               config.ROLE_EDITOR, "قطاع الأسكندرية"),
            ("editor_north_coast", hash_password("coast123"),     "مهندس قطاع الساحل الشمالى ومطروح",   config.ROLE_EDITOR, "قطاع الساحل الشمالى ومطروح"),
            ("editor_delta_west",  hash_password("delta_w123"),   "مهندس قطاع غرب الدلتا",               config.ROLE_EDITOR, "قطاع غرب الدلتا"),
            ("editor_delta_mid",   hash_password("delta_m123"),   "مهندس قطاع وسط الدلتا",               config.ROLE_EDITOR, "قطاع وسط الدلتا"),
            ("viewer",             hash_password("viewer123"),    "مستعرض عام للتقارير",                  config.ROLE_VIEWER, None),
        ]
        for u in default_editors:
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO users (username, password_hash, full_name, role, assigned_sector)
                    VALUES (?, ?, ?, ?, ?)
                """, u)
            except Exception:
                pass
        conn.commit()

    conn.close()

def authenticate(username, password):
    """التحقق من بيانات الدخول وإرجاع بيانات المستخدم إذا صحيحة"""
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username.strip(),))
    row = cursor.fetchone()
    conn.close()

    if row and verify_password(password, row["password_hash"]):
        return dict(row)
    return None

def get_all_users():
    """الحصول على قائمة بجميع المستخدمين (للوحة تحكم المدير)"""
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, full_name, role, assigned_sector, created_at FROM users ORDER BY role, assigned_sector, id;")
    users = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return users

def create_user(username, password, full_name, role, assigned_sector):
    """إنشاء مستخدم جديد في النظام"""
    conn = database.get_connection()
    cursor = conn.cursor()
    try:
        sector_val = None if (not assigned_sector or assigned_sector in ("الكل", config.SECTOR_ALL, "جميع القطاعات (غير مقيد)")) else assigned_sector
        cursor.execute("""
            INSERT INTO users (username, password_hash, full_name, role, assigned_sector)
            VALUES (?, ?, ?, ?, ?)
        """, (username.strip(), hash_password(password), full_name.strip(), role, sector_val))
        conn.commit()
        return True, "تم إضافة المستخدم بنجاح"
    except sqlite3.IntegrityError:
        return False, "اسم المستخدم مسجل مسبقاً، يرجى اختيار اسم آخر"
    except Exception as e:
        return False, f"حدث خطأ: {e}"
    finally:
        conn.close()

def delete_user(user_id):
    """حذف مستخدم من النظام"""
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return True

def update_user(user_id, full_name, role, assigned_sector, password=None):
    """تحديث بيانات المستخدم وصلاحياته والقطاع المخصص له (للمدير)"""
    conn = database.get_connection()
    cursor = conn.cursor()
    try:
        sector_val = None if (not assigned_sector or assigned_sector in ("الكل", config.SECTOR_ALL, "جميع القطاعات (غير مقيد)")) else assigned_sector
        if password and password.strip():
            cursor.execute("""
                UPDATE users SET full_name = ?, role = ?, assigned_sector = ?, password_hash = ?
                WHERE id = ?
            """, (full_name.strip(), role, sector_val, hash_password(password), user_id))
        else:
            cursor.execute("""
                UPDATE users SET full_name = ?, role = ?, assigned_sector = ?
                WHERE id = ?
            """, (full_name.strip(), role, sector_val, user_id))
        conn.commit()
        return True, "تم تحديث بيانات المستخدم بنجاح"
    except Exception as e:
        return False, f"حدث خطأ أثناء التحديث: {e}"
    finally:
        conn.close()


def is_authenticated():
    """فحص حالة تسجيل دخول الجلسة الحالية"""
    return st.session_state.get("authenticated", False)

def current_user():
    """إرجاع بيانات المستخدم الحالي المسجل"""
    return st.session_state.get("user", None)

def login_user(user_info):
    """تثبيت حالة الدخول في الجلسة"""
    st.session_state["authenticated"] = True
    st.session_state["user"] = user_info

def logout_user():
    """تسجيل الخروج ومسح بيانات الجلسة"""
    st.session_state["authenticated"] = False
    st.session_state["user"] = None
    st.rerun()

def can_edit(target_sector=None):
    """
    التحقق من صلاحية التعديل:
    - المدير Admin: يعدل في أي قطاع.
    - المحرر Editor: يعدل فقط في قطاعه المخصص (أو في الكل إذا لم يكن مقيداً).
    - المستعرض Viewer: لا يمكنه التعديل نهائياً.
    """
    user = current_user()
    if not user:
        return False
    if user["role"] == config.ROLE_ADMIN:
        return True
    if user["role"] == config.ROLE_EDITOR:
        if not user.get("assigned_sector"):
            return True
        if target_sector is None:
            return True
        return user.get("assigned_sector") == target_sector
    return False

def render_login_form():
    """عرض نموذج تسجيل الدخول بتصميم عصري وألوان مريحة للعين"""
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(74,28,109,0.95) 0%, rgba(42,15,69,0.95) 100%); border: 1px solid rgba(168,85,247,0.3); border-radius: 24px; padding: 40px; box-shadow: 0 20px 50px rgba(0,0,0,0.4); backdrop-filter: blur(10px); margin-top: 40px; text-align: center;">
            <div style="background: rgba(168,85,247,0.2); width: 90px; height: 90px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px auto; border: 2px solid rgba(168,85,247,0.5);">
                <span style="font-size: 42px;">🟣</span>
            </div>
            <h2 style="color: #ffffff; font-weight: 800; margin-bottom: 6px; font-size: 1.5rem;">بوابة التحويل الرقمي FTTH</h2>
            <p style="color: rgba(255,255,255,0.75); font-size: 0.9rem; margin-bottom: 0;">المصرية للاتصالات WE — نظام إدارة الفايبر الضوئي</p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("👤 اسم المستخدم (Username)", placeholder="أدخل اسم المستخدم...")
            password = st.text_input("🔑 كلمة المرور (Password)", type="password", placeholder="أدخل كلمة المرور...")

            submit = st.form_submit_button("تسجيل الدخول للمنصة", use_container_width=True, type="primary")

            if submit:
                if not username or not password:
                    st.error("⚠️ يرجى إدخال اسم المستخدم وكلمة المرور")
                else:
                    user = authenticate(username, password)
                    if user:
                        login_user(user)
                        sector_msg = f" — {user['assigned_sector']}" if user.get('assigned_sector') else " — كامل الصلاحيات"
                        st.success(f"✅ مرحباً بك، {user['full_name']}{sector_msg}")
                        st.rerun()
                    else:
                        st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة")

        # صندوق إرشادي بالحسابات الجاهزة للتجربة
        with st.expander("🔑 حسابات تجريبية جاهزة للاختبار السريع"):
            st.markdown("""
            | الدور | اسم المستخدم | كلمة المرور | القطاع |
            | :--- | :--- | :--- | :--- |
            | **مدير عام (Admin)** | `admin` | `admin123` | جميع القطاعات |
            | **محرر قطاع** | `editor_cairo_east` | `cairo_e123` | قطاع شرق القاهرة |
            | **محرر قطاع** | `editor_cairo_west` | `cairo_w123` | قطاع غرب القاهرة |
            | **محرر قطاع** | `editor_giza` | `giza123` | قطاع الجيزة |
            | **محرر قطاع** | `editor_october` | `oct123` | قطاع أكتوبر |
            | **محرر قطاع** | `editor_alex` | `alex123` | قطاع الأسكندرية |
            | **محرر قطاع** | `editor_delta_e2` | `delta_e2_123` | شرق الدلتا 2 |
            | **مستعرض** | `viewer` | `viewer123` | عرض فقط |
            """)

