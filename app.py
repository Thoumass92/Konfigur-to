import streamlit as st
import pandas as pd
import math

# --- BARVY ---
WILO_GREEN = "#21B6A8"
WILO_GREEN_DARK = "#168e84"
WILO_GREEN_LIGHT = "#8be6da"
WILO_GREEN_HOVER = "#159d93"
BUTTON_TEXT_COLOR = "#fff"
BORDER_RADIUS = "8px"

WILO_LOGO_URL = "https://scontent-fra3-1.xx.fbcdn.net/v/t39.30808-6/312307533_996663857947185_6220530952015731225_n.png?_nc_cat=108&ccb=1-7&_nc_sid=6ee11a&_nc_ohc=83_eOJu59pQQ7kNvwF1FuJO&_nc_oc=AdneoM6Ax72YEQxMPuPNAht6eEjBBfllTwCT3yezrDZ-QGObbuWxfAnWIddVn6dLfSs&_nc_zt=23&_nc_ht=scontent-fra3-1.xx&_nc_gid=Yvtk47THe4NhpdkBwjbyjA&oh=00_AfTEkPpnVzUkus59W8aK0U_bAIazC2CjjpJAEQDqjSBFcg&oe=68916816"

# --- VLASTNÍ CSS ---
st.markdown(f"""
    <style>
    .stButton button {{
        background-color: {WILO_GREEN_DARK};
        color: {BUTTON_TEXT_COLOR};
        border-radius: {BORDER_RADIUS};
        padding: 0.5em 2.2em;
        font-size: 1.1em;
        font-weight: bold;
        border: none;
        transition: background 0.3s;
    }}
    .stButton button:hover {{
        background-color: {WILO_GREEN_HOVER};
        color: white;
    }}
    .shop-btn {{
        background-color: {WILO_GREEN_LIGHT};
        color: #004643;
        border: none;
        border-radius: {BORDER_RADIUS};
        padding: 0.45em 2em;
        font-size: 1em;
        font-weight: 600;
        margin-bottom: 8px;
        transition: background 0.3s;
        text-decoration: none;
        display: inline-block;
    }}
    .shop-btn:hover {{
        background-color: {WILO_GREEN};
        color: white;
    }}
    </style>
""", unsafe_allow_html=True)

def wilo_header():
    st.markdown(
        f"""
        <div style='background-color:{WILO_GREEN};padding:1.2em 2em;display:flex;align-items:center;border-radius: 0 0 16px 16px;margin-bottom:2em;'>
            <img src="{WILO_LOGO_URL}" style="height:48px;margin-right:24px;">
            <span style='color:white; font-size:2.3em; font-weight:bold;'>Výběr vhodného čerpadla</span>
        </div>
        """,
        unsafe_allow_html=True
    )

wilo_header()

# --- DATA BLOKY ---

