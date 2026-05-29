import streamlit as st


def apply_global_style(theme):
    page_style = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,600&display=swap');

    :root {{
        --beige-100: #f7efe3;
        --beige-200: #f0e3d3;
        --beige-300: #ead8c1;
        --ink-900: {theme['text']};
        --ink-600: {theme['muted']};
        --accent: {theme['accent']};
        --card: {theme['card']};
        --panel: {theme['panel']};
        --border: {theme['border']};
        --shadow: {theme['shadow']};
    }}

    @keyframes fadeLift {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    @keyframes slowFloat {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-6px); }}
        100% {{ transform: translateY(0px); }}
    }}

    body {{
        background: linear-gradient(180deg, #f0e3d3 0%, #f6ede0 100%);
        color: {theme['text']};
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: 0.01em;
    }}

    section[data-testid="stAppViewContainer"] {{
        position: relative;
        background: radial-gradient(circle at 12% 18%, rgba(215, 177, 126, 0.18), transparent 40%),
                    radial-gradient(circle at 88% 24%, rgba(15, 118, 110, 0.12), transparent 38%),
                    radial-gradient(circle at 18% 78%, rgba(244, 195, 128, 0.2), transparent 45%);
        animation: fadeLift 0.6s ease-out;
    }}

    section[data-testid="stAppViewContainer"]::after {{
        content: "";
        position: absolute;
        right: -80px;
        top: 120px;
        width: 220px;
        height: 220px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(15, 118, 110, 0.18), transparent 65%);
        filter: blur(2px);
        opacity: 0.8;
        animation: slowFloat 8s ease-in-out infinite;
        pointer-events: none;
    }}

    section[data-testid="stAppViewContainer"]::before {{
        content: "";
        position: absolute;
        inset: 0;
        pointer-events: none;
        background-image: repeating-linear-gradient(
            0deg,
            rgba(0, 0, 0, 0.02) 0px,
            rgba(0, 0, 0, 0.02) 1px,
            transparent 1px,
            transparent 3px
        );
        mix-blend-mode: multiply;
        opacity: 0.35;
    }}

    section.main {{
        padding-top: 1rem;
    }}

    section[data-testid="stAppViewContainer"] {{
        padding-top: 0 !important;
    }}

    h1, h2, h3 {{
        font-family: 'Fraunces', serif;
        letter-spacing: -0.01em;
    }}

    .stMarkdown h2, .stMarkdown h3 {{
        color: var(--ink-900);
        position: relative;
    }}

    .stMarkdown h2::after {{
        content: "";
        display: block;
        width: 48px;
        height: 3px;
        margin-top: 8px;
        border-radius: 999px;
        background: linear-gradient(90deg, var(--accent), rgba(15, 118, 110, 0.2));
    }}

    .stMarkdown p {{
        color: var(--ink-600);
        line-height: 1.7;
    }}

    .stMarkdown h1 a,
    .stMarkdown h2 a,
    .stMarkdown h3 a,
    .stMarkdown h4 a,
    .stMarkdown h5 a,
    .stMarkdown h6 a {{
        display: none !important;
    }}

    section[data-testid="stAppViewContainer"] a[href^="#"] {{
        pointer-events: none;
        text-decoration: none;
        color: inherit;
    }}

    .stButton>button {{
        border-radius: 16px;
        padding: 0.85rem 1.6rem;
        font-size: 1rem;
        background: {theme['accent']};
        color: #ffffff;
        border: none;
        box-shadow: 0 14px 30px rgba(15, 23, 42, 0.18);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}

    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 18px 36px rgba(15, 23, 42, 0.2);
    }}

    .stTextArea>div>div>textarea {{
        border-radius: 18px !important;
        border: 1px solid {theme['border']} !important;
        padding: 1rem !important;
        min-height: 150px;
        background: {theme['card']} !important;
        color: {theme['text']} !important;
        box-shadow: inset 0 2px 8px rgba(31, 41, 55, 0.04);
    }}

    .stTextInput>div>div>input {{
        border-radius: 14px !important;
        border: 1px solid var(--border) !important;
        padding: 0.65rem 0.9rem !important;
        background: var(--card) !important;
        color: var(--ink-900) !important;
        box-shadow: inset 0 2px 8px rgba(31, 41, 55, 0.04);
    }}

    .stMultiSelect>div>div>div {{
        border-radius: 16px !important;
        border: 1px solid {theme['border']} !important;
        background: {theme['card']} !important;
        color: {theme['text']} !important;
    }}

    .stMultiSelect div[data-baseweb="tag"] {{
        border-radius: 999px;
        background: rgba(15, 118, 110, 0.12);
        color: var(--accent);
        font-weight: 600;
        padding: 2px 8px;
    }}

    .stAlert {{
        border-radius: 18px !important;
        border: 1px solid var(--border);
        background: var(--card);
        box-shadow: var(--shadow);
    }}

    .stExpander {{
        border-radius: 18px !important;
        border: 1px solid var(--border);
        background: var(--card);
        box-shadow: var(--shadow);
    }}

    .stMetric {{
        background: var(--panel);
        padding: 12px 16px;
        border-radius: 14px;
        border: 1px solid var(--border);
    }}

    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, var(--beige-100), var(--beige-200));
        border-right: 1px solid var(--border);
    }}

    section[data-testid="stSidebar"] > div {{
        display: flex;
        flex-direction: column;
        height: 100%;
    }}

    .sidebar-spacer {{
        flex: 1 1 auto;
    }}

    .sidebar-footer {{
        margin-top: auto;
        padding-top: 12px;
    }}

    section[data-testid="stSidebar"] .stMarkdown h2::after {{
        width: 36px;
    }}

    </style>
    """
    st.markdown(page_style, unsafe_allow_html=True)
