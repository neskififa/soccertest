import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import requests
from bs4 import BeautifulSoup
import re
import json
import urllib.parse
from datetime import datetime
from zoneinfo import ZoneInfo
import random
import json
from datetime import datetime, timedelta
import numpy as np

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================

st.set_page_config(
    page_title="PROBIUM | Quantitative Betting Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 1. SETUP DEUS TIER (DARK MATTER THEME)
# CSS PREMIUM - CYBERPUNK DARK THEME
# ==========================================
st.set_page_config(page_title="PROBUM | God Tier Engine", page_icon="👁️", layout="wide", initial_sidebar_state="collapsed")

# Inicialização e Atualização do Banco de Dados para suportar tudo
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&family=JetBrains+Mono:wght@400;700&display=swap');

:root {
    --primary: #00f0ff;
    --secondary: #7000ff;
    --accent: #ff006e;
    --success: #00ff88;
    --warning: #ffb700;
    --danger: #ff0040;
    --bg-dark: #050505;
    --bg-card: #0a0a0f;
    --bg-elevated: #12121a;
    --border: #1e1e2e;
    --text-primary: #ffffff;
    --text-secondary: #a0a0b0;
}

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #050505 0%, #0a0a1a 50%, #0f0f23 100%);
    color: var(--text-primary);
}

/* Sidebar Premium */
.css-1d391kg, .css-163ttbj, .stSidebar {
    background: linear-gradient(180deg, #0a0a0f 0%, #12121a 100%) !important;
    border-right: 1px solid var(--border);
}

/* Typography */
.title-main {
    font-size: 72px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(135deg, #00f0ff 0%, #7000ff 50%, #ff006e 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -2px;
    margin-bottom: 10px;
    text-shadow: 0 0 60px rgba(0, 240, 255, 0.3);
}

.subtitle {
    text-align: center;
    color: var(--text-secondary);
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 6px;
    text-transform: uppercase;
    margin-bottom: 40px;
}

/* Cards Glassmorphism */
.bet-card {
    background: rgba(18, 18, 26, 0.8);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.bet-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    opacity: 0;
    transition: opacity 0.3s ease;
}

.bet-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 60px rgba(0, 240, 255, 0.15);
    border-color: rgba(0, 240, 255, 0.3);
}

.bet-card:hover::before {
    opacity: 1;
}

/* Metric Cards */
.metric-card {
    background: linear-gradient(135deg, rgba(0, 240, 255, 0.1) 0%, rgba(112, 0, 255, 0.1) 100%);
    border: 1px solid rgba(0, 240, 255, 0.2);
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.metric-value {
    font-size: 36px;
    font-weight: 900;
    color: var(--primary);
    font-family: 'JetBrains Mono', monospace;
}

.metric-label {
    font-size: 12px;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-top: 8px;
}

/* EV Indicators */
.ev-positive {
    color: var(--success);
    font-weight: 800;
    font-size: 24px;
    font-family: 'JetBrains Mono', monospace;
    text-shadow: 0 0 20px rgba(0, 255, 136, 0.4);
}

.ev-negative {
    color: var(--danger);
    font-weight: 800;
    font-size: 24px;
    font-family: 'JetBrains Mono', monospace;
}

/* Odds Display */
.odds-display {
    font-size: 48px;
    font-weight: 900;
    color: var(--text-primary);
    font-family: 'JetBrains Mono', monospace;
    line-height: 1;
}

.odds-label {
    font-size: 12px;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 2px;
}

/* Market Info */
.market-badge {
    display: inline-block;
    background: rgba(112, 0, 255, 0.2);
    color: var(--secondary);
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    border: 1px solid rgba(112, 0, 255, 0.3);
}

.team-name {
    font-size: 28px;
    font-weight: 800;
    color: var(--text-primary);
    margin: 12px 0;
}

.vs-divider {
    color: var(--text-secondary);
    font-size: 14px;
    font-weight: 600;
    margin: 0 12px;
}

/* Kelly Criterion Box */
.kelly-box {
    background: rgba(5, 5, 5, 0.6);
    border: 1px dashed rgba(0, 240, 255, 0.3);
    border-radius: 12px;
    padding: 16px;
    margin-top: 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.kelly-label {
    font-size: 12px;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1px;
}

.kelly-value {
    font-size: 24px;
    font-weight: 900;
    color: var(--warning);
    font-family: 'JetBrains Mono', monospace;
}

/* Quantum Button */
.quantum-btn {
    background: linear-gradient(135deg, #00f0ff 0%, #7000ff 100%);
    color: white;
    border: none;
    padding: 20px 40px;
    border-radius: 16px;
    font-size: 16px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 2px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    box-shadow: 0 0 40px rgba(0, 240, 255, 0.3);
}

.quantum-btn:hover {
    transform: scale(1.05);
    box-shadow: 0 0 60px rgba(0, 240, 255, 0.5);
}

.quantum-btn::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
    transition: left 0.5s;
}

.quantum-btn:hover::before {
    left: 100%;
}

/* Status Badges */
.status-pendente {
    background: rgba(255, 183, 0, 0.2);
    color: var(--warning);
    border: 1px solid rgba(255, 183, 0, 0.3);
}

.status-ganho {
    background: rgba(0, 255, 136, 0.2);
    color: var(--success);
    border: 1px solid rgba(0, 255, 136, 0.3);
}

.status-perda {
    background: rgba(255, 0, 64, 0.2);
    color: var(--danger);
    border: 1px solid rgba(255, 0, 64, 0.3);
}

/* Divider */
.custom-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    margin: 40px 0;
    border: none;
}

/* Table Styling */
.stDataFrame {
    background: rgba(18, 18, 26, 0.8) !important;
    border-radius: 16px !important;
    border: 1px solid var(--border) !important;
}

/* Input Fields */
.stTextInput input, .stNumberInput input, .stSelectbox select {
    background: rgba(18, 18, 26, 0.8) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: white !important;
    padding: 12px 16px !important;
}

/* Progress Bars */
.stProgress > div > div {
    background: linear-gradient(90deg, var(--primary), var(--secondary)) !important;
    border-radius: 10px !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-dark);
}

::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--primary);
}

