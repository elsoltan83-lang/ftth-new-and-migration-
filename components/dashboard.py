# -*- coding: utf-8 -*-
"""
صفحة لوحة المؤشرات الرئيسية (Dashboard)
تعرض إحصائيات حية ومؤشرات أداء KPI مجسمة ورسم بياني تفاعلي أنيق باستخدام Plotly
مع دعم تصفية القطاعات حسب صلاحية المستخدم تلقائياً.
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import database
import styling
import config


def show_dashboard(current_user=None):
    current_user = current_user or {}
    assigned_sector = current_user.get("assigned_sector")
    role = current_user.get("role", config.ROLE_VIEWER)

    # 1. ترويسة لوحة المؤشرات - رأسية مخصصة
    sector_info = f" — {assigned_sector}" if assigned_sector else " — إجمالي كافة القطاعات"
    st.markdown("""
    <div style=\"display:flex; align-items:center; gap:12px; padding:10px 0;\">
        <img src=\"file:///C:/Users/Sherif/.gemini/antigravity-ide/brain/64029a1e-db73-45a7-a76d-3da46a172ce0/fiber_icon_1792863382466.jpg\" width=\"48\" style=\"filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));\" />
        <div style=\"font-size:1.4rem; font-weight:800; color:#662D91;\">لوحة مؤشرات التحول إلى الفايبر - المصرية للاتصالات WE</div>
    </div>
    """, unsafe_allow_html=True)


    # 2. تحميل البيانات الحقيقية من قاعدة البيانات
    # إذا كان المستخدم مخصص له قطاع، نحمل بيانات قطاعه فقط؛ وإلا نحمل الكل
    df = database.load_data(sector=assigned_sector)

    if df.empty:
        st.warning("⚠️ لا توجد بيانات متاحة حالياً في قاعدة البيانات.")
        return

    # حساب المجاميع الحقيقية بدقة
    total_new_comp = int(df["New_Completed_YTD"].sum())
    total_mig_comp = int(df["Migration_Completed_YTD"].sum())
    total_target_2026 = int(df["Flagged_2026"].sum())
    total_mig_yesterday = int(df["Migration_Yesterday"].sum())

    pct_achieved = round((total_mig_comp / total_target_2026 * 100), 1) if total_target_2026 > 0 else 0

    # 3. عرض كروت المؤشرات KPI Cards بشكل مجسم وألوان الهوية البنفسجية
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">🚀 إجمالي التحويل المنجز (YTD)</div>
                <div class="kpi-value">{total_mig_comp:,}</div>
                <div class="kpi-sub">نسبة الإنجاز من المستهدف: <b>{pct_achieved}%</b></div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">🌐 شبكة فايبر جديدة (YTD)</div>
                <div class="kpi-value">{total_new_comp:,}</div>
                <div class="kpi-sub">خطوط جديدة تم تشغيلها</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">🎯 المستهدف الكلي 2026</div>
                <div class="kpi-value">{total_target_2026:,}</div>
                <div class="kpi-sub">الهدف التراكمي المخطط</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">⚡ إنجاز التحويل بالأمس</div>
                <div class="kpi-value">{total_mig_yesterday:,}</div>
                <div class="kpi-sub">معدل العمليات اليومية المنفذة</div>
            </div>
        """, unsafe_allow_html=True)

    st.write("")

    # 4. تجهيز بيانات الرسم البياني التفاعلي Plotly
    if not assigned_sector:
        # عرض لكافة القطاعات
        chart_title = "📈 معدلات إنجاز التحويل النحاسي حسب القطاع (% من المستهدف)"
        group_col = "Sector"
        x_label = "اسم القطاع"

        # تجميع البيانات حسب القطاع
        grp = df.groupby(group_col).agg({
            "Migration_Completed_YTD": "sum",
            "Flagged_2026": "sum",
            "New_Completed_YTD": "sum",
            "Migration_Yesterday": "sum"
        }).reset_index()

        grp["نسبة الإنجاز %"] = grp.apply(
            lambda r: round((r["Migration_Completed_YTD"] / r["Flagged_2026"] * 100), 1) if r["Flagged_2026"] > 0 else 0,
            axis=1
        )
        grp = grp.sort_values(by="نسبة الإنجاز %", ascending=False)
        chart_data = grp
    else:
        # عرض لمناطق وسنترالات القطاع المخصص للمحرر
        chart_title = f"📈 معدلات إنجاز التحويل لمناطق وسنترالات {assigned_sector}"
        group_col = "Region"
        x_label = "المنطقة / السنترال"

        grp = df.groupby(group_col).agg({
            "Migration_Completed_YTD": "sum",
            "Flagged_2026": "sum",
            "New_Completed_YTD": "sum",
            "Migration_Yesterday": "sum"
        }).reset_index()

        grp["نسبة الإنجاز %"] = grp.apply(
            lambda r: round((r["Migration_Completed_YTD"] / r["Flagged_2026"] * 100), 1) if r["Flagged_2026"] > 0 else 0,
            axis=1
        )
        grp = grp.sort_values(by="نسبة الإنجاز %", ascending=False)
        chart_data = grp

    # 5. رسم بياني محسن وأنيق مع درجات البنفسجي لـ WE وتباين عالي
    st.markdown(f"#### {chart_title}")

    # تسلسل الألوان البنفسجية المتدرجة
    we_purple_palette = [
        '#662D91', '#7835A8', '#8C43B1', '#9E4FC4',
        '#521D7A', '#421663', '#7A2C99', '#8A3AA8',
        '#6B2B94', '#59227C', '#9046B6', '#A154C9'
    ]

    max_val = chart_data["نسبة الإنجاز %"].max() if not chart_data.empty else 100
    y_upper = max(max_val * 1.18, 100)

    fig = px.bar(
        chart_data,
        x=group_col,
        y="نسبة الإنجاز %",
        color=group_col,
        color_discrete_sequence=we_purple_palette,
        text=chart_data["نسبة الإنجاز %"].apply(lambda v: f"{v:.1f}%"),
        custom_data=["Migration_Completed_YTD", "Flagged_2026"]
    )

    # ضبط التسميات والقيم فوق الأعمدة
    fig.update_traces(
        textposition="outside",
        textfont=dict(family="Cairo", size=11, color="#1e293b", weight="bold"),
        hovertemplate="<b>%{x}</b><br>نسبة الإنجاز: %{y:.1f}%<br>تحويل منجز: %{customdata[0]:,} خط<br>المستهدف: %{customdata[1]:,} خط<extra></extra>",
        marker=dict(line=dict(width=1, color="rgba(255,255,255,0.6)"))
    )

    # ضبط الهوامش وتدوير العناوين لمنع أي تداخل نهائياً
    fig.update_layout(
        height=520,
        margin=dict(l=40, r=40, t=50, b=120),
        xaxis=dict(
            tickangle=-25,
            title=dict(
                text=x_label,
                font=dict(family="Cairo", size=14, color="#4A1C6D", weight="bold")
            ),
            tickfont=dict(family="Cairo", size=11, color="#1e293b", weight="bold"),
            automargin=True
        ),
        yaxis=dict(
            range=[0, y_upper],
            title=dict(
                text="نسبة الإنجاز المئوية (%)",
                font=dict(family="Cairo", size=14, color="#4A1C6D", weight="bold")
            ),
            tickfont=dict(family="Cairo", size=11, color="#475569"),
            gridcolor="rgba(226, 232, 240, 0.7)",
            zerolinecolor="rgba(203, 213, 225, 0.8)"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255, 255, 255, 0.6)",
        showlegend=False,
        hoverlabel=dict(
            bgcolor="#4A1C6D",
            font_size=13,
            font_family="Cairo",
            font_color="#ffffff"
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    # 6. تفاصيل إضافية في جدول ملخص سريع
    with st.expander("🔍 استعراض الأرقام التفصيلية للقطاعات"):
        display_summary = chart_data[[group_col, "Migration_Completed_YTD", "Flagged_2026", "New_Completed_YTD", "نسبة الإنجاز %"]].copy()
        display_summary.columns = [x_label, "تحويل منجز YTD", "المستهدف 2026", "فايبر جديد YTD", "نسبة الإنجاز %"]
        st.dataframe(display_summary, use_container_width=True, hide_index=True)