DATA_TWI5 = [
    [75, 1.5, "TWI 5 308"],
    [70, 1.5, "TWI 5 308"], [70, 2.0, "TWI 5 308"],
    [65, 1.5, "TWI 5 307"], [65, 2.0, "TWI 5 308"], [65, 2.5, "TWI 5 308"],
    [60, 1.5, "TWI 5 307"], [60, 2.0, "TWI 5 307"], [60, 2.5, "TWI 5 308"], [60, 3.0, "TWI 5 308"],
    [55, 1.5, "TWI 5 306"], [55, 2.0, "TWI 5 307"], [55, 2.5, "TWI 5 307"], [55, 3.0, "TWI 5 308"], [55, 3.5, "TWI 5 506"],
    [50, 1.5, "TWI 5 306"], [50, 2.0, "TWI 5 306"], [50, 2.5, "TWI 5 307"], [50, 3.0, "TWI 5 307"], [50, 3.5, "TWI 5 308"], [50, 4.0, "TWI 5 506"],
    [45, 1.5, "TWI 5 305"], [45, 2.0, "TWI 5 306"], [45, 2.5, "TWI 5 306"], [45, 3.0, "TWI 5 307"], [45, 3.5, "TWI 5 307"], [45, 4.0, "TWI 5 308"], [45, 4.5, "TWI 5 506"], [45, 5.0, "TWI 5 506"],
    [40, 1.5, "TWI 5 305"], [40, 2.0, "TWI 5 305"], [40, 2.5, "TWI 5 305"], [40, 3.0, "TWI 5 306"], [40, 3.5, "TWI 5 307"], [40, 4.0, "TWI 5 308"], [40, 4.5, "TWI 5 505"], [40, 5.0, "TWI 5 505"], [40, 6.0, "TWI 5 506"], [40, 7.0, "TWI 5 506"],
    [35, 1.5, "TWI 5 304"], [35, 2.0, "TWI 5 304"], [35, 2.5, "TWI 5 305"], [35, 3.0, "TWI 5 305"], [35, 3.5, "TWI 5 306"], [35, 4.0, "TWI 5 307"], [35, 4.5, "TWI 5 308"], [35, 5.0, "TWI 5 505"], [35, 6.0, "TWI 5 505"], [35, 7.0, "TWI 5 506"], [35, 8.0, "TWI 5 904"],
    [30, 1.5, "TWI 5 304"], [30, 2.0, "TWI 5 304"], [30, 2.5, "TWI 5 304"], [30, 3.0, "TWI 5 304"], [30, 3.5, "TWI 5 305"], [30, 4.0, "TWI 5 306"], [30, 4.5, "TWI 5 307"], [30, 5.0, "TWI 5 504"], [30, 6.0, "TWI 5 505"], [30, 7.0, "TWI 5 903"], [30, 8.0, "TWI 5 904"], [30, 9.5, "TWI 5 904"],
    [25, 1.5, "TWI 5 304"], [25, 2.0, "TWI 5 304"], [25, 2.5, "TWI 5 304"], [25, 3.0, "TWI 5 304"], [25, 3.5, "TWI 5 304"], [25, 4.0, "TWI 5 305"], [25, 4.5, "TWI 5 306"], [25, 5.0, "TWI 5 308"], [25, 6.0, "TWI 5 504"], [25, 7.0, "TWI 5 505"], [25, 8.0, "TWI 5 903"], [25, 9.5, "TWI 5 903"], [25, 11.0, "TWI 5 904"],
    [20, 1.5, "TWI 5 304"], [20, 2.0, "TWI 5 304"], [20, 2.5, "TWI 5 304"], [20, 3.0, "TWI 5 304"], [20, 3.5, "TWI 5 304"], [20, 4.0, "TWI 5 304"], [20, 4.5, "TWI 5 305"], [20, 5.0, "TWI 5 307"], [20, 6.0, "TWI 5 504"], [20, 7.0, "TWI 5 504"], [20, 8.0, "TWI 5 903"], [20, 9.5, "TWI 5 903"], [20, 11.0, "TWI 5 903"], [20, 12.5, "TWI 5 904"],
    [15, 1.5, "TWI 5 304"], [15, 2.0, "TWI 5 304"], [15, 2.5, "TWI 5 304"], [15, 3.0, "TWI 5 304"], [15, 3.5, "TWI 5 304"], [15, 4.0, "TWI 5 304"], [15, 4.5, "TWI 5 304"], [15, 5.0, "TWI 5 306"], [15, 6.0, "TWI 5 504"], [15, 7.0, "TWI 5 504"], [15, 8.0, "TWI 5 903"], [15, 9.5, "TWI 5 903"], [15, 11.0, "TWI 5 903"], [15, 12.5, "TWI 5 903"], [15, 14.0, "TWI 5 904"],
]

