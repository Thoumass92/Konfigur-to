import streamlit as st
import pandas as pd
import math

# --- Barvy ---
WILO_GREEN = "#21B6A8"
WILO_GREEN_LIGHT = "#d6f7f2"
WILO_GREY = "#f5f5f5"

# --- Logo ---
WILO_LOGO_URL = "https://scontent-fra3-1.xx.fbcdn.net/v/t39.30808-6/312307533_996663857947185_6220530952015731225_n.png?_nc_cat=108&ccb=1-7&_nc_sid=6ee11a&_nc_ohc=83_eOJu59pQQ7kNvwF1FuJO&_nc_oc=AdneoM6Ax72YEQxMPuPNAht6eEjBBfllTwCT3yezrDZ-QGObbuWxfAnWIddVn6dLfSs&_nc_zt=23&_nc_ht=scontent-fra3-1.xx&_nc_gid=Yvtk47THe4NhpdkBwjbyjA&oh=00_AfTEkPpnVzUkus59W8aK0U_bAIazC2CjjpJAEQDqjSBFcg&oe=68916816"

# --- Překladové slovníky ---
LANGS = {
    "CZ": {
        "lang": "Čeština",
        "switch": "Jazyk",
        "title": "Výběr vhodného čerpadla",
        "subtitle": "Konfigurátor pro výběr čerpadla Wilo 💧",
        "desc": "Zadejte parametry zdroje a odběru. Doporučené čerpadlo a příslušenství budou vybrány automaticky.",
        "source_type": "Typ zdroje vody:",
        "studna": "Kopaná studna (>500 mm)",
        "vrt120": "Vrt od 120 do 250 mm",
        "vrt100": "Vrt do 120 mm",
        "params_header": "Parametry odběru vody",
        "depth": "Svislá vzdálenost (od hladiny ke středu čerpadla) [m]",
        "pipe": "Vzdálenost od čerpadla k prvnímu odběrnému místu [m]",
        "press": "Požadovaný tlak na výstupu [bar]",
        "riser": "Výškový rozdíl mezi čerpadlem a nejvyšším odběrným místem [m]",
        "persons": "Počet osob v domácnosti",
        "sprinklers": "Počet zavlažovacích zařízení",
        "nozzles": "Počet výstupů pro hadici",
        "vrt_depth": "Hloubka vrtu (pro volbu kabelu a lanka) [m]",
        "spocitat": "Spočítat",
        "head": "Výtlak H",
        "loss": "ztráta",
        "flow": "Průtok Q",
        "hwj_title": "Doporučená domácí vodárna (pro nízký výtlak):",
        "hwj_suitable": "Pro sání do 8 metrů je vhodné použít domácí vodárnu s integrovanou expanzní nádobou.",
        "where_hwk": "Kde koupit domácí vodárnu HWJ:",
        "buy": "Koupit",
        "pump_title": "Doporučené čerpadlo:",
        "voltage": "Napětí",
        "head_max": "H_max",
        "flow_max": "Q_max",
        "shop_btn": "🌐 Kde koupit?",
        "no_pump": "Žádné čerpadlo nesplňuje potřebné parametry.",
        "accessories": "Doporučené příslušenství:",
        "control": "Řízení",
        "expansion": "Expanze",
        "cable": "Kabel a lanko",
        "connection": "Napojení",
        "for_well": "pro vrt",
        "not_in_list": "Pro zadanou hloubku není kabel v seznamu.",
        "title": "Výběr vhodného čerpadla",
        "desc": "Zadejte parametry zdroje a odběru. Doporučené čerpadlo a příslušenství budou vybrány automaticky."
    },
    "EN": {
        "lang": "English",
        "switch": "Language",
        "title": "Pump Selection Tool",
        "subtitle": "Wilo Pump Selection Configurator 💧",
        "desc": "Enter your source and usage parameters. Recommended pump and accessories will be selected automatically.",
        "source_type": "Source type:",
        "studna": "Dug well (>500 mm)",
        "vrt120": "Borehole 120–250 mm",
        "vrt100": "Borehole up to 120 mm",
        "params_header": "Water draw parameters",
        "depth": "Vertical distance (from water level to pump center) [m]",
        "pipe": "Distance from pump to first draw-off point [m]",
        "press": "Required outlet pressure [bar]",
        "riser": "Elevation difference between pump and highest draw-off point [m]",
        "persons": "Number of persons in household",
        "sprinklers": "Number of sprinklers",
        "nozzles": "Number of hose outlets",
        "vrt_depth": "Well depth (for cable and rope selection) [m]",
        "spocitat": "Calculate",
        "head": "Total Head H",
        "loss": "loss",
        "flow": "Flow Q",
        "hwj_title": "Recommended domestic waterworks (for low lift):",
        "hwj_suitable": "For suction up to 8 meters, a domestic waterworks with integrated expansion vessel is suitable.",
        "where_hwk": "Where to buy HWJ domestic waterworks:",
        "buy": "Buy",
        "pump_title": "Recommended pump:",
        "voltage": "Voltage",
        "head_max": "H_max",
        "flow_max": "Q_max",
        "shop_btn": "🌐 Where to buy?",
        "no_pump": "No pump meets the required parameters.",
        "accessories": "Recommended accessories:",
        "control": "Control",
        "expansion": "Expansion",
        "cable": "Cable & rope",
        "connection": "Connection",
        "for_well": "for well",
        "not_in_list": "No cable in list for this well depth.",
        "lang": "English",
        "title": "Pump Selection Tool",
        "desc": "Enter your source and demand parameters. The recommended pump and accessories will be selected automatically."
    }
}

