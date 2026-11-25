import html
import streamlit as st
from predictor import load_model, predict_url

st.set_page_config(page_title='PhishingDetector', page_icon='🛡️', layout='centered')

st.markdown('''<style>
.stApp {background:#0c1422;color:#e2e8f0;}
[data-testid="stHeader"] {background:transparent;}
.block-container {max-width:850px;padding-top:2.5rem;padding-bottom:2rem;}
.brand {display:flex;align-items:center;gap:14px;border-bottom:1px solid #29374a;padding-bottom:20px;}
.brand-icon {background:#19334b;border-radius:12px;padding:12px;display:flex;}
.brand-name {font-size:23px;font-weight:700;color:#f1f5f9;}
.muted {color:#a3b4c9;font-size:13px;}
.status {margin-left:auto;color:#36c99b;font-size:12px;white-space:nowrap;}
.hero {text-align:center;padding:34px 0 24px;}
.hero h1 {font-size:34px;color:#f1f5f9;margin:0 0 10px;}
.hero p {color:#a3b4c9;margin:0;}
[data-testid="stForm"] {background:#142032;border:1px solid #2d4057;border-radius:14px;padding:22px;}
.stTextInput input {background:#0c1422;color:#e2e8f0;}
.stButton button, [data-testid="stFormSubmitButton"] button {background:#2479b9;color:white;border:0;border-radius:8px;min-height:44px;}
.result {background:#142032;border:1px solid #29374a;border-radius:14px;padding:24px;margin:18px 0;}
.result-main {display:flex;align-items:center;gap:24px;margin:18px 0;flex-wrap:wrap;}
.result-copy {flex:1;min-width:180px;}
.result-copy h2 {margin:0 0 8px;font-size:24px;}
.result-copy p {color:#d2deec;margin:0 0 8px;}
.scores {display:grid;grid-template-columns:1fr 1fr;gap:16px;border-top:1px solid #29374a;padding-top:18px;}
.score {font-size:25px;font-weight:700;}
.analyzed {overflow-wrap:anywhere;color:#a3b4c9;font-size:12px;margin-top:16px;}
.stats {display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:24px;}
.stat {background:#142032;border:1px solid #29374a;border-radius:10px;padding:16px 8px;text-align:center;}
.stat strong {display:block;color:#e2e8f0;font-size:22px;}
.footer {text-align:center;color:#a3b4c9;font-size:12px;padding:20px 0;}
@media(max-width:480px){.hero h1{font-size:27px}.stat strong{font-size:17px}.stat .muted{font-size:11px}.result-main{gap:12px}}
</style>''', unsafe_allow_html=True)

@st.cache_resource
def get_artifact():
    return load_model()

try:
    artifact = get_artifact()
except Exception as error:
    st.error(f'No se pudo cargar el modelo: {error}')
    st.stop()

st.markdown('''<div class="brand"><div class="brand-icon"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#55c4e8" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-11V5l-8-3-8 3v6c0 7 8 11 8 11z"/><path d="m9 12 2 2 4-4"/></svg></div><div><div class="brand-name">PhishingDetector</div><div class="muted">URL Security Analyzer</div></div><div class="status">● Modelo activo</div></div><div class="hero"><h1>¿Es seguro este enlace?</h1><p>Analiza una dirección web antes de acceder a ella.</p></div>''', unsafe_allow_html=True)

with st.form('url_analysis'):
    url = st.text_input('Dirección URL', placeholder='https://example.com/login')
    submitted = st.form_submit_button('Analizar enlace', use_container_width=True)

if submitted:
    try:
        result = predict_url(url, artifact)
        probability = result['phishing_probability'] * 100
        legitimate = result['legitimate_probability'] * 100
        phishing = result['is_phishing']
        color = '#f36a73' if phishing else '#36c99b'
        title = 'Riesgo alto' if phishing else 'Riesgo bajo'
        description = ('El modelo detecta patrones asociados con phishing.' if phishing else 'El modelo clasifica esta URL como legítima.')
        advice = ('Evita introducir información personal y verifica el origen del enlace.' if phishing else 'Mantén las precauciones habituales. El resultado no garantiza seguridad.')
        safe_url = html.escape(result['url'])
        st.markdown(f'''<div class="result"><div class="muted">RESULTADO DEL ANÁLISIS</div><div class="result-main"><svg viewBox="0 0 140 140" width="140" height="140" role="img" aria-label="Probabilidad estimada de phishing: {probability:.2f}%"><circle cx="70" cy="70" r="57" stroke="#29394d" stroke-width="9" fill="none"/><circle cx="70" cy="70" r="57" stroke="{color}" stroke-width="9" fill="none" pathLength="100" stroke-dasharray="{probability:.6f} 100" transform="rotate(-90 70 70)" stroke-linecap="round"/><text x="70" y="69" text-anchor="middle" fill="#f1f5f9" font-size="23" font-weight="700">{probability:.2f}%</text><text x="70" y="86" text-anchor="middle" fill="#a3b4c9" font-size="10">Riesgo estimado</text></svg><div class="result-copy"><h2 style="color:{color}">{title}</h2><p>{description}</p><div class="muted">{advice}</div></div></div><div class="scores"><div><div class="muted">Legítima</div><div class="score" style="color:#36c99b">{legitimate:.2f}%</div></div><div><div class="muted">Phishing</div><div class="score" style="color:#f36a73">{probability:.2f}%</div></div></div><div class="analyzed">URL analizada: {safe_url}</div></div>''', unsafe_allow_html=True)
    except ValueError as error:
        st.warning(str(error))
    except Exception as error:
        st.error(f'No fue posible realizar el análisis: {error}')

st.caption('El análisis utiliza únicamente el texto de la URL. No visita el sitio ni consulta su reputación en tiempo real.')
st.markdown('''<div class="stats"><div class="stat"><strong>235.370</strong><span class="muted">URLs procesadas</span></div><div class="stat"><strong>99,62%</strong><span class="muted">Accuracy de prueba</span></div><div class="stat"><strong>99,55%</strong><span class="muted">F1-score</span></div></div>''', unsafe_allow_html=True)
with st.expander('Acerca del modelo'):
    st.write(f"Modelo cargado: {artifact.get('model_name', 'Modelo entrenado')}")
    st.write('Clasificación supervisada con TF-IDF de caracteres. Dataset PhiUSIIL de UCI. Evaluación sobre 47.074 URLs de prueba. Las métricas no garantizan el mismo rendimiento en dominios nuevos.')