DATA_TWU4 = [
    [200, 2.5, "TWU 4-0435-C"], [200, 3, "TWU 4-0444-C"], [200, 3.5, "TWU 4-0448-C"], [200, 4, "TWU 4-0448-C"],
    [190, 2.5, "TWU 4-0435-C"], [190, 3, "TWU 4-0444-C"], [190, 3.5, "TWU 4-0444-C"], [190, 4, "TWU 4-0448-C"], [190, 4.5, "TWU 4.08-34"], [190, 5, "TWU 4.08-34"],
    [180, 2.5, "TWU 4-0435-C"], [180, 3, "TWU 4-0435-C"], [180, 3.5, "TWU 4-0444-C"], [180, 4, "TWU 4-0448-C"], [180, 4.5, "TWU 4.08-34"], [180, 5, "TWU 4.08-34"], [180, 6, "TWU 4.08-34"],
    [170, 2.5, "TWU 4-0435-C"], [170, 3, "TWU 4-0435-C"], [170, 3.5, "TWU 4.08-29"], [170, 4, "TWU 4-0444-C"], [170, 4.5, "TWU 4-0448-C"], [170, 5, "TWU 4.08-34"], [170, 6, "TWU 4.08-34"],
    [160, 2.5, "TWU 4-0435-C"], [160, 3, "TWU 4-0435-C"], [160, 3.5, "TWU 4.08-29"], [160, 4, "TWU 4-0444-C"], [160, 4.5, "TWU 4.08-29"], [160, 5, "TWU 4.08-29"], [160, 6, "TWU 4.08-34"], [160, 7, "TWU 4.08-34"],
    [150, 2.5, "TWU 4-0435-C"], [150, 3, "TWU 4-0435-C"], [150, 3.5, "TWU 4-0435-C"], [150, 4, "TWU 4.08-29"], [150, 4.5, "TWU 4-0444-C"], [150, 5, "TWU 4.08-29"], [150, 6, "TWU 4.08-29"], [150, 7, "TWU 4.08-34"], [150, 8, "TWU 4.08-34"],
    [140, 2.5, "TWU 4-0427-C"], [140, 3, "TWU 4-0435-C"], [140, 3.5, "TWU 4-0435-C"], [140, 4, "TWU 4.08-29"], [140, 4.5, "TWU 4-0444-C"], [140, 5, "TWU 4.08-29"], [140, 6, "TWU 4.08-29"], [140, 7, "TWU 4.08-29"], [140, 8, "TWU 4.08-34"],
    [130, 2.5, "TWU 4-0427-C"], [130, 3, "TWU 4-0427-C"], [130, 3.5, "TWU 4-0435-C"], [130, 4, "TWU 4-0435-C"], [130, 4.5, "TWU 4.08-29"], [130, 5, "TWU 4.08-29"], [130, 6, "TWU 4.08-29"], [130, 7, "TWU 4.08-29"], [130, 8, "TWU 4.08-34"], [130, 9, "TWU 4.08-34"],
    [120, 2.5, "TWU 4-0427-C"], [120, 3, "TWU 4-0427-C"], [120, 3.5, "TWU 4-0427-C"], [120, 4, "TWU 4-0435-C"], [120, 4.5, "TWU 4.08-29"], [120, 5, "TWU 4.08-29"], [120, 6, "TWU 4.08-29"], [120, 7, "TWU 4.08-29"], [120, 8, "TWU 4.08-29"], [120, 9, "TWU 4.08-34"],
    [110, 2.5, "TWU 4-0418-C"], [110, 3, "TWU 4-0427-C"], [110, 3.5, "TWU 4-0427-C"], [110, 4, "TWU 4-0435-C"], [110, 4.5, "TWU 4.08-21"], [110, 5, "TWU 4.08-21"], [110, 6, "TWU 4.08-21"], [110, 7, "TWU 4.08-29"], [110, 8, "TWU 4.08-29"], [110, 9, "TWU 4.08-34"],
    [100, 2.5, "TWU 4-0418-C"], [100, 3, "TWU 4-0418-C"], [100, 3.5, "TWU 4-0427-C"], [100, 4, "TWU 4-0427-C"], [100, 4.5, "TWU 4.08-21"], [100, 5, "TWU 4.08-21"], [100, 6, "TWU 4.08-21"], [100, 7, "TWU 4.08-21"], [100, 8, "TWU 4.08-29"], [100, 9, "TWU 4.08-29"], [100, 10, "TWU 4.08-34"],
    [90, 2.5, "TWU 4-0418-C"], [90, 3, "TWU 4-0418-C"], [90, 3.5, "TWU 4-0418-C"], [90, 4, "TWU 4-0427-C"], [90, 4.5, "TWU 4-0435-C"], [90, 5, "TWU 4.08-21"], [90, 6, "TWU 4.08-21"], [90, 7, "TWU 4.08-21"], [90, 8, "TWU 4.08-21"], [90, 9, "TWU 4.08-29"], [90, 10, "TWU 4.08-34"],
    [80, 2.5, "TWU 4-0414-C"], [80, 3, "TWU 4-0418-C"], [80, 3.5, "TWU 4-0418-C"], [80, 4, "TWU 4-0418-C"], [80, 4.5, "TWU 4.08-15"], [80, 5, "TWU 4.08-15"], [80, 6, "TWU 4.08-21"], [80, 7, "TWU 4.08-21"], [80, 8, "TWU 4.08-21"], [80, 9, "TWU 4.08-29"], [80, 10, "TWU 4.08-29"],
    [70, 2.5, "TWU 4-0414-C"], [70, 3, "TWU 4-0414-C"], [70, 3.5, "TWU 4-0414-C"], [70, 4, "TWU 4-0418-C"], [70, 4.5, "TWU 4-0418-C"], [70, 5, "TWU 4.08-15"], [70, 6, "TWU 4.08-15"], [70, 7, "TWU 4.08-15"], [70, 8, "TWU 4.08-21"], [70, 9, "TWU 4.08-21"], [70, 10, "TWU 4.08-29"], [70, 11, "TWU 4.08-34"],
    [60, 2.5, "TWU 4-0414-C"], [60, 3, "TWU 4-0414-C"], [60, 3.5, "TWU 4-0414-C"], [60, 4, "TWU 4-0414-C"], [60, 4.5, "TWU 4-0418-C"], [60, 5, "TWU 4.08-15"], [60, 6, "TWU 4.08-15"], [60, 7, "TWU 4.08-15"], [60, 8, "TWU 4.08-15"], [60, 9, "TWU 4.08-21"], [60, 10, "TWU 4.08-29"], [60, 11, "TWU 4.08-29"],
    [50, 2.5, "TWU 4-0409-C"], [50, 3, "TWU 4-0409-C"], [50, 3.5, "TWU 4-0414-C"], [50, 4, "TWU 4-0414-C"], [50, 4.5, "TWU 4-0414-C"], [50, 5, "TWU 4-0418-C"], [50, 6, "TWU 4-0418-C"], [50, 7, "TWU 4.08-15"], [50, 8, "TWU 4.08-15"], [50, 9, "TWU 4.08-15"], [50, 10, "TWU 4.08-21"], [50, 11, "TWU 4.08-29"],
    [40, 2.5, "TWU 4-0409-C"], [40, 3, "TWU 4-0409-C"], [40, 3.5, "TWU 4-0409-C"], [40, 4, "TWU 4-0409-C"], [40, 4.5, "TWU 4-0414-C"], [40, 5, "TWU 4-0414-C"], [40, 6, "TWU 4-0418-C"], [40, 7, "TWU 4.08-10"], [40, 8, "TWU 4.08-10"], [40, 9, "TWU 4.08-15"], [40, 10, "TWU 4.08-15"], [40, 11, "TWU 4.08-21"], [40, 12, "TWU 4.08-34"],
    [30, 2.5, "TWU 4-0409-C"], [30, 3, "TWU 4-0409-C"], [30, 3.5, "TWU 4-0409-C"], [30, 4, "TWU 4-0409-C"], [30, 4.5, "TWU 4-0409-C"], [30, 5, "TWU 4-0414-C"], [30, 6, "TWU 4-0414-C"], [30, 7, "TWU 4.08-07"], [30, 8, "TWU 4.08-07"], [30, 9, "TWU 4.08-10"], [30, 10, "TWU 4.08-15"], [30, 11, "TWU 4.08-15"], [30, 12, "TWU 4.08-29"],
    [20, 2.5, "TWU 4-0409-C"], [20, 3, "TWU 4-0409-C"], [20, 3.5, "TWU 4-0409-C"], [20, 4.5, "TWU 4-0409-C"], [20, 5, "TWU 4-0409-C"], [20, 6, "TWU 4.08-07"], [20, 7, "TWU 4.08-07"], [20, 8, "TWU 4.08-07"], [20, 9, "TWU 4.08-07"], [20, 10, "TWU 4.08-10"], [20, 11, "TWU 4.08-10"], [20, 12, "TWU 4.08-21"],
    [10, 3, "TWU 4-0409-C"], [10, 3.5, "TWU 4-0409-C"], [10, 4.5, "TWU 4-0409-C"], [10, 5, "TWU 4-0409-C"], [10, 6, "TWU 4.08-07"], [10, 7, "TWU 4.08-07"], [10, 8, "TWU 4.08-07"], [10, 9, "TWU 4.08-07"], [10, 10, "TWU 4.08-07"]
]