# --- Větší selectbox a úpravy vzhledu ---
st.markdown(f"""
    <style>
    .lang-selectbox label {{display:none;}}
    div[data-baseweb="select"] {{ width:200px !important; font-size:1.13em !important;}}
    .header-main {{
        width:100vw; min-width:1000px; margin-left:calc(-50vw + 50%);
        background:{WILO_GREEN}; 
        padding:2.3em 0 2em 0; border-radius:0 0 32px 32px; box-shadow:0 8px 36px #21b6a81b;
    }}
    .header-content {{display:flex; align-items:center; justify-content:center; gap:28px;}}
    .header-title {{color:white; font-size:2.7em; font-weight:900; letter-spacing:-1px;}}
    .header-desc {{margin-top:1em; font-size:1.2em; color:#444; text-align:center;}}
    .langbar {{width:100%%; display:flex; justify-content:flex-end; margin-bottom:-3.2em; margin-top:1.2em;}}
    </style>
""", unsafe_allow_html=True)


# --- Jazykový přepínač vždy vpravo nahoře ---
st.markdown("<div class='langbar'>", unsafe_allow_html=True)
lang = st.selectbox(
    "",
    options=["CZ", "EN"],
    format_func=lambda x: LANGS[x]["lang"],
    key="lang_selectbox",
    label_visibility="collapsed"
)
st.markdown("</div>", unsafe_allow_html=True)
TXT = LANGS[lang]

# --- Hlavička a popis ---
st.markdown(
    f"""
    <div class='header-main'>
      <div class='header-content'>
        <img src="{WILO_LOGO_URL}" style="height:56px; margin-right:18px;">
        <span class='header-title'>{TXT['title']}</span>
      </div>
    </div>
    <div class='header-desc'>
      {TXT['desc']}
    </div>
    """, unsafe_allow_html=True
)
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
def najdi_hwj(Q):
    for hwj in DATA_HWJ:
        if Q <= hwj["Q_max"]:
            return hwj
    return DATA_HWJ[-1] if DATA_HWJ else None

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

def get_twu4_accessories(pump_model, accessories_dict):
    pump_model_norm = pump_model.replace(" ", "").replace("-", "").replace(".", "").upper()
    for key in accessories_dict:
        key_norm = key.replace(" ", "").replace("-", "").replace(".", "").upper()
        if pump_model_norm in key_norm or key_norm in pump_model_norm:
            return accessories_dict[key]
    return None

