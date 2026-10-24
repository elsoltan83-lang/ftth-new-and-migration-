# -*- coding: utf-8 -*-
"""
styling.py — ملف التنسيقات العامة والهوية البصرية لشركة WE
يحتوي على ألوان الهوية البنفسجية (#662D91)، الخطوط العربية، الكروت المجسمة،
وتحسينات القائمة الجانبية والأزرار.
"""
import streamlit as st

def apply_custom_css():
    """تطبيق أكواد CSS المخصصة لكامل التطبيق"""
    st.markdown("""
    <style>
    /* استيراد خط تجاري أنيق يدعم العربية */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');

    html, body, [class*="css"], .stMarkdown, .stText {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl;
        text-align: right;
    }

    /* ألوان الخلفية العامة للموقع */
    .stApp {
        background-color: #f8f9fc;
    }

    /* ══════════════════════════════════════════════
       تخصيص الشريط الجانبي Sidebar بتصميم عصري وتباين قوي
       ══════════════════════════════════════════════ */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #4A1C6D 0%, #2A0F45 100%) !important;
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.25);
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        color: #f8fafc !important;
        font-family: 'Cairo', sans-serif !important;
    }

    /* أزرار التنقل في القائمة الجانبية - تباين قوي وخط داكن واضح وجريء */
    [data-testid="stSidebar"] div.stButton > button {
        background: #ffffff !important;
        color: #331A4D !important; /* Dark Purple / Bold */
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        font-size: 0.95rem !important;
        padding: 10px 16px !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15) !important;
        transition: all 0.25s ease-in-out !important;
        margin-bottom: 6px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
    }

    [data-testid="stSidebar"] div.stButton > button p,
    [data-testid="stSidebar"] div.stButton > button span,
    [data-testid="stSidebar"] div.stButton > button div {
        color: #331A4D !important;
        font-weight: 800 !important;
        font-size: 0.95rem !important;
    }

    /* تأثير المرور فوق الأزرار */
    [data-testid="stSidebar"] div.stButton > button:hover {
        background: #F3E8FF !important; /* Light Lavender */
        color: #662D91 !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.25) !important;
        border-color: #A855F7 !important;
    }

    [data-testid="stSidebar"] div.stButton > button:hover p,
    [data-testid="stSidebar"] div.stButton > button:hover span {
        color: #662D91 !important;
    }

    /* الزر النشط حالياً في القائمة الجانبية */
    [data-testid="stSidebar"] div.stButton > button[kind="primary"],
    [data-testid="stSidebar"] div.stButton > button[data-testid="baseButton-primary"] {
        background: linear-gradient(90deg, #F9F5FF 0%, #FFFFFF 100%) !important;
        color: #662D91 !important;
        border: 2px solid #A855F7 !important;
        box-shadow: 0 4px 18px rgba(168, 85, 247, 0.4) !important;
    }

    [data-testid="stSidebar"] div.stButton > button[kind="primary"] p,
    [data-testid="stSidebar"] div.stButton > button[kind="primary"] span,
    [data-testid="stSidebar"] div.stButton > button[data-testid="baseButton-primary"] p,
    [data-testid="stSidebar"] div.stButton > button[data-testid="baseButton-primary"] span {
        color: #662D91 !important;
        font-weight: 900 !important;
    }

    /* بطاقة المستخدم في الشريط الجانبي */
    .user-status-card {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 14px;
        padding: 14px 16px;
        margin-bottom: 15px;
        backdrop-filter: blur(8px);
    }

    /* شارات الصلاحيات */
    .user-role-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 700;
        margin-top: 4px;
    }
    .badge-admin {
        background: linear-gradient(135deg, #a855f7, #662d91);
        color: #ffffff !important;
    }
    .badge-editor {
        background: linear-gradient(135deg, #0ea5e9, #0284c7);
        color: #ffffff !important;
    }
    .badge-viewer {
        background: linear-gradient(135deg, #64748b, #475569);
        color: #ffffff !important;
    }

    /* ══════════════════════════════════════════════
       كروت إحصائية مجسمة 3D Cards
       ══════════════════════════════════════════════ */
    .kpi-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 10px 25px rgba(102, 45, 145, 0.08), 0 2px 6px rgba(0,0,0,0.04);
        border-right: 6px solid #662D91;
        transition: all 0.3s ease-in-out;
        margin-bottom: 15px;
    }

    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 16px 32px rgba(102, 45, 145, 0.16);
    }

    .kpi-title {
        font-size: 0.95rem;
        color: #64748b !important;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        color: #662D91 !important;
        line-height: 1.2;
    }

    .kpi-sub {
        font-size: 0.8rem;
        color: #94a3b8;
        margin-top: 4px;
    }

    /* بطاقة تنبيه/معلومات */
    .info-pill {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-right: 4px solid #662D91;
        border-radius: 10px;
        padding: 12px 18px;
        margin: 14px 0;
        font-weight: 600;
        color: #334155;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    /* أزرار المحتوى الرئيسي */
    .stApp div.stButton > button {
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        padding: 8px 18px !important;
        transition: all 0.25s ease !important;
    }

    /* خانات الإدخال والتصفية */
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stNumberInput input {
        border-radius: 8px !important;
        border: 1px solid #cbd5e1 !important;
        color: #1e293b !important;
        direction: rtl !important;
        text-align: right !important;
    }

    /* الجداول الفاخرة */
    .stDataFrame, [data-testid="stDataEditor"] {
        border-radius: 14px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 18px rgba(0,0,0,0.06) !important;
        border: 1px solid #e2e8f0 !important;
    }
    </style>
    """, unsafe_allow_html=True)


def render_header(title: str, subtitle: str = "", icon: str = ""):
    """عرض ترويسة الصفحة الرسمية بهوية WE البنفسجية الأنيقة"""
    icon_map = {
        "dashboard": "📊",
        "edit": "✏️",
        "users-cog": "👥",
        "shield": "🛡️",
        "network": "🌐"
    }
    icon_emoji = icon_map.get(icon, "🟣")

    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #662D91 0%, #8C43B1 100%); padding: 22px 28px; border-radius: 16px; margin-bottom: 25px; box-shadow: 0 8px 24px rgba(102, 45, 145, 0.2); color: white;">
        <h2 style="margin: 0; color: #ffffff !important; font-weight: 800; font-size: 1.65rem; display: flex; align-items: center; gap: 10px;">
            <span>{icon_emoji}</span>
            <span>{title}</span>
        </h2>
        {f'<p style="margin: 6px 0 0 0; color: rgba(255,255,255,0.9) !important; font-size: 0.95rem; font-weight: 500;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)