DATA_TWU3 = [
    [70, 1.0, "TWU 3-0707"],
    [65, 1.0, "TWU 3-0607"],
    [60, 1.0, "TWU 3-0606"], [60, 1.5, "TWU 3-0610"],
    [55, 1.0, "TWU 3-0606"], [55, 1.5, "TWU 3-0610"],
    [50, 1.0, "TWU 3-0605"], [50, 1.5, "TWU 3-0608"], [50, 2.0, "TWU 3-0610"],
    [45, 1.0, "TWU 3-0605"], [45, 1.5, "TWU 3-0608"], [45, 2.0, "TWU 3-0610"],
    [40, 1.0, "TWU 3-0604"], [40, 1.5, "TWU 3-0607"], [40, 2.0, "TWU 3-0610"],
    [35, 1.0, "TWU 3-0604"], [35, 1.5, "TWU 3-0607"], [35, 2.0, "TWU 3-0610"],
    [30, 1.0, "TWU 3-0604"], [30, 1.5, "TWU 3-0607"], [30, 2.0, "TWU 3-0609"],
    [25, 1.0, "TWU 3-0603"], [25, 1.5, "TWU 3-0605"], [25, 2.0, "TWU 3-0608"],
    [20, 1.0, "TWU 3-0603"], [20, 1.5, "TWU 3-0605"], [20, 2.0, "TWU 3-0608"],
    [15, 1.0, "TWU 3-0603"], [15, 1.5, "TWU 3-0605"], [15, 2.0, "TWU 3-0607"],
]

DATA_HWJ = [
    {"model": "HWJ 201 EM 20 l - M", "Q_max": 2.5, "H_max": 42},
    {"model": "HWJ 301 EM 60 l - M", "Q_max": 4.5, "H_max": 45},
    {"model": "HWJ 401 EM 60 l - M", "Q_max": 4.8, "H_max": 50},
]

