import streamlit as st

def apply_custom_css():
    # Premium Dark Theme CSS (Only supported theme)
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Font overrides */
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
    }
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
    }
    
    /* Core layout background override */
    .stApp {
        background: #0b0f17 !important;
        color: #f8fafc !important;
    }
    
    /* Presentation Cards */
    .kyc-card, div[class*="stBorderedContainer"] {
        background: rgba(22, 31, 48, 0.75) !important;
        backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 14px !important;
        padding: 24px !important;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.3) !important;
        margin-bottom: 20px !important;
        transition: all 0.2s ease !important;
    }
    .kyc-card:hover, div[class*="stBorderedContainer"]:hover {
        border-color: rgba(255, 255, 255, 0.16) !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4) !important;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    
    /* Active nav states */
    div[data-testid="stSidebarNav"] ul {
        padding-top: 10px !important;
    }
    
    /* KPI Metrics custom styling */
    .kpi-value {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #f8fafc !important;
        font-family: 'Outfit', sans-serif !important;
    }
    .kpi-label {
        font-size: 0.85rem !important;
        color: #94a3b8 !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    
    /* Vibrant primary button overrides */
    .stButton>button {
        background: linear-gradient(180deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25) !important;
        transition: all 0.15s ease !important;
        width: 100% !important;
    }
    .stButton>button:hover {
        background: linear-gradient(180deg, #1d4ed8 0%, #1e40af 100%) !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
        transform: translateY(-1px) !important;
    }

    .stButton>button:active {
        transform: translateY(1px) !important;
    }
    
    /* Custom tables and charts container */
    .data-table-container {
        background: #1e293b !important;
        border-radius: 12px !important;
        border: 1px solid #334155 !important;
        padding: 16px !important;
    }
    
    /* Gradient highlight labels */
    .brand-text {
        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    /* Mobile / Android Chrome Responsive Optimizations */
    @media (max-width: 768px) {
        div[class*="stBorderedContainer"], .kyc-card {
            padding: 16px !important;
            margin-bottom: 12px !important;
        }
        .kpi-value {
            font-size: 1.8rem !important;
        }
        /* Prevent viewport auto-zoom on focus on mobile/Android Chrome */
        input, select, textarea {
            font-size: 16px !important;
        }
        /* Maximize content utilization on narrow viewports */
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 1.5rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
    
def kpi_card(label, value, icon="📈"):
    st.markdown(f"""
    <div class="kyc-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span class="kpi-label">{label}</span>
            <span style="font-size: 1.5rem;">{icon}</span>
        </div>
        <div class="kpi-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

def content_card(title, html_content):
    st.markdown(f"""
    <div class="kyc-card">
        <h3 style="margin-top: 0; margin-bottom: 12px; font-weight:600;">{title}</h3>
        <div>{html_content}</div>
    </div>
    """, unsafe_allow_html=True)