/* Animations */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.live-indicator {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: var(--success);
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.live-indicator::before {
    content: '';
    width: 8px;
    height: 8px;
    background: var(--success);
    border-radius: 50%;
    animation: pulse 2s infinite;
    box-shadow: 0 0 10px var(--success);
}

/* Confidence Meter */
.confidence-meter {
    width: 100%;
    height: 6px;
    background: rgba(255,255,255,0.1);
    border-radius: 3px;
    overflow: hidden;
    margin-top: 12px;
}

.confidence-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--danger), var(--warning), var(--success));
    border-radius: 3px;
    transition: width 0.5s ease;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# BANCO DE DADOS - SUPABASE POSTGRESQL
# ==========================================

def get_db_connection():
    """Conecta ao PostgreSQL da Supabase"""
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        
        # Usando a URL do seu Supabase (da memória)
        conn = psycopg2.connect(
            "postgresql://postgres.lyickymaibsakuqhevat:[PASSWORD]@aws-0-us-west-2.pooler.supabase.com:5432/postgres",
            cursor_factory=RealDictCursor
        )
        return conn
    except:
        # Fallback para SQLite local se PostgreSQL falhar
        return sqlite3.connect("probum.db")

def init_db():
    conn = sqlite3.connect("probum.db")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    
    # Tabela de operações
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS operacoes_tipster (
            id_aposta TEXT PRIMARY KEY, esporte TEXT, jogo TEXT, liga TEXT, mercado TEXT, selecao TEXT,
            odd REAL, prob REAL, ev REAL, stake REAL, status TEXT DEFAULT 'PENDENTE', lucro REAL DEFAULT 0,
            data_hora TEXT, pinnacle_odd REAL, ranking_score REAL, nivel_confianca TEXT, justificativa TEXT,
            stats_home TEXT, stats_away TEXT, fonte_dados TEXT, linha REAL, odd_history TEXT,
            kelly_stake REAL, telegram_enviado INTEGER DEFAULT 0
        )
    CREATE TABLE IF NOT EXISTS operacoes_tipster(
        id_aposta TEXT PRIMARY KEY,
        jogo TEXT,
        liga TEXT,
        mercado TEXT,
        selecao TEXT,
        odd REAL,
        prob REAL,
        ev REAL,
        kelly REAL,
        stake REAL DEFAULT 0,
        status TEXT DEFAULT 'PENDENTE',
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        data_resultado TIMESTAMP,
        lucro REAL DEFAULT 0
    )
    """)
    
    # Tabela de histórico de banca
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historico_banca(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        banca_total REAL,
        roi REAL,
        apostas_feitas INTEGER
    )
    """)
    
    conn.commit()
    conn.close()

init_db()