# --- Seznam obchodů pro HWJ vodárny ---
HWJ_SHOPS = [
    {"name": "Bola.cz", "url": "https://www.bola.cz/vyhledat-produkt/HWJ"},
    {"name": "Pumpa.eu", "url": "https://www.pumpa.eu/cs/wilo-jet-hwj-automaticke-samonasavaci-domaci-vodarny/"},
    {"name": "Kamody.cz", "url": "https://www.kamody.cz/index.php?route=product/search&filter_name=HWJ"},
]

# --- Kompletní příslušenství podle tabulky
# Pro přehlednosti uvádím jen základní část, ale můžeš ji libovolně rozšířit. Stačí přidat další položky podle potřeby.
TWU4_ACCESSORIES = {
    # EM - jednofázové
    "TWU 4-0409-C EM": {
        "řízení": "Wilo-HiControl 1-EK (4190895)",
        "expanze": "",
        "kabel": {
            20: ("4x1,5 mm²", "2867011"),
            30: ("4x1,5 mm²", "2867012"),
            40: ("4x1,5 mm²", "2860713"),
            50: ("4x2,5 mm²", "2867040"),
        },
        "napojení": "2867014"
    },
    "TWU 4-0414-C EM": {
        "řízení": "Wilo-HiControl 1-EK (4190895)",
        "expanze": "",
        "kabel": {
            20: ("4x1,5 mm²", "2867011"),
            30: ("4x1,5 mm²", "2867012"),
            40: ("4x1,5 mm²", "2860713"),
            50: ("4x2,5 mm²", "2867040"),
        },
        "napojení": "2867014"
    },
    "TWU 4-0418-C EM": {
        "řízení": "DOMESTIC CONTROL 1M/3-S (2865994)",
        "expanze": "SET 50 (2865134)",
        "kabel": {
            20: ("4x1,5 mm²", "2867011"),
            30: ("4x1,5 mm²", "2867012"),
            40: ("4x2,5 mm²", "2867039"),
            50: ("4x2,5 mm²", "2867040"),
        },
        "napojení": "2867014"
    },
    "TWU 4-0427-C EM": {
        "řízení": "DOMESTIC CONTROL 1M/3-S (2865994)",
        "expanze": "SET 50 (2865134)",
        "kabel": {
            20: ("4x1,5 mm²", "2867011"),
            30: ("4x2,5 mm²", "2867038"),
            40: ("4x2,5 mm²", "2867039"),
        },
        "napojení": "2867014"
    },
    "TWU 4.08-07-EM-C": {
        "řízení": "Wilo-HiControl 1-EK (4190895)",
        "expanze": "",
        "kabel": {
            20: ("4x1,5 mm²", "2867011"),
            30: ("4x1,5 mm²", "2867012"),
            40: ("4x1,5 mm²", "2860713"),
            50: ("4x2,5 mm²", "2867040"),
        },
        "napojení": "2867014"
    },
    "TWU 4.08-10-EM-C": {
        "řízení": "DOMESTIC CONTROL 1M/3-S (2865994)",
        "expanze": "SET 50",
        "kabel": {
            20: ("4x1,5 mm²", "2867011"),
            30: ("4x1,5 mm²", "2867012"),
            40: ("4x2,5 mm²", "2867039"),
            50: ("4x2,5 mm²", "2867040"),
        },
        "napojení": "2867014"
    },
    "TWU 4.08-15-EM-C": {
        "řízení": "DOMESTIC CONTROL 1M/3-S (2865994)",
        "expanze": "SET 50 (2865134)",
        "kabel": {
            20: ("4x1,5 mm²", "2867011"),
            30: ("4x2,5 mm²", "2867038"),
            40: ("4x2,5 mm²", "2867039"),
        },
        "napojení": "2867014"
    },
    # DM - třífázové
    "TWU 4-0409-C DM": {
        "řízení": "DOMESTIC CONTROL 1T/10-S (2865996)",
        "expanze": "SET 50 (2865134)",
        "kabel": {
            20: ("4x1,5 mm²", "2867011"),
            30: ("4x1,5 mm²", "2867012"),
            40: ("4x1,5 mm²", "2860713"),
            50: ("4x1,5 mm²", "2867036"),
        },
        "napojení": "2867014"
    },
    "TWU 4-0414-C DM": {
        "řízení": "DOMESTIC CONTROL 1T/10-S (2865996)",
        "expanze": "SET 50 (2865134)",
        "kabel": {
            20: ("4x1,5 mm²", "2867011"),
            30: ("4x1,5 mm²", "2867012"),
            40: ("4x1,5 mm²", "2860713"),
            50: ("4x1,5 mm²", "2867036"),
        },
        "napojení": "2867014"
    },
    "TWU 4-0418-C DM": {
        "řízení": "DOMESTIC CONTROL 1T/10-S (2865996)",
        "expanze": "SET 50 (2865134)",
        "kabel": {
            20: ("4x1,5 mm²", "2867011"),
            30: ("4x1,5 mm²", "2867012"),
            40: ("4x1,5 mm²", "2860713"),
            50: ("4x1,5 mm²", "2867036"),
        },
        "napojení": "2867014"
    },
    "TWU 4-0427-C DM": {
        "řízení": "DOMESTIC CONTROL 1T/10-S (2865996)",
        "expanze": "SET 50 (2865134)",
        "kabel": {
            20: ("4x1,5 mm²", "2867011"),
            30: ("4x1,5 mm²", "2867012"),
            40: ("4x1,5 mm²", "2860713"),
            50: ("4x1,5 mm²", "2867036"),
        },
        "napojení": "2867014"
    },
    "TWU 4-0435-C DM": {
        "řízení": "DOMESTIC CONTROL 1T/10-S (2865996)",
        "expanze": "SET 50 (2865134)",
        "kabel": {
            20: ("4x1,5 mm²", "2867011"),
            30: ("4x1,5 mm²", "2867012"),
            40: ("4x1,5 mm²", "2860713"),
            50: ("4x1,5 mm²", "2867036"),
        },
        "napojení": "2867014"
    },
    "TWU 4-0444-C DM": {
        "řízení": "DOMESTIC CONTROL 1T/10-S (2865996)",
        "expanze": "SET 50 (2865134)",
        "kabel": {
            20: ("4x1,5 mm²", "2867011"),
            30: ("4x1,5 mm²", "2867012"),
            40: ("4x1,5 mm²", "2860713"),
            50: ("4x1,5 mm²", "2867036"),
        },
        "napojení": "2867014"
    },
    "TWU 4-0448-C DM": {
        "řízení": "DOMESTIC CONTROL 1T/10-S (2865996)",
        "expanze": "SET 50 (2865134)",
        "kabel": {
            20: ("4x1,5 mm²", "2867011"),
            30: ("4x1,5 mm²", "2867012"),
            40: ("4x1,5 mm²", "2860713"),
            50: ("4x1,5 mm²", "2867036"),
        },
        "napojení": "2867014"
    },
    "TWU 4.08-07-DM-C": {
        "řízení": "DOMESTIC CONTROL 1T/10-S (2865996)",
        "expanze": "SET 50 (2865134)",
        "kabel": {
            20: ("4x1,5 mm²", "2867011"),
            30: ("4x1,5 mm²", "2867012"),
            40: ("4x1,5 mm²", "2860713"),
            50: ("4x1,5 mm²", "2867036"),
        },
        "napojení": "2867014"
    },
    "TWU 4.08-10-DM-C": {
        "řízení": "DOMESTIC CONTROL 1T/10-S (2865996)",
        "expanze": "SET 50 (2865134)",
        "kabel": {
            20: ("4x1,5 mm²", "2867011"),
            30: ("4x1,5 mm²", "2867012"),
            40: ("4x1,5 mm²", "2860713"),
            50: ("4x1,5 mm²", "2867036"),
        },
        "napojení": "2867014"
    },
    "TWU 4.08-15-DM-C": {
        "řízení": "DOMESTIC CONTROL 1T/10-S (2865996)",
        "expanze": "SET 50 (2865134)",
        "kabel": {
            20: ("4x1,5 mm²", "2867011"),
            30: ("4x1,5 mm²", "2867012"),
            40: ("4x1,5 mm²", "2860713"),
            50: ("4x1,5 mm²", "2867036"),
        },
        "napojení": "2867014"
    },
    "TWU 4.08-21-DM-C": {
        "řízení": "DOMESTIC CONTROL 1T/10-S (2865996)",
        "expanze": "SET 50 (2865134)",
        "kabel": {
            20: ("4x1,5 mm²", "2867011"),
            30: ("4x1,5 mm²", "2867012"),
            40: ("4x1,5 mm²", "2860713"),
            50: ("4x1,5 mm²", "2867036"),
        },
        "napojení": "2867014"
    },
    "TWU 4.08-29-DM-C": {
        "řízení": "DOMESTIC CONTROL 1T/10-S (2865996)",
        "expanze": "SET 50 (2865134)",
        "kabel": {
            20: ("4x1,5 mm²", "2867011"),
            30: ("4x1,5 mm²", "2867012"),
            40: ("4x1,5 mm²", "2860713"),
            50: ("4x1,5 mm²", "2867036"),
        },
        "napojení": "2867014"
    },
    "TWU 4.08-34-DM-C": {
        "řízení": "DOMESTIC CONTROL 1T/10-S (2865996)",
        "expanze": "SET 50 (2865134)",
        "kabel": {
            20: ("4x1,5 mm²", "2867011"),
            30: ("4x1,5 mm²", "2867012"),
            40: ("4x1,5 mm²", "2860713"),
            50: ("4x1,5 mm²", "2867036"),
        },
        "napojení": "2867014"
    },
    "TWU 4.08-39-DM-C": {
        "řízení": "DOMESTIC CONTROL 1T/10-S (2865996)",
        "expanze": "SET 50 (2865134)",
        "kabel": {
            20: ("4x1,5 mm²", "2867011"),
            30: ("4x1,5 mm²", "2867012"),
            40: ("4x1,5 mm²", "2860713"),
            50: ("4x1,5 mm²", "2867036"),
        },
        "napojení": "2867014"
    },
    "TWU 4.08-45-DM-C": {
        "řízení": "DOMESTIC CONTROL 1T/10-S (2865996)",
        "expanze": "SET 50 (2865134)",
        "kabel": {
            20: ("4x1,5 mm²", "2867011"),
            30: ("4x1,5 mm²", "2867012"),
            40: ("4x1,5 mm²", "2860713"),
            50: ("4x2,5 mm²", "2867040"),
        },
        "napojení": "2867014"
    },
    "TWU 4.08-51-DM-C": {
        "řízení": "DOMESTIC CONTROL 1T/10-S (2865996)",
        "expanze": "SET 50 (2865134)",
        "kabel": {
            20: ("4x1,5 mm²", "2867011"),
            30: ("4x1,5 mm²", "2867012"),
            40: ("4x1,5 mm²", "2860713"),
            50: ("4x2,5 mm²", "2867040"),
        },
        "napojení": "2867014"
    },
}
# --- Funkce ---
def doporuc_kabel(accessory, hloubka):
    if accessory and "kabel" in accessory:
        delky = sorted(accessory["kabel"].keys())
        for d in delky:
            if hloubka <= d:
                return d, accessory["kabel"][d]
        return delky[-1], accessory["kabel"][delky[-1]]
    return (None, (None, None))

