# -*- coding: utf-8 -*-
"""
صفحة إدارة المستخدمين والصلاحيات وتوزيع القطاعات (User Management - Admin Only)
تسمح لمدير النظام حصراً بإنشاء وتعديل وحذف المستخدمين، وتعيين الأدوار،
وربط كل محرر بالقطاع الميداني الخاص به.
"""
import streamlit as st
import auth
import database
import styling
import config


def render_user_management(user=None):
    user = user or {}
    current_role = user.get("role")

    if current_role != config.ROLE_ADMIN:
        st.error("🔒 عذراً، هذه الصفحة مخصصة لمدير النظام (Admin) فقط.")
        return

    styling.render_header(
        "إدارة المستخدمين والصلاحيات وتوزيع القطاعات",
        "لوحة التحكم المركزية لإنشاء المستخدمين، تعيين الصلاحيات، وربط المحررين بالقطاعات الميدانية",
        icon="users-cog"
    )

    all_db_sectors = database.get_unique_options("Sector")
    # استخدم القطاعات من DB إن وُجدت، وإلا استخدم القائمة الثابتة من config
    sectors_list = all_db_sectors if all_db_sectors else config.ALL_SECTORS
    sector_choices = [f"{config.SECTOR_ALL} (غير مقيد)"] + sectors_list

    # ============================================================
    # 1. قسم إضافة مستخدم جديد
    # ============================================================
    with st.expander("➕ إضافة مستخدم جديد وتحديد قطاعه الميداني", expanded=False):
        with st.form("add_user_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                new_username = st.text_input("اسم المستخدم (Username)*", placeholder="مثال: eng_mohamed")
                new_fullname = st.text_input("الاسم الكامل للمهندس/الموظف*", placeholder="المهندس / محمد أحمد")
            with col2:
                new_password = st.text_input("كلمة المرور*", type="password", placeholder="6 أحرف على الأقل")
                new_role = st.selectbox(
                    "الدور / الصلاحية*",
                    options=[config.ROLE_EDITOR, config.ROLE_VIEWER, config.ROLE_ADMIN],
                    format_func=lambda r: config.ROLES_NAMES.get(r, r)
                )

            # تحديد القطاع المخصص
            assigned_sec_choice = st.selectbox(
                "القطاع المخصص للمستخدم:",
                options=sector_choices,
                help="محرر البيانات: سيُقيَّد بالقطاع المختار فقط. مدير/مستعرض: اختر 'جميع القطاعات'."
            )

            submitted = st.form_submit_button("💾 إنشاء وتفعيل حساب المستخدم", type="primary", use_container_width=True)
            if submitted:
                if not new_username.strip() or not new_password.strip() or not new_fullname.strip():
                    st.error("❌ يرجى ملء كافة الحقول الإلزامية المطلوبة.")
                elif len(new_password.strip()) < 6:
                    st.error("❌ كلمة المرور يجب ألا تقل عن 6 أحرف أو أرقام.")
                else:
                    is_all = assigned_sec_choice.startswith(config.SECTOR_ALL)
                    final_sector = None if is_all else assigned_sec_choice
                    ok, msg = auth.create_user(
                        new_username.strip(),
                        new_password.strip(),
                        new_fullname.strip(),
                        new_role,
                        final_sector
                    )
                    if ok:
                        st.success(f"✅ {msg}")
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")

    # ============================================================
    # 2. قائمة وتعديل المستخدمين المسجلين
    # ============================================================
    st.markdown("### 👥 قائمة المستخدمين والصلاحيات والقطاعات المربوطة")
    users = auth.get_all_users()

    if not users:
        st.info("لا يوجد مستخدمون مسجلون حالياً.")
        return

    for u in users:
        u_id = u["id"]
        u_name = u["username"]
        u_full = u["full_name"]
        u_role = u["role"]
        u_sec = u.get("assigned_sector") or "جميع القطاعات"
        role_label = config.ROLES_NAMES.get(u_role, u_role)
        badge_class = {"admin": "badge-admin", "editor": "badge-editor", "viewer": "badge-viewer"}.get(u_role, "badge-viewer")

        with st.container():
            col_info, col_actions = st.columns([3, 1])

            with col_info:
                st.markdown(f"""
                <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; padding:14px 18px; margin-bottom:10px; box-shadow:0 2px 8px rgba(0,0,0,0.03);">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <span style="font-weight:800; font-size:1.05rem; color:#1e293b;">{u_full}</span>
                            <span style="color:#64748b; font-size:0.85rem; margin-right:8px;">(@{u_name})</span>
                        </div>
                        <span class="user-role-badge {badge_class}">{role_label}</span>
                    </div>
                    <div style="margin-top:8px; font-size:0.88rem; color:#475569;">
                        📍 <b>القطاع المخصص:</b> <span style="color:#662D91; font-weight:700;">{u_sec}</span>
                        <span style="color:#94a3b8; font-size:0.75rem; margin-right:15px;">| تاريخ التسجيل: {str(u.get('created_at', ''))[:10]}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col_actions:
                # زر تعديل الصلاحية والقطاع
                with st.expander(f"⚙️ تعديل الحساب", expanded=False):
                    with st.form(f"edit_user_{u_id}"):
                        edit_fullname = st.text_input("الاسم الكامل", value=u_full)
                        edit_role = st.selectbox(
                            "الدور",
                            options=[config.ROLE_EDITOR, config.ROLE_ADMIN, config.ROLE_VIEWER],
                            index=[config.ROLE_EDITOR, config.ROLE_ADMIN, config.ROLE_VIEWER].index(u_role) if u_role in [config.ROLE_EDITOR, config.ROLE_ADMIN, config.ROLE_VIEWER] else 0,
                            format_func=lambda r: config.ROLES_NAMES.get(r, r)
                        )
                        # اختيار القطاع
                        current_sec_idx = sector_choices.index(u_sec) if u_sec in sector_choices else 0
                        edit_sector = st.selectbox("القطاع المخصص", options=sector_choices, index=current_sec_idx)
                        edit_pass = st.text_input("كلمة مرور جديدة (اتركه فارغاً للإبقاء)", type="password")

                        btn_update = st.form_submit_button("💾 تحديث الحساب", type="primary", use_container_width=True)
                        if btn_update:
                            is_all = edit_sector.startswith(config.SECTOR_ALL)
                            new_sec_val = None if is_all else edit_sector
                            ok, msg = auth.update_user(u_id, edit_fullname, edit_role, new_sec_val, edit_pass if edit_pass.strip() else None)
                            if ok:
                                st.success("✅ تم تحديث بيانات المستخدم بنجاح!")
                                st.rerun()
                            else:
                                st.error(f"❌ {msg}")

                # زر حذف المستخدم
                if u_name != user.get("username"):
                    if st.button("🗑️ حذف الحساب", key=f"del_btn_{u_id}", use_container_width=True):
                        auth.delete_user(u_id)
                        st.success(f"تم حذف المستخدم: {u_name}")
                        st.rerun()
                else:
                    st.caption("🔒 حسابك الحالي")