def doporuc_kabel(accessory, hloubka):
    if accessory and "kabel" in accessory:
        delky = sorted(accessory["kabel"].keys())
        for d in delky:
            if hloubka <= d:
                return d, accessory["kabel"][d]
        return delky[-1], accessory["kabel"][delky[-1]]
    return (None, (None, None))
st.markdown(
    f"<hr style='border: none; border-top: 2.5px solid {WILO_GREY}; margin: 38px 0;'>",
    unsafe_allow_html=True
)

# --- UI parametry ---
typ_zdroje = st.selectbox(
    TXT["source_type"],
    (
        TXT["studna"],
        TXT["vrt120"],
        TXT["vrt100"]
    ),
    key="typ_zdroje_selectbox"
)
st.header(TXT["params_header"])
col1, col2 = st.columns([1, 1])
with col1:
    dist_vert = st.number_input(
        TXT["depth"],
        0.0, 1000.0, 4.0, step=1.0
    )
    dist_horz = st.number_input(
        TXT["pipe"],
        0.0, 1000.0, 3.0, step=1.0
    )
    press_bar = st.number_input(
        TXT["press"],
        0.0, 20.0, 2.0, step=0.5
    )
    riser = st.number_input(
        TXT["riser"],
        0.0, 500.0, 2.0, step=1.0
    )
    
with col2:
    persons = st.number_input(
        TXT["persons"], 1, 20, 4
    )
    sprinklers = st.number_input(
        TXT["sprinklers"], 0, 10, 1
    )
    nozzles = st.number_input(
        TXT["nozzles"], 0, 20, 1
    )
st.markdown(
    f"<hr style='border: none; border-top: 2.5px solid {WILO_GREY}; margin: 38px 0;'>",
    unsafe_allow_html=True
)
hloubka_vrtu = None
if typ_zdroje == TXT["vrt120"]:
    hloubka_vrtu = st.number_input(
        TXT["vrt_depth"], min_value=10, max_value=200, value=30, step=1
    )

if typ_zdroje == TXT["studna"]:
    df_long = pd.DataFrame(DATA_TWI5, columns=["H_max", "Q_max", "PumpModel"])
elif typ_zdroje == TXT["vrt120"]:
    df_long = pd.DataFrame(DATA_TWU4, columns=["H_max", "Q_max", "PumpModel"])
else:
    df_long = pd.DataFrame(DATA_TWU3, columns=["H_max", "Q_max", "PumpModel"])
df_long["Voltage"] = 230