def get_twu4_accessories(pump_model, accessories_dict):
    pump_model_norm = pump_model.replace(" ", "").replace("-", "").replace(".", "").upper()
    for key in accessories_dict:
        key_norm = key.replace(" ", "").replace("-", "").replace(".", "").upper()
        if pump_model_norm in key_norm or key_norm in pump_model_norm:
            return accessories_dict[key]
    return None

def najdi_hwj(Q):
    for hwj in DATA_HWJ:
        if Q <= hwj["Q_max"]:
            return hwj
    return DATA_HWJ[-1]

def calculate_head(dist_vert, riser, press_bar, dist_horz, friction_coeff=0.05):
    head_press = press_bar * 10
    loss = dist_horz * friction_coeff
    total_head = dist_vert + riser + head_press + loss
    return total_head, loss

def calculate_flow(persons, sprinklers, nozzles):
    q_ls = persons * 0.1 + sprinklers * 0.2 + nozzles * 0.1
    return q_ls * 3.6

def find_best_pump(df, req_H, req_Q):
    candidates = df[(df["H_max"] >= req_H) & (df["Q_max"] >= req_Q)]
    if not candidates.empty:
        candidates = candidates.copy()
        candidates["total_diff"] = (candidates["H_max"] - req_H) + (candidates["Q_max"] - req_Q)
        return candidates.nsmallest(1, "total_diff")
    df = df.copy()
    df["abs_diff"] = (df["H_max"] - req_H).abs() + (df["Q_max"] - req_Q).abs()
    return df.nsmallest(1, "abs_diff")