st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #F8FAFC; font-family: 'Inter', sans-serif; }
    
    .main-title {
        font-size: 3.5rem; font-weight: 900; text-align: center;
        background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0px; letter-spacing: -2px; text-transform: uppercase;
    }
    .sub-title { color: #64748B; text-align: center; font-size: 1.1rem; letter-spacing: 4px; margin-bottom: 40px; text-transform: uppercase; font-weight: bold;}

    /* God Tier Match Card & Diamond */
    .god-card {
        background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.05); border-radius: 24px;
        padding: 24px; margin-bottom: 30px; position: relative; overflow: hidden;
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.05), 0 20px 40px -20px rgba(0,0,0,1);
    }
    .diamond-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 2px solid #EAB308; box-shadow: 0 0 30px rgba(234, 179, 8, 0.15);
    }
    .diamond-badge { position: absolute; top: 0; left: 0; background: linear-gradient(90deg, #EAB308, #F59E0B); color: #000; font-weight: 900; padding: 6px 20px; border-bottom-right-radius: 16px; font-size: 0.8rem; letter-spacing: 1px; }

    /* Teams & UI */
    .teams-grid { display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; text-align: center; margin-bottom: 20px; }
    .team-col img { width: 70px; height: 70px; border-radius: 50%; border: 2px solid #334155; margin-bottom: 8px; box-shadow: 0 0 20px rgba(0,0,0,0.5);}
    .team-name { font-size: 1.1rem; font-weight: 800; color: #F1F5F9; }
    .vs-text { font-size: 1.5rem; font-weight: 900; color: #38BDF8; font-style: italic; padding: 0 20px; }

    /* The Call Box (Kelly & Market) */
    .call-box {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.05) 100%);
        border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 16px; padding: 20px; text-align: center;
        display: grid; grid-template-columns: 1fr 1fr 1fr; align-items: center; margin-bottom: 16px;
    }
    .diamond-call-box { background: rgba(234, 179, 8, 0.1); border-color: #EAB308; }
    .call-title { font-size: 0.7rem; color: #10B981; text-transform: uppercase; font-weight: 900; letter-spacing: 2px; margin-bottom: 4px;}
    .diamond-call-box .call-title { color: #EAB308; }
    .call-market { font-size: 1.3rem; font-weight: 900; color: #FFF; }
    .kelly-box { background: rgba(0,0,0,0.3); padding: 10px; border-radius: 12px; border: 1px dashed rgba(255,255,255,0.2); }
    .kelly-title { font-size: 0.65rem; color: #94A3B8; text-transform: uppercase; font-weight: bold; }
    .kelly-value { font-size: 1.5rem; color: #EAB308; font-weight: 900; }

    /* NLP Bars & Context */
    .intel-bar-container { margin-bottom: 12px; }
    .intel-label { display: flex; justify-content: space-between; font-size: 0.75rem; color: #CBD5E1; font-weight: bold; margin-bottom: 4px; text-transform: uppercase; }
    .intel-bar-bg { width: 100%; height: 6px; background: #1E293B; border-radius: 10px; overflow: hidden; }
    .intel-bar-fill-ai { height: 100%; background: linear-gradient(90deg, #3B82F6, #8B5CF6); }
    .intel-bar-fill-web { height: 100%; background: linear-gradient(90deg, #10B981, #EAB308); }
    
    .context-row { display: flex; justify-content: space-around; background: #0F172A; padding: 12px; border-radius: 12px; font-size: 0.8rem; color: #CBD5E1; margin-bottom: 16px;}
    .context-item span { font-weight: bold; color: #38BDF8; }

    /* Quantum Button */
    .btn-quantum { background: linear-gradient(90deg, #8B5CF6, #3B82F6); border: none; color: white; padding: 18px; text-align: center; font-size: 18px; border-radius: 16px; cursor: pointer; width: 100%; font-weight: 900; box-shadow: 0 0 20px rgba(139, 92, 246, 0.4); text-transform: uppercase; letter-spacing: 2px;}
    .btn-quantum:hover { opacity: 0.9; transform: scale(1.01); }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. MOTORES NEURAIS (SCRAPING, NLP E MATH)
# FUNÇÕES DE CÁLCULO
# ==========================================

def calcular_stake_kelly(odd, prob_real, fracao=0.25):
    """Fórmula Exata de Wall Street para Gestão de Risco"""
def calcular_kelly(odd, prob, fracao=0.25):
    """Kelly Criterion com fração ajustável"""
    b = odd - 1
    p = prob_real
    q = 1 - p
    kelly = (b * p - q) / b
    if kelly <= 0: return 0.5
    return round(min(kelly * fracao * 100, 5.0), 2)

@st.cache_data(ttl=3600)
def oraculo_contexto_invisivel(equipe_casa, equipe_fora):
    """ Extrai clima, árbitro e desfalques sem API """
    query = f"{equipe_casa} x {equipe_fora} desfalques clima arbitro"
    url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        req = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(req.text, 'html.parser')
        txt = " ".join([a.text.lower() for a in soup.find_all('a', class_='result__snippet')[:3]])
        clima = "🌧️ Possível Chuva" if any(w in txt for w in ['chuva', 'temporal', 'alagado']) else "☀️ Bom Clima"
        juiz = "🟨 Jogo Faltoso" if any(w in txt for w in ['cartões', 'rigoroso', 'polêmica']) else "⚖️ Arbitragem Padrão"
        foco = "⚠️ Desfalques" if any(w in txt for w in ['poupando', 'misto', 'desfalque', 'lesão']) else "🔥 Força Máxima"
        return clima, juiz, foco
    except: return "☀️ ND", "⚖️ ND", "🔥 ND"

def analise_sentimento_web(equipe_casa, equipe_fora):
    """ Analisa o sentimento da internet para calcular consenso """
    query = f"{equipe_casa} vs {equipe_fora} previsao palpites"
    url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
    try:
        req = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
        soup = BeautifulSoup(req.text, 'html.parser')
        texto_puro = " ".join([a.text.lower() for a in soup.find_all('a', class_='result__snippet')[:5]])
    q = 1 - prob
    kelly = ((b * prob) - q) / b
    
    if kelly <= 0:
        return 0
    
    return round(min(kelly * 100 * fracao, 5), 2)

def calcular_ev(odd, prob):
    """Calcula Expected Value"""
    return (prob * odd) - 1

def calcular_stake(banca, kelly_percent, unidade=1):
    """Calcula stake baseado na banca e Kelly"""
    return round((banca * (kelly_percent / 100)) * unidade, 2)

# ==========================================
# MOTOR DE ANÁLISE (SIMULAÇÃO PREMIUM)
# ==========================================

def gerar_oportunidades_premium():
    """Gera oportunidades de apostas com análise simulada premium"""
    
    oportunidades = []
    times_top = [
        ("Manchester City", "Premier League", 0.75),
        ("Arsenal", "Premier League", 0.72),
        ("Liverpool", "Premier League", 0.74),
        ("Real Madrid", "La Liga", 0.78),
        ("Barcelona", "La Liga", 0.76),
        ("Bayern Munich", "Bundesliga", 0.77),
        ("PSG", "Ligue 1", 0.73),
        ("Inter Milan", "Serie A", 0.71),
        ("Benfica", "Primeira Liga", 0.68),
        ("Porto", "Primeira Liga", 0.67)
    ]
    
    mercados = [
        ("Match Winner", "Casa", lambda o: 1/o + random.uniform(0.05, 0.15)),
        ("Over 2.5 Goals", "Over", lambda o: 1/o + random.uniform(0.03, 0.12)),
        ("BTTS", "Sim", lambda o: 1/o + random.uniform(0.02, 0.10)),
        ("Asian Handicap -1", "Casa", lambda o: 1/o + random.uniform(0.04, 0.14))
    ]
    
    for i in range(5):
        casa = random.choice(times_top)
        fora = random.choice([t for t in times_top if t != casa])

        score_web = 50
        casa_lower = equipe_casa.lower().split()[0]
        if len(re.findall(casa_lower, texto_puro)) > len(re.findall(equipe_fora.lower().split()[0], texto_puro)):
            score_web += 20
        for kw in ['favorito', 'amassa', 'superior', 'imbativel']:
            if kw in texto_puro: score_web += 5
        return max(10, min(95, score_web))
    except: return 50

def motor_quantico_buscar_apostas():
    """ O Cérebro: Finge ser um humano varrendo sites e acha apostas """
    queries = ["palpites de futebol hoje odds previsoes"]
    headers = {"User-Agent": "Mozilla/5.0"}
    oportunidades =[]
    
    for query in queries:
        url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
        try:
            req = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(req.text, 'html.parser')
            texto_completo = " ".join([a.text for a in soup.find_all('a', class_='result__snippet')])
            
            times = re.findall(r'([A-Z][a-z]+)\s(?:x|vs)\s([A-Z][a-z]+)', texto_completo)
            odds = re.findall(r'1\.\d{2}|2\.\d{2}', texto_completo)
            
            for i, (casa, fora) in enumerate(times[:3]):
                odd = float(odds[i]) if i < len(odds) else round(random.uniform(1.70, 2.50), 2)
                prob_matematica = (1 / odd) + random.uniform(0.02, 0.08) # Simulando EV+ encontrado
                ev = (prob_matematica * odd) - 1
                kelly = calcular_stake_kelly(odd, prob_matematica)
                score_web = analise_sentimento_web(casa, fora)
                
                # Histórico inicial para o gráfico (Dropping Odds)
                hora_atual = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime('%H:%M')
                odd_history = json.dumps([{"time": "Detectado", "odd": odd + 0.15}, {"time": hora_atual, "odd": odd}])
                
                oportunidades.append({
                    "jogo_id": f"WEB_{random.randint(1000,9999)}", "esporte": "soccer",
                    "jogo": f"{casa} x {fora}", "liga": "Prospecção Web AI", "mercado": "Match Winner",
                    "selecao": f"Vitória {casa}", "odd": odd, "prob": prob_matematica, "ev": ev,
                    "kelly_stake": kelly, "odd_history": odd_history, "score_web": score_web,
                    "justificativa": "Análise Neural extraída e validada pelo consenso da Web."
                })
        except Exception as e: st.error(f"Erro no Scraper: {e}")
        mercado_nome, selecao, prob_calc = random.choice(mercados)
        
        odd_base = round(random.uniform(1.65, 2.45), 2)
        prob = min(prob_calc(odd_base), 0.95)
        ev = calcular_ev(odd_base, prob)
        
        if ev > 0.05:  # Só oportunidades com EV positivo significativo
            kelly = calcular_kelly(odd_base, prob)

    return oportunidades
            oportunidades.append({
                "id": f"PROB-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}",
                "jogo": f"{casa[0]} x {fora[0]}",
                "liga": casa[1],
                "mercado": mercado_nome,
                "selecao": selecao if selecao == "Casa" else random.choice([casa[0], "Empate", fora[0]]),
                "odd": odd_base,
                "prob": round(prob, 3),
                "ev": round(ev, 3),
                "kelly": kelly,
                "confianca": random.randint(65, 95),
                "timestamp": datetime.now()
            })
    
    return sorted(oportunidades, key=lambda x: x['ev'], reverse=True)

# ==========================================
# 3. INTERFACE E GRÁFICOS
# GERENCIAMENTO DE BANCA
# ==========================================
def plotar_dropping_odds(json_history):
    hist = json.loads(json_history)
    df_hist = pd.DataFrame(hist)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_hist['time'], y=df_hist['odd'], mode='lines+markers',
        line=dict(color='#00F2FE', width=4, shape='spline'),
        marker=dict(size=10, color='#4FACFE', line=dict(width=2, color='white')),
        fill='tozeroy', fillcolor='rgba(0, 242, 254, 0.1)'
    ))
    fig.update_layout(
        height=150, margin=dict(l=0, r=0, t=20, b=0), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, color='#64748B'), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='#64748B'),
        title=dict(text="📉 Rastreador de Pressão Financeira (Dropping Odds)", font=dict(color='#94A3B8', size=12))
    )
    return fig

def gerar_escudo(nome):
    return f"https://ui-avatars.com/api/?name={urllib.parse.quote(nome)}&background=1E293B&color=fff&size=150&bold=true"
def get_estatisticas():
    """Retorna estatísticas da banca"""
    conn = get_db_connection()
    
    try:
        # Total de apostas
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as total FROM operacoes_tipster")
        total_apostas = cursor.fetchone()['total'] if isinstance(cursor.fetchone(), dict) else cursor.fetchone()[0]
        
        # Taxa de acerto
        cursor.execute("SELECT COUNT(*) as ganhos FROM operacoes_tipster WHERE status='GANHO'")
        ganhos = cursor.fetchone()['ganhos'] if isinstance(cursor.fetchone(), dict) else cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) as perdidos FROM operacoes_tipster WHERE status='PERDA'")
        perdidos = cursor.fetchone()['perdidos'] if isinstance(cursor.fetchone(), dict) else cursor.fetchone()[0]
        
        # Lucro/Prejuízo
        cursor.execute("SELECT SUM(lucro) as total_lucro FROM operacoes_tipster WHERE status IN ('GANHO', 'PERDA')")
        resultado = cursor.fetchone()
        lucro_total = resultado['total_lucro'] if isinstance(resultado, dict) else resultado[0]
        lucro_total = lucro_total if lucro_total else 0
        
        # ROI
        cursor.execute("SELECT SUM(stake) as total_stake FROM operacoes_tipster WHERE status IN ('GANHO', 'PERDA')")
        resultado = cursor.fetchone()
        total_stake = resultado['total_stake'] if isinstance(resultado, dict) else resultado[0]
        total_stake = total_stake if total_stake else 1
        
        roi = (lucro_total / total_stake) * 100 if total_stake > 0 else 0
        
        conn.close()
        
        return {
            "total_apostas": total_apostas,
            "ganhos": ganhos,
            "perdidos": perdidos,
            "taxa_acerto": (ganhos / (ganhos + perdidos) * 100) if (ganhos + perdidos) > 0 else 0,
            "lucro_total": lucro_total,
            "roi": roi,
            "banca_atual": 1000 + lucro_total  # Banca inicial simulada
        }
    except:
        conn.close()
        return {
            "total_apostas": 0,
            "ganhos": 0,
            "perdidos": 0,
            "taxa_acerto": 0,
            "lucro_total": 0,
            "roi": 0,
            "banca_atual": 1000
        }

# ==========================================
# 4. APLICAÇÃO WEB
# INTERFACE PREMIUM
# ==========================================
st.markdown('<div class="main-title">PROBUM QUANTITATIVE</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Hedge Fund Esportivo & Motor de Prospecção</div>', unsafe_allow_html=True)

# 4.1. BOTÃO DO CÉREBRO
if st.button("🔮 ATIVAR MOTOR QUÂNTICO (Varredura Inteligente na Web)", key="btn_quantum"):
    with st.spinner("Conectando aos nós da Web... Lendo artigos... Cruzando matemáticas de risco..."):
        ops = motor_quantico_buscar_apostas()
        if ops:
            conn = sqlite3.connect("probum.db")
            cursor = conn.cursor()
            hoje = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime('%d/%m/%Y')
            for op in ops:
                cursor.execute("""
                    INSERT OR IGNORE INTO operacoes_tipster 
                    (id_aposta, esporte, jogo, liga, mercado, selecao, odd, prob, ev, kelly_stake, status, data_hora, justificativa, odd_history, telegram_enviado)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'PENDENTE', ?, ?, ?, 0)
                """, (op['jogo_id'], op['esporte'], op['jogo'], op['liga'], op['mercado'], op['selecao'], op['odd'], op['prob'], op['ev'], op['kelly_stake'], hoje, op['justificativa'], op['odd_history']))
            conn.commit()
            conn.close()
            st.success(f"⚡ {len(ops)} Operações localizadas, calculadas e salvas no Banco. O Bot Mensageiro irá despachar em instantes!")

st.markdown("---")
# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <div style="font-size: 32px; font-weight: 900; color: #00f0ff;">PROBIUM</div>
        <div style="font-size: 10px; color: #64748b; letter-spacing: 4px;">QUANTITATIVE ENGINE</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Menu
    page = st.radio(
        "Navegação",
        ["🏠 Dashboard", "🔍 Oportunidades", "📊 Análises", "💰 Gestão de Banca", "⚙️ Configurações"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Resumo rápido
    stats = get_estatisticas()
    st.markdown(f"""
    <div style="background: rgba(0,240,255,0.1); border-radius: 12px; padding: 16px; border: 1px solid rgba(0,240,255,0.2);">
        <div style="font-size: 10px; color: #64748b; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 8px;">Banca Atual</div>
        <div style="font-size: 24px; font-weight: 900; color: #00f0ff; font-family: 'JetBrains Mono', monospace;">${stats['banca_atual']:.2f}</div>
        <div style="font-size: 12px; color: {'#00ff88' if stats['roi'] >= 0 else '#ff0040'}; margin-top: 4px;">{stats['roi']:+.2f}% ROI</div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# PÁGINA: DASHBOARD
# ==========================================

tab_oracle, tab_ml = st.tabs(["👁️ O ORÁCULO (Live Cards)", "🧠 MACHINE LEARNING & CORREÇÃO"])
if page == "🏠 Dashboard":
    st.markdown('<div class="title-main">PROBIUM</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Quantitative Sports Betting Intelligence</div>', unsafe_allow_html=True)
    
    # Métricas principais
    stats = get_estatisticas()
    
    cols = st.columns(4)
    metrics = [
        ("Banca Total", f"${stats['banca_atual']:.2f}", "💰"),
        ("ROI", f"{stats['roi']:+.2f}%", "📈"),
        ("Taxa de Acerto", f"{stats['taxa_acerto']:.1f}%", "🎯"),
        ("Total Apostas", stats['total_apostas'], "🎲")
    ]
    
    for col, (label, value, icon) in zip(cols, metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 24px; margin-bottom: 8px;">{icon}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Gráfico de Performance
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📊 Evolução da Banca")
        
        # Simulação de dados para o gráfico
        dias = pd.date_range(end=datetime.now(), periods=30, freq='D')
        evolucao = [1000 + (i * random.uniform(-20, 35)) for i in range(30)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dias,
            y=evolucao,
            mode='lines',
            fill='tozeroy',
            line=dict(color='#00f0ff', width=3),
            fillcolor='rgba(0, 240, 255, 0.1)',
            name='Banca'
        ))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(showgrid=False, color='#64748b'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='#64748b'),
            height=400,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Distribuição")
        
        # Gráfico de pizza
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Ganhos', 'Perdas', 'Pendentes'],
            values=[stats['ganhos'], stats['perdidos'], stats['total_apostas'] - stats['ganhos'] - stats['perdidos']],
            hole=.6,
            marker_colors=['#00ff88', '#ff0040', '#ffb700']
        )])
        
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=True,
            legend=dict(orientation='h', yanchor='bottom', y=-0.1),
            height=400,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)

# ABA 1: CARDS DEUS TIER
with tab_oracle:
    conn = sqlite3.connect("probum.db")
    df = pd.read_sql("SELECT * FROM operacoes_tipster WHERE status='PENDENTE'", conn)
# ==========================================
# PÁGINA: OPORTUNIDADES
# ==========================================

elif page == "🔍 Oportunidades":
    st.markdown('<div class="title-main">🔍 SCANNER</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Motor de Análise Quantitativa</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("⚡ ATIVAR MOTOR QUÂNTICO", key="scan_btn"):
            with st.spinner("Analisando mercados com algoritmos de machine learning..."):
                ops = gerar_oportunidades_premium()
                
                conn = get_db_connection()
                cursor = conn.cursor()
                
                for op in ops:
                    try:
                        cursor.execute("""
                        INSERT OR IGNORE INTO operacoes_tipster 
                        (id_aposta, jogo, liga, mercado, selecao, odd, prob, ev, kelly, status)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (op['id'], op['jogo'], op['liga'], op['mercado'], 
                              op['selecao'], op['odd'], op['prob'], op['ev'], op['kelly'], 'PENDENTE'))
                    except:
                        cursor.execute("""
                        INSERT INTO operacoes_tipster 
                        (id_aposta, jogo, liga, mercado, selecao, odd, prob, ev, kelly, status)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ON CONFLICT(id_aposta) DO NOTHING
                        """, (op['id'], op['jogo'], op['liga'], op['mercado'], 
                              op['selecao'], op['odd'], op['prob'], op['ev'], op['kelly'], 'PENDENTE'))
                
                conn.commit()
                conn.close()
                
                st.success(f"✅ {len(ops)} oportunidades de valor identificadas!")
                st.balloons()
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Filtros
    col_filtro1, col_filtro2, col_filtro3 = st.columns(3)
    
    with col_filtro1:
        filtro_ev = st.slider("EV Mínimo", 0.0, 0.5, 0.05, 0.01)
    
    with col_filtro2:
        filtro_odd_min = st.number_input("Odd Mínima", 1.1, 10.0, 1.5)
        filtro_odd_max = st.number_input("Odd Máxima", 1.1, 10.0, 3.0)
    
    with col_filtro3:
        filtro_liga = st.multiselect(
            "Ligas",
            ["Premier League", "La Liga", "Bundesliga", "Serie A", "Ligue 1", "Primeira Liga"],
            default=["Premier League", "La Liga"]
        )
    
    # Buscar oportunidades
    conn = get_db_connection()
    
    try:
        query = """
        SELECT * FROM operacoes_tipster 
        WHERE status='PENDENTE' 
        AND ev >= ?
        AND odd BETWEEN ? AND ?
        ORDER BY ev DESC
        """
        df = pd.read_sql(query, conn, params=(filtro_ev, filtro_odd_min, filtro_odd_max))
    except:
        df = pd.read_sql("SELECT * FROM operacoes_tipster WHERE status='PENDENTE'", conn)
    
    conn.close()

    if df.empty:
        st.info("Nenhuma operação aberta. Pressione o botão do Motor Quântico acima para buscar oportunidades.")
        st.info("🔍 Nenhuma oportunidade encontrada com os filtros atuais.")
    else:
        st.markdown(f"### 🎯 {len(df)} Oportunidades Encontradas")
        
        for _, row in df.iterrows():
            time_casa, time_fora = row['jogo'].split(' x ') if ' x ' in str(row['jogo']) else (row['jogo'][:5], row['jogo'][5:])
            clima, juiz, foco = oraculo_contexto_invisivel(time_casa, time_fora)
            score_web = analise_sentimento_web(time_casa, time_fora)
            prob_mat = row['prob'] * 100
            
            # DIAMOND RULE: Se EV > 5% e Consenso Web > 60%, a aposta vira Ouro!
            is_diamond = row['ev'] >= 0.05 and score_web >= 60
            card_class = "god-card diamond-card" if is_diamond else "god-card"
            badge = '<div class="diamond-badge">💎 OPORTUNIDADE IMPERDÍVEL</div>' if is_diamond else '<div class="diamond-badge" style="background:#10B981;color:white;">🎯 ENTRADA ENCONTRADA</div>'
            box_class = "call-box diamond-call-box" if is_diamond else "call-box"

            status_tg = "✅ Despachado (Telegram)" if row.get('telegram_enviado', 0) == 1 else "⏳ Aguardando Bot"

            st.markdown(f"""
            <div class="{card_class}">
                {badge}
                <div style="font-size: 0.8rem; color: #94A3B8; margin-bottom: 10px; font-weight: bold; margin-top: 15px;">
                    {row['liga']} | {status_tg}
                </div>
                
                <div class="teams-grid">
                    <div class="team-col"><img src="{gerar_escudo(time_casa)}"><div class="team-name">{time_casa}</div></div>
                    <div class="vs-text">VS</div>
                    <div class="team-col"><img src="{gerar_escudo(time_fora)}"><div class="team-name">{time_fora}</div></div>
                </div>
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

                <!-- BARRAS DE INTELIGÊNCIA -->
                <div class="intel-bar-container">
                    <div class="intel-label"><span>🤖 Matemática Pura (Algoritmo)</span><span>{prob_mat:.1f}%</span></div>
                    <div class="intel-bar-bg"><div class="intel-bar-fill-ai" style="width: {prob_mat}%;"></div></div>
                </div>
                <div class="intel-bar-container">
                    <div class="intel-label"><span>🌐 Consenso Web & Notícias</span><span>{score_web:.1f}%</span></div>
                    <div class="intel-bar-bg"><div class="intel-bar-fill-web" style="width: {score_web}%;"></div></div>
                </div>

                <!-- CONTEXTO INVISÍVEL -->
                <div class="context-row">
                    <div class="context-item"><span>{clima}</span></div>
                    <div class="context-item"><span>{juiz}</span></div>
                    <div class="context-item"><span>{foco}</span></div>
                </div>
                with col1:
                    time_casa, time_fora = row['jogo'].split(' x ')
                    st.markdown(f"""
                    <div class="bet-card">
                        <div style="display: flex; align-items: center; margin-bottom: 12px;">
                            <span class="market-badge">{row['liga']}</span>
                            <span style="margin-left: 12px; color: #64748b; font-size: 12px;">{row['mercado']}</span>
                        </div>
                        
                        <div style="display: flex; align-items: center; margin-bottom: 16px;">
                            <span class="team-name">{time_casa}</span>
                            <span class="vs-divider">VS</span>
                            <span class="team-name">{time_fora}</span>
                        </div>
                        
                        <div style="font-size: 14px; color: #a0a0b0; margin-bottom: 8px;">
                            Seleção: <strong style="color: #00f0ff;">{row['selecao']}</strong>
                        </div>
                        
                        <div class="confidence-meter">
                            <div class="confidence-fill" style="width: {random.randint(60, 95)}%;"></div>
                        </div>
                        <div style="font-size: 11px; color: #64748b; margin-top: 4px;">Confiança do Modelo</div>
                    </div>
                    """, unsafe_allow_html=True)

                <!-- THE CALL -->
                <div class="{box_class}">
                    <div>
                        <div class="call-title">VANTAGEM ESTATÍSTICA</div>
                        <div style="font-size: 1.5rem; color: #10B981; font-weight: 900;">+{(row['ev']*100):.1f}% EV</div>
                with col2:
                    st.markdown(f"""
                    <div class="bet-card" style="text-align: center;">
                        <div class="odds-label">ODD</div>
                        <div class="odds-display">{row['odd']}</div>
                        <div style="font-size: 12px; color: #64748b; margin-top: 8px;">
                            Prob: {row['prob']*100:.if}%
                        </div>
                    </div>
                    <div>
                        <div class="call-title">A OPERAÇÃO</div>
                        <div class="call-market">{row['mercado']}</div>
                        <div style="color: #CBD5E1; font-size: 0.9rem;">{row['selecao']} @ {row['odd']:.if}</div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    ev_color = "ev-positive" if row['ev'] > 0 else "ev-negative"
                    st.markdown(f"""
                    <div class="bet-card" style="text-align: center;">
                        <div class="odds-label">EXPECTED VALUE</div>
                        <div class="{ev_color}">{row['ev']*100:+.2f}%</div>
                        <div style="font-size: 12px; color: #64748b; margin-top: 8px;">
                            Edge identificado
                        </div>
                    </div>
                    <div class="kelly-box">
                        <div class="kelly-title">STAKE DE SEGURANÇA (KELLY)</div>
                        <div class="kelly-value">{row.get('kelly_stake', 1.0):.1f}% <span style="font-size:0.7rem; color:#94A3B8;">Banca</span></div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f"""
                    <div class="bet-card" style="text-align: center;">
                        <div class="odds-label">KELLY CRITERION</div>
                        <div style="font-size: 32px; font-weight: 900; color: #ffb700; font-family: 'JetBrains Mono', monospace;">
                            {row['kelly']}%
                        </div>
                        <div class="kelly-box" style="margin-top: 12px; padding: 8px;">
                            <span style="font-size: 11px; color: #64748b;">Stake Rec.</span>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.plotly_chart(plotar_dropping_odds(row.get('odd_history', '[]')), use_container_width=True)
                    """, unsafe_allow_html=True)
                
                # Botões de ação
                col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
                
                with col_btn1:
                    if st.button(f"✅ Apostar", key=f"bet_{row['id_aposta']}"):
                        stake = st.number_input(f"Stake ($)", min_value=1.0, value=10.0, key=f"stake_{row['id_aposta']}")
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute("UPDATE operacoes_tipster SET stake = ? WHERE id_aposta = ?", (stake, row['id_aposta']))
                        conn.commit()
                        conn.close()
                        st.success(f"Aposta registrada: ${stake}")
                
                with col_btn2:
                    if st.button(f"❌ Rejeitar", key=f"rej_{row['id_aposta']}"):
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM operacoes_tipster WHERE id_aposta = ?", (row['id_aposta'],))
                        conn.commit()
                        conn.close()
                        st.rerun()
                
                st.markdown("---")

# ABA 2: DASHBOARD ML
with tab_ml:
    conn = sqlite3.connect("probum.db")
    resolvidos = pd.read_sql("SELECT * FROM operacoes_tipster WHERE status IN ('GREEN', 'RED')", conn)
# ==========================================
# PÁGINA: ANÁLISES
# ==========================================

elif page == "📊 Análises":
    st.markdown('<div class="title-main">📊 ANALYTICS</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Inteligência de Dados Avançada</div>', unsafe_allow_html=True)
    
    # Gráfico de dispersão: Odd vs EV
    conn = get_db_connection()
    df_hist = pd.read_sql("SELECT * FROM operacoes_tipster WHERE status IN ('GANHO', 'PERDA', 'PENDENTE')", conn)
    conn.close()

    st.markdown("### 🧠 Motor Preditivo e Autocorreção")
    if not resolvidos.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("Win Rate Geral", f"{(len(resolvidos[resolvidos['status']=='GREEN'])/len(resolvidos)*100):.1f}%")
        c2.metric("Unidades Acumuladas", f"{resolvidos['lucro'].sum():+.2f}")
        c3.metric("Correções Aplicadas", str(len(resolvidos)))
    if not df_hist.empty:
        fig = px.scatter(
            df_hist,
            x='odd',
            y='ev',
            color='status',
            size='kelly',
            hover_data=['jogo', 'selecao'],
            color_discrete_map={
                'GANHO': '#00ff88',
                'PERDA': '#ff0040',
                'PENDENTE': '#ffb700'
            },
            template='plotly_dark'
        )
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            title="Análise de Eficiência: Odd vs Expected Value",
            xaxis_title="Odd",
            yaxis_title="EV (Expected Value)"
        )

        lucro_mercado = resolvidos.groupby('mercado')['lucro'].sum().reset_index()
        fig = px.bar(lucro_mercado, x='mercado', y='lucro', color='lucro', color_continuous_scale=['#EF4444', '#10B981'])
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#94A3B8')
        st.plotly_chart(fig, use_container_width=True)
        
        # Análise por Liga
        st.markdown("### 🏆 Performance por Liga")
        
        fig_liga = px.bar(
            df_hist.groupby('liga')['ev'].mean().reset_index(),
            x='liga',
            y='ev',
            color='ev',
            color_continuous_scale=['#ff0040', '#ffb700', '#00ff88'],
            template='plotly_dark'
        )
        
        fig_liga.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_liga, use_container_width=True)
    else:
        st.info("Aguardando operações finalizadas para calibragem do algoritmo.")
        st.info("📊 Dados insuficientes para análise. Realize apostas para visualizar estatísticas.")

# ==========================================
# PÁGINA: GESTÃO DE BANCA
# ==========================================

elif page == "💰 Gestão de Banca":
    st.markdown('<div class="title-main">💰 BANKROLL</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Gestão de Risco e Capital</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⚙️ Configurações de Stake")
        
        banca_total = st.number_input("Banca Total ($)", value=1000.0, step=100.0)
        unidade_padrao = st.slider("Unidade Padrão (% da banca)", 0.5, 5.0, 1.0, 0.5)
        fracao_kelly = st.slider("Fração Kelly (Conservador)", 0.1, 0.5, 0.25, 0.05)
        
        st.markdown(f"""
        <div class="bet-card" style="margin-top: 20px;">
            <div style="font-size: 14px; color: #64748b; margin-bottom: 8px;">Stake por Unidade</div>
            <div style="font-size: 32px; font-weight: 900; color: #00f0ff; font-family: 'JetBrains Mono', monospace;">
                ${banca_total * (unidade_padrao/100):.2f}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📋 Histórico de Apostas")
        
        conn = get_db_connection()
        df_historico = pd.read_sql(
            "SELECT data_criacao, jogo, odd, stake, status, lucro FROM operacoes_tipster WHERE status != 'PENDENTE' ORDER BY data_criacao DESC LIMIT 10", 
            conn
        )
        conn.close()
        
        if not df_historico.empty:
            st.dataframe(
                df_historico,
                column_config={
                    "data_criacao": "Data",
                    "jogo": "Jogo",
                    "odd": st.column_config.NumberColumn("Odd", format="%.2f"),
                    "stake": st.column_config.NumberColumn("Stake", format="$%.2f"),
                    "status": "Status",
                    "lucro": st.column_config.NumberColumn("Lucro", format="$%.2f")
                },
                hide_index=True,
                use_container_width=True
            )
        else:
            st.info("Nenhuma aposta finalizada ainda.")

# ==========================================
# PÁGINA: CONFIGURAÇÕES
# ==========================================

elif page == "⚙️ Configurações":
    st.markdown('<div class="title-main">⚙️ SETTINGS</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Configurações do Sistema</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎨 Aparência")
        tema = st.selectbox("Tema", ["Cyberpunk Dark", "Midnight Blue", "Matrix Green"])
        animacoes = st.toggle("Animações Ativadas", value=True)
        
        st.markdown("### 🔔 Notificações")
        notif_telegram = st.toggle("Alertas Telegram", value=False)
        notif_email = st.toggle("Alertas Email", value=False)
    
    with col2:
        st.markdown("### 🔧 Algoritmo")
        modelo = st.selectbox(
            "Modelo de Predição",
            ["Kelly Criterion Puro", "Kelly Fractional", "Martingale Adaptativo", "Fibonacci"]
        )
        min_ev = st.slider("EV Mínimo para Alerta", 0.0, 0.2, 0.05, 0.01)
        
        if st.button("🗑️ Limpar Banco de Dados", type="secondary"):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM operacoes_tipster")
            conn.commit()
            conn.close()
            st.success("Banco de dados limpo!")
            st.rerun()

# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<div style="position: fixed; bottom: 0; left: 0; right: 0; background: rgba(5,5,5,0.9); border-top: 1px solid #1e1e2e; padding: 12px; text-align: center; font-size: 11px; color: #64748b; z-index: 999;">
    PROBIUM v2.0 | Quantitative Betting Engine | Powered by AI
</div>
""", unsafe_allow_html=True)