if st.button(TXT["spocitat"]):
    H, loss = calculate_head(dist_vert, riser, press_bar, dist_horz)
    Q = calculate_flow(persons, sprinklers, nozzles)
    req_H = math.ceil(H)
    req_Q = math.ceil(Q)
    st.markdown(
        f"<div style='margin:1.3em 0 0.5em 0;color:#222;font-size:1.09em;'>"
        f"<b>{TXT['head']}:</b> {H:.2f} m (rounded {req_H} m), <b>{TXT['loss']}:</b> {loss:.2f} m<br>"
        f"<b>{TXT['flow']}:</b> {Q:.2f} m³/h (rounded {req_Q} m³/h)</div>",
        unsafe_allow_html=True
    )
    # --- HWJ doporučení ---
    if typ_zdroje == TXT["studna"] and dist_vert <= 8 and DATA_HWJ:
        hwj = najdi_hwj(req_Q)
        st.markdown(
            f"<div style='background:{WILO_GREEN_LIGHT};border-left:8px solid {WILO_GREEN};padding:1.4em 2em 1.1em 2em;margin:2em 0 1.2em 0;border-radius:11px;'>"
            f"<span style='font-size:1.35em;font-weight:700;'>{TXT['hwj_title']}</span><br><br>"
            f"<b style='font-size:1.18em;color:#222;'>{hwj['model']}</b> | <span style='color:#777;'>H_max:</span> {hwj['H_max']} m | <span style='color:#777;'>Q_max:</span> {hwj['Q_max']:.1f} m³/h"
            f"<div style='margin-top:1em;background:#eaf5ff;border-radius:7px;padding:0.7em 1.2em;font-size:1em;'>{TXT['hwj_suitable']}</div>"
            "</div>",
            unsafe_allow_html=True
        )
        st.markdown(f"<h4 style='margin-top:0.7em'>{TXT['where_hwk']}</h4>", unsafe_allow_html=True)
        shops = [
            {"name": "Bola.cz", "url": "https://www.bola.cz/vyhledat-produkt/HWJ"},
            {"name": "Pumpa.eu", "url": "https://www.pumpa.eu/cs/wilo-jet-hwj-automaticke-samonasavaci-domaci-vodarny/"},
            {"name": "Kamody.cz", "url": "https://www.kamody.cz/index.php?route=product/search&filter_name=HWJ"}
        ]
        for shop in shops:
            st.markdown(
                f"<div style='display:flex;align-items:center;margin-bottom:0.5em;'>"
                f"<span style='font-size:1.11em;font-weight:500;width:120px'>{shop['name']}</span>"
                f"<a href='{shop['url']}' target='_blank'>"
                f"<button style='margin-left:18px;padding:0.45em 1.6em;background:{WILO_GREEN};color:white;font-weight:bold;border:none;border-radius:6px;cursor:pointer;font-size:1.09em;'>{TXT['buy']}</button>"
                f"</a></div>", unsafe_allow_html=True)

    else:
        result = find_best_pump(df_long, req_H, req_Q)
        if not result.empty:
            pump = result.iloc[0]
            st.markdown(
                f"<div style='background:#F8FCFB;border-left:8px solid {WILO_GREEN};padding:1.2em 2em 1.2em 2em;margin:2em 0 1.3em 0;border-radius:11px;'>"
                f"<span style='font-size:1.3em;font-weight:700;'>{TXT['pump_title']}</span><br><br>"
                f"<b style='font-size:1.12em;color:#222;'>{pump['PumpModel']}</b> | <span style='color:#777;'>{TXT['voltage']}:</span> {int(pump['Voltage'])} V | <span style='color:#777;'>{TXT['head_max']}:</span> {int(pump['H_max'])} m | <span style='color:#777;'>{TXT['flow_max']}:</span> {pump['Q_max']:.1f} m³/h"
                "</div>",
                unsafe_allow_html=True
            )
            # --- Doplněk: příslušenství pro TWU4 ---
            if typ_zdroje == TXT["vrt120"]:
                acc = get_twu4_accessories(pump['PumpModel'], TWU4_ACCESSORIES)
                if acc:
                    st.markdown(f"<h4 style='margin-top:1.2em'>{TXT['accessories']}</h4>", unsafe_allow_html=True)
                    st.markdown(f"- <b>{TXT['control']}:</b> {acc['řízení']}", unsafe_allow_html=True)
                    st.markdown(f"- <b>{TXT['expansion']}:</b> {acc['expanze']}" if acc['expanze'] else f"- <b>{TXT['expansion']}:</b> (není potřeba)", unsafe_allow_html=True)
                    # Automatická volba kabelu:
                    if hloubka_vrtu:
                        dop_delka, (kabel_typ, kabel_obj) = doporuc_kabel(acc, hloubka_vrtu)
                        if kabel_typ:
                            st.markdown(f"- <b>{TXT['cable']}:</b> {kabel_typ} (obj. {kabel_obj}) – {TXT['for_well']} {dop_delka} m (zadáno {hloubka_vrtu} m)", unsafe_allow_html=True)
                        else:
                            st.warning(TXT['not_in_list'])
                    st.markdown(f"- <b>{TXT['connection']}:</b> {acc['napojení']}", unsafe_allow_html=True)
            st.markdown(
                f"""
                <a href="https://wilo.com/cz/cs/dum-a-zahrada/%C5%98e%C5%A1en%C3%AD/" target="_blank">
                    <button style='font-size:1.14em; background:{WILO_GREEN}; color:white; padding:0.55em 2.2em; border:none; border-radius:8px; cursor:pointer; margin-top:0.7em;'>{TXT['shop_btn']}</button>
                </a>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning(TXT["no_pump"])