# --- UI a logika ---
st.title("Konfigurátor pro výběr čerpadla Wilo 💧")
st.markdown("Zadejte parametry zdroje a odběru. Doporučené čerpadlo a příslušenství budou vybrány automaticky.")

typ_zdroje = st.radio(
    "Typ zdroje vody:",
    (
        "Kopaná studna (>500 mm)",
        "Vrt od 120 do 250 mm",
        "Vrt do 120 mm"
    )
)

st.header("Parametry odběru vody")
col1, col2 = st.columns([2, 1])
with col1:
    dist_vert = st.number_input(
        "Svislá vzdálenost (od hladiny ke středu čerpadla) [m]",
        0.0, 1000.0, 5.0, step=1.0,
        help="Výška hladiny vody ode dna do čerpadla – pro povrchová čerpadla max. 8 m"
    )
    dist_horz = st.number_input(
        "Vzdálenost od čerpadla k prvnímu odběrnému místu [m]",
        0.0, 1000.0, 15.0, step=1.0,
        help="Délka vodovodního potrubí od čerpadla ke kohoutku"
    )
    press_bar = st.number_input(
        "Požadovaný tlak na výstupu [bar]",
        0.0, 20.0, 2.0, step=0.1,
        help="Tlak, který potřebujete v nejvyšším místě rozvodu"
    )
