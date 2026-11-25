import re
from pathlib import Path
from urllib.parse import urlsplit
import joblib

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL_PATH = PROJECT_ROOT / "models" / "phishing_detector.joblib"

def normalize_url(url: str) -> str:
    if not isinstance(url, str) or not url.strip():
        raise ValueError("Ingresa una URL; el campo no puede estar vacío.")
    value = url.strip()
    if any(ch.isspace() for ch in value):
        raise ValueError("La URL no debe contener espacios.")
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", value):
        value = "https://" + value
    parsed = urlsplit(value)
    if parsed.scheme.lower() not in ("http", "https") or not parsed.hostname:
        raise ValueError("URL inválida. Usa un dominio válido, por ejemplo https://example.com.")
    try:
        _ = parsed.port
    except ValueError as exc:
        raise ValueError("El puerto indicado en la URL no es válido.") from exc
    return value

def load_model(model_path=DEFAULT_MODEL_PATH):
    path = Path(model_path)
    if not path.exists():
        raise FileNotFoundError(
            f"No se encontró el modelo: {path}. Ejecuta el notebook de Colab y copia "
            "phishing_detector.joblib dentro de la carpeta models/."
        )
    artifact = joblib.load(path)
    if "pipeline" not in artifact:
        raise ValueError("El archivo del modelo no tiene el formato esperado.")
    return artifact

def predict_url(url: str, artifact: dict) -> dict:
    normalized = normalize_url(url)
    pipeline = artifact["pipeline"]
    prediction = int(pipeline.predict([normalized])[0])
    probability = float(pipeline.predict_proba([normalized])[0][1])
    return {
        "url": normalized,
        "is_phishing": prediction == 1,
        "label": "Phishing" if prediction == 1 else "Legítima",
        "phishing_probability": probability,
        "legitimate_probability": 1.0 - probability
    }
