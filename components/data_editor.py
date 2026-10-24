# -*- coding: utf-8 -*-
"""
صفحة تعديل وإدخال البيانات الميدانية (Data Editor Page)
نظام صلاحيات متقدم حسب القطاع (Role-Based Access Control):
- المدير (Admin): وصول كامل لكافة القطاعات، إضافة، تعديل، واستيراد ملفات الإكسيل.
- المحرر (Editor): مقيد بالقطاع المخصص لحسابه فقط؛ لا يمكنه تعديل أو إضافة بيانات قطاع آخر.
- المستعرض (Viewer): استعراض وتصدير للقراءة فقط.
"""
import streamlit as st
import pandas as pd
import io
import database
import auth
import styling
import config


def render_data_editor(user=None):
    user = user or {}
    assigned_sector = user.get("assigned_sector")
    role = user.get("role", config.ROLE_VIEWER)

    # ترويسة الصفحة الرسمية
    styling.render_header(
        "محرر البيانات الميدانية والمزامنة",
        "إضافة وتحديث بيانات المناطق والمشاريع مع نظام صلاحيات صارم ومزامنة فورية مع ملف الإكسيل",
        icon="edit"
    )

    # رسالة الصلاحية الحالية
    if role == config.ROLE_ADMIN:
        st.markdown("""
        <div class="info-pill">
            🛡️ <b>صلاحية مدير النظام:</b> يمكنك إدارة، إضافة، وتعديل بيانات جميع القطاعات والمناطق واستيراد ملفات جديدة.
        </div>
        """, unsafe_allow_html=True)
    elif role == config.ROLE_EDITOR:
        if assigned_sector:
            st.markdown(f"""
            <div class="info-pill">
                🔒 <b>صلاحية محرر مقيد:</b> حسابك مرتبط حصرياً بـ <b>{assigned_sector}</b>. لا يُسمح لك بتعديل أو إضافة أي بيانات خارج هذا القطاع.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="info-pill">
                ✏️ <b>صلاحية محرر عام:</b> يمكنك تعديل وإضافة البيانات لكافة القطاعات.
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-pill">
            👀 <b>صلاحية مستعرض:</b> استعراض وتصدير البيانات للقراءة فقط (غير مسموح بالتعديل أو الإضافة).
        </div>
        """, unsafe_allow_html=True)

    # ============================================================
    # 1. قسم رفع واستيراد ملف الإكسيل (للمدير فقط)
    # ============================================================
    if role == config.ROLE_ADMIN:
        with st.expander("⬆️ استيراد بيانات من ملف Excel جديد (للمدير فقط)"):
            st.caption("ملاحظة: هذا الإجراء يستبدل قاعدة البيانات الحالية ببيانات الملف المرفوع.")
            uploaded = st.file_uploader(
                "ارفع ملف FTTH بنفس هيكل الأعمدة الأصلي",
                type=["xlsx", "xls"],
                key="excel_upload_widget"
            )
            if uploaded:
                col_u1, col_u2 = st.columns([1, 3])
                with col_u1:
                    if st.button("✅ تأكيد الاستيراد والتحديث", type="primary", use_container_width=True):
                        with st.spinner("جارٍ استيراد البيانات وتحديث قاعدة البيانات..."):
                            ok = database.reset_db_from_excel(uploaded)
                        if ok:
                            st.success("✅ تم استيراد البيانات وتحديث قاعدة البيانات بنجاح!")
                            st.rerun()
                        else:
                            st.error("❌ حدث خطأ أثناء الاستيراد.")

    # ============================================================
    # 2. نموذج إضافة سجل جديد (للمدير والمحرر فقط)
    # ============================================================
    if role in [config.ROLE_ADMIN, config.ROLE_EDITOR]:
        with st.expander("➕ إضافة منطقة / سنترال جديد"):
            with st.form("add_record_form", clear_on_submit=True):
                st.markdown("##### بيانات المنطقة / السنترال الجديد")
                col1, col2, col3, col4 = st.columns(4)

                all_sectors = database.get_unique_options("Sector")
                all_seniors = database.get_unique_options("Senior_Sector")

                with col1:
                    if assigned_sector:
                        new_senior = st.text_input("الرئاسة / الإدارة العليا*", value=all_seniors[0] if all_seniors else "رئاسة القاهرة الكبرى")
                    else:
                        new_senior = st.selectbox("الرئاسة / الإدارة العليا*", options=all_seniors if all_seniors else ["رئاسة القاهرة الكبرى"])

                with col2:
                    if assigned_sector:
                        # للمحرر المقيد: الحقل ثابت وغير قابل للتغيير
                        new_sector = st.text_input("القطاع المخصص (مقيد)*", value=assigned_sector, disabled=True)
                    else:
                        # للمدير: يمكنه اختيار أي قطاع موجود أو كتابة جديد
                        new_sector = st.selectbox("القطاع*", options=all_sectors if all_sectors else ["قطاع الجيزة"])

                with col3:
                    new_region = st.text_input("المنطقة / السنترال*", placeholder="مثال: سنترال الدقي")
                with col4:
                    new_type = st.selectbox("نوع الخط", ["Normal", "VIP", "Business"])

                st.markdown("**أرقام الشبكة الجديدة (New FTTH):**")
                nc1, nc2, nc3, nc4, nc5 = st.columns(5)
                with nc1: n_comp = st.number_input("منجز YTD", min_value=0, value=0, step=1, key="add_n_comp")
                with nc2: n_surv = st.number_input("معاينات YTD", min_value=0, value=0, step=1, key="add_n_surv")
                with nc3: n_last7 = st.number_input("آخر 7 أيام", min_value=0, value=0, step=1, key="add_n_last7")
                with nc4: n_yest = st.number_input("الأمس", min_value=0, value=0, step=1, key="add_n_yest")
                with nc5: n_pend = st.number_input("معاينات معلقة", min_value=0, value=0, step=1, key="add_n_pend")

                st.markdown("**أرقام تحويل النحاس إلى فايبر (Migration):**")
                mc1, mc2, mc3, mc4, mc5 = st.columns(5)
                with mc1: m_comp = st.number_input("تحويل منجز YTD", min_value=0, value=0, step=1, key="add_m_comp")
                with mc2: m_surv = st.number_input("معاينات تحويل YTD", min_value=0, value=0, step=1, key="add_m_surv")
                with mc3: m_last7 = st.number_input("تحويل آخر 7 أيام", min_value=0, value=0, step=1, key="add_m_last7")
                with mc4: m_yest = st.number_input("تحويل الأمس", min_value=0, value=0, step=1, key="add_m_yest")
                with mc5: m_pend = st.number_input("معاينات تحويل معلقة", min_value=0, value=0, step=1, key="add_m_pend")

                st.markdown("**المؤشرات والمستهدفات (Flagged):**")
                fl1, fl2, fl3 = st.columns(3)
                with fl1: f_2026 = st.number_input("المستهدف 2026", min_value=0, value=0, step=1, key="add_f_2026")
                with fl2: f_last7 = st.number_input("مؤشر آخر 7 أيام", min_value=0, value=0, step=1, key="add_f_last7")
                with fl3: f_yest = st.number_input("مؤشر الأمس", min_value=0, value=0, step=1, key="add_f_yest")

                submitted = st.form_submit_button("💾 حفظ السجل الجديد في قاعدة البيانات", type="primary", use_container_width=True)
                if submitted:
                    target_sector = assigned_sector if assigned_sector else str(new_sector).strip()
                    if not new_region.strip():
                        st.error("❌ يرجى إدخال اسم المنطقة / السنترال.")
                    elif not target_sector:
                        st.error("❌ يرجى تحديد القطاع.")
                    elif assigned_sector and target_sector != assigned_sector:
                        st.error(f"❌ غير مصرح لك بإضافة سجلات خارج قطاعك المخصص: ({assigned_sector})")
                    else:
                        rec = {
                            "Senior_Sector": str(new_senior).strip(),
                            "Sector": target_sector,
                            "Region": new_region.strip(),
                            "Type": new_type,
                            "New_Completed_YTD": n_comp, "New_Survey_Done_YTD": n_surv,
                            "New_Last_7_Days": n_last7, "New_Yesterday": n_yest,
                            "New_Pending_Survey": n_pend,
                            "Migration_Completed_YTD": m_comp, "Migration_Survey_Done_YTD": m_surv,
                            "Migration_Last_7_Days": m_last7, "Migration_Yesterday": m_yest,
                            "Migration_Pending_Survey": m_pend,
                            "Flagged_2026": f_2026, "Flagged_Last_7_Days": f_last7,
                            "Flagged_Yesterday": f_yest
                        }
                        new_id = database.add_new_record(rec)
                        st.success(f"✅ تم إضافة السجل بنجاح للقطاع ({target_sector}) برقم: {new_id}")
                        st.rerun()

    # ============================================================
    # 3. جدول البيانات التفاعلي (Data Editor / Viewer)
    # ============================================================
    st.markdown("### 📋 جدول السجلات الميدانية")

    col_flt1, col_flt2 = st.columns([2, 1])
    with col_flt1:
        search_term = st.text_input("🔍 بحث سريع في السجلات (المنطقة، السنترال، الرئاسة):", placeholder="اكتب للبحث...")

    # تصفية القطاعات: للمدير قائمة منسدلة، للمحرر مقيد بقطاعه فقط
    if role == config.ROLE_ADMIN:
        with col_flt2:
            all_sec_list = ["جميع القطاعات"] + database.get_unique_options("Sector")
            selected_sector_filter = st.selectbox("تصفية حسب القطاع:", options=all_sec_list)
            effective_sector = None if selected_sector_filter == "جميع القطاعات" else selected_sector_filter
    else:
        effective_sector = assigned_sector

    # تحميل البيانات وفق الصلاحيات
    df = database.load_data(sector=effective_sector, search_term=search_term if search_term else None)

    if df.empty:
        st.warning("⚠️ لا توجد سجلات مطابقة للبحث أو لهذا القطاع.")
        return

    # إحصائية عدد السجلات
    sector_badge = f" | مقيد بقطاع: <b>{effective_sector}</b>" if effective_sector else " | عرض: <b>كافة القطاعات</b>"
    st.markdown(f"""
    <div style="font-size:0.88rem; color:#475569; margin-bottom:12px;">
        📊 إجمالي السجلات المعروضة: <b>{len(df)}</b> منطقة {sector_badge}
    </div>
    """, unsafe_allow_html=True)

    can_edit_table = (role in [config.ROLE_ADMIN, config.ROLE_EDITOR])

    if can_edit_table:
        # إعداد أعمدة الجدول مع قفل عمود القطاع للمحرر
        sector_disabled = bool(assigned_sector)  # غير قابل للتغيير إذا كان المحرر مقيداً

        column_config = {
            "id": st.column_config.NumberColumn("ID", disabled=True, width="small"),
            "Senior_Sector": st.column_config.TextColumn("الرئاسة", width="medium"),
            "Sector": st.column_config.TextColumn("القطاع", disabled=sector_disabled, width="medium"),
            "Region": st.column_config.TextColumn("المنطقة / السنترال", width="medium"),
            "Type": st.column_config.SelectboxColumn("النوع", options=["Normal", "VIP", "Business"]),
            "New_Completed_YTD": st.column_config.NumberColumn("جديد منجز YTD", min_value=0),
            "New_Survey_Done_YTD": st.column_config.NumberColumn("معاينات جديدة YTD", min_value=0),
            "New_Last_7_Days": st.column_config.NumberColumn("جديد آخر 7 أيام", min_value=0),
            "New_Yesterday": st.column_config.NumberColumn("جديد الأمس", min_value=0),
            "New_Pending_Survey": st.column_config.NumberColumn("معاينات جديدة معلقة", min_value=0),
            "Migration_Completed_YTD": st.column_config.NumberColumn("تحويل منجز YTD", min_value=0),
            "Migration_Survey_Done_YTD": st.column_config.NumberColumn("معاينات تحويل YTD", min_value=0),
            "Migration_Last_7_Days": st.column_config.NumberColumn("تحويل آخر 7 أيام", min_value=0),
            "Migration_Yesterday": st.column_config.NumberColumn("تحويل الأمس", min_value=0),
            "Migration_Pending_Survey": st.column_config.NumberColumn("معاينات تحويل معلقة", min_value=0),
            "Flagged_2026": st.column_config.NumberColumn("المستهدف 2026", min_value=0),
            "Flagged_Last_7_Days": st.column_config.NumberColumn("مؤشر آخر 7 أيام", min_value=0),
            "Flagged_Yesterday": st.column_config.NumberColumn("مؤشر الأمس", min_value=0),
            "last_updated": st.column_config.DatetimeColumn("آخر تحديث", disabled=True)
        }

        edited_df = st.data_editor(
            df,
            use_container_width=True,
            hide_index=True,
            num_rows="fixed",
            key="data_editor_grid",
            column_config=column_config
        )

        col_save, col_export = st.columns([1, 1])
        with col_save:
            if st.button("💾 حفظ التعديلات ومزامنة ملف الإكسيل", type="primary", use_container_width=True):
                # التحقق الأمني: إذا كان محرر مقيد، نتأكد أن جميع الصفوف تابعة لقطاعه
                if assigned_sector:
                    tampered = edited_df[edited_df["Sector"] != assigned_sector]
                    if not tampered.empty:
                        st.error(f"❌ خطأ أمني: تم رصد محاولة لتعديل قطاع خارج صلاحيتك ({assigned_sector})!")
                        return

                with st.spinner("جارٍ حفظ التعديلات ومزامنة ملف الإكسيل..."):
                    success = database.update_from_dataframe(edited_df)
                if success:
                    st.success("✅ تم حفظ التعديلات ومزامنة ملف الإكسيل بنجاح!")
                    st.rerun()
                else:
                    st.error("❌ حدث خطأ أثناء الحفظ.")

        with col_export:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                disp_map = {col: config.COLUMN_MAP.get(col, col) for col in edited_df.columns}
                edited_df.rename(columns=disp_map).to_excel(writer, index=False, sheet_name="FTTH Data")
            output.seek(0)
            st.download_button(
                label="📥 تصدير البيانات المعروضة كملف Excel",
                data=output,
                file_name=f"ftth_export_{assigned_sector or 'all'}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    else:
        # عرض فقط للمستعرض
        st.dataframe(df, use_container_width=True, hide_index=True)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            disp_map = {col: config.COLUMN_MAP.get(col, col) for col in df.columns}
            df.rename(columns=disp_map).to_excel(writer, index=False, sheet_name="FTTH Data")
        output.seek(0)
        st.download_button(
            label="📥 تصدير البيانات المعروضة Excel",
            data=output,
            file_name="ftth_export_view.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