with col2:
    riser = st.number_input(
        "Výškový rozdíl mezi čerpadlem a nejvyšším odběrným místem [m]",
        0.0, 500.0, 2.0, step=1.0,
        help="Např. pokud je odběr v patře"
    )
    persons = st.number_input(
        "Počet osob v domácnosti", 1, 20, 4,
        help="Vliv na typický průtok"
    )
    sprinklers = st.number_input(
        "Počet zavlažovacích zařízení", 0, 10, 1,
        help="Počet závlahových postřikovačů"
    )
    nozzles = st.number_input(
        "Počet výstupů pro hadici", 0, 20, 1,
        help="Počet míst, kde bude současně voda"
    )

# --- Hloubka vrtu jako číslo ---
hloubka_vrtu = None
if typ_zdroje == "Vrt od 120 do 250 mm":
    hloubka_vrtu = st.number_input(
        "Hloubka vrtu (pro volbu kabelu a lanka) [m]",
        min_value=10, max_value=200, value=30,
        step=1, help="Celková hloubka vrtu od povrchu – kabel a lanko se doporučí podle této hodnoty."
    )

if typ_zdroje == "Kopaná studna (>500 mm)":
    df_long = pd.DataFrame(DATA_TWI5, columns=["H_max", "Q_max", "PumpModel"])
elif typ_zdroje == "Vrt od 120 do 250 mm":
    df_long = pd.DataFrame(DATA_TWU4, columns=["H_max", "Q_max", "PumpModel"])
else:
    df_long = pd.DataFrame(DATA_TWU3, columns=["H_max", "Q_max", "PumpModel"])
df_long["Voltage"] = 230

if st.button("Spočítat"):
    H, loss = calculate_head(dist_vert, riser, press_bar, dist_horz)
    Q = calculate_flow(persons, sprinklers, nozzles)
    req_H = math.ceil(H)
    req_Q = math.ceil(Q)
    st.write(f"Výtlak H: {H:.2f} m (zaokrouhleno na {req_H} m), ztráta: {loss:.2f} m")
    st.write(f"Průtok Q: {Q:.2f} m³/h (zaokrouhleno na {req_Q} m³/h)")

    # HWJ domácí vodárny pro kopanou studnu do 8 m
    if typ_zdroje == "Kopaná studna (>500 mm)" and dist_vert <= 8:
        hwj = najdi_hwj(req_Q)
        st.subheader("Doporučená domácí vodárna (pro nízký výtlak):")
        st.markdown(
            f"**{hwj['model']}** | H_max: {hwj['H_max']} m | Q_max: {hwj['Q_max']} m³/h"
        )
        st.info("Pro sání do 8 metrů je vhodné použít domácí vodárnu s integrovanou expanzní nádobou.")

        # Výpis e-shopů
        st.markdown("### Kde koupit domácí vodárnu HWJ:")
        for shop in HWJ_SHOPS:
            st.markdown(
                f"""
                <span style="font-weight:500;">{shop['name']}</span>
                <a href="{shop['url']}" target="_blank" class="shop-btn">Koupit</a>
                """,
                unsafe_allow_html=True
            )
    else:
        result = find_best_pump(df_long, req_H, req_Q)
        if not result.empty:
            pump = result.iloc[0]
            st.subheader("Doporučené čerpadlo:")
            st.markdown(
                f"**{pump['PumpModel']}** | Napětí: {int(pump['Voltage'])} V | "
                f"H_max: {int(pump['H_max'])} m | Q_max: {pump['Q_max']} m³/h"
            )
            # Příslušenství pro TWU4
            if typ_zdroje == "Vrt od 120 do 250 mm":
                acc = get_twu4_accessories(pump['PumpModel'], TWU4_ACCESSORIES)
                if acc:
                    st.subheader("Doporučené příslušenství:")
                    st.write(f"- Řízení: **{acc['řízení']}**")
                    st.write(f"- Expanze: **{acc['expanze']}**" if acc['expanze'] else "- Expanze: (není potřeba)")
                    if hloubka_vrtu:
                        dop_delka, (kabel_typ, kabel_obj) = doporuc_kabel(acc, hloubka_vrtu)
                        if kabel_typ:
                            st.write(f"- Kabel a lanko: **{kabel_typ}** (obj. {kabel_obj}) – doporučeno pro vrt {dop_delka} m (zadáno {hloubka_vrtu} m)")
                        else:
                            st.warning("Pro zadanou hloubku není kabel v seznamu.")
                    st.write(f"- Napojení: **{acc['napojení']}**")
                else:
                    st.info("Pro tento model není příslušenství v seznamu.")

            st.markdown(
                """
                <a href="https://wilo.com/cz/cs/dum-a-zahrada/%C5%98e%C5%A1en%C3%AD/" target="_blank">
                    <button style='font-size:1.2em; background:#21B6A8; color:white; padding:0.5em 2em; border:none; border-radius:6px; cursor:pointer; margin-top:1em;'>🌐 Kde koupit?</button>
                </a>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning("Žádné čerpadlo nesplňuje potřebné parametry.")
