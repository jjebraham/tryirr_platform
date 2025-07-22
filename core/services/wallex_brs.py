# core/services/wallex_brs.py

import logging
import requests
from typing import Dict

logger = logging.getLogger(__name__)

# ─── PROXY SETUP ────────────────────────────────────────────────────────────────
PROXY_URL = "http://jjebraham-9:Amir1234@p.webshare.io:80"
proxies   = {"http": PROXY_URL, "https": PROXY_URL}

# ─── WALLEX CONFIG ──────────────────────────────────────────────────────────────
WALLEX_API_KEY  = "15064|7tVDd4NDBYmATAe4lWTUQSTzj0v7ceTELEv6u6zG"
WALLEX_BASE_URL = "https://api.wallex.ir/v1"

# ─── FALLBACK & MAPPINGS ─────────────────────────────────────────────────────────
FALLBACK_USDT = {"buy": 8800, "sell": 8450}
FALLBACK_VALUES = {
    "gold-miskal": 28000000,
    "coin-emami": 72000000,
    "coin-baharazadi": 68000000,
    "coin-baharazadi-nim": 42000000,
    "coin-baharazadi-rob": 24000000,
    "coin-gerami": 13000000,
    "usd": 80000,
    "gbp": 107000,
    "euro": 91000,
    "try": 2137,
}
BRS_API_MAPPING = {
    "gold-miskal":   "IR_GOLD_MELTED",
    "coin-emami":    "IR_COIN_EMAMI",
    "coin-baharazadi":"IR_COIN_BAHAR",
    "coin-baharazadi-nim":"IR_COIN_HALF",
    "coin-baharazadi-rob":"IR_COIN_QUARTER",
    "coin-gerami":   "IR_COIN_1G",
    "usd":           "USD",
    "gbp":           "GBP",
    "euro":          "EUR",
    "try":           "TRY",
}

def round_to_nearest_10(v: float) -> int:
    return round(v/10) * 10

def round_to_nearest_50(v: float) -> int:
    return round(v/50) * 50

def get_brs_api_data() -> dict:
    url = "https://brsapi.ir/Api/Market/Gold_Currency.php?key=FreeEUI3NpParONhn01c4x3pcqbnni4A"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    try:
        r = requests.get(url, headers=headers, proxies=proxies, timeout=30)
        if r.status_code == 200:
            return r.json()
        logger.error("BRS API %s → %s", r.status_code, r.text[:200])
    except Exception as e:
        logger.error("BRS API error: %s", e)
    return {}

def get_rate(rate_type: str) -> float:
    symbol = BRS_API_MAPPING.get(rate_type)
    data   = get_brs_api_data()
    for section in ("gold", "currency"):
        for item in data.get(section, []):
            if item.get("symbol") == symbol:
                return float(item.get("price", 0))
    return FALLBACK_VALUES.get(rate_type, 0)

def get_usdt_rate() -> Dict[str,int]:
    # --- Primary: Wallex API ---
    try:
        headers = {"X-API-Key": WALLEX_API_KEY, "User-Agent": "Mozilla/5.0"}
        r = requests.get(f"{WALLEX_BASE_URL}/markets",
                         headers=headers, proxies=proxies, timeout=10)
        r.raise_for_status()
        syms = r.json()["result"]["symbols"]
        mkt  = syms.get("USDTTMN")
        price = float(mkt["stats"]["lastPrice"])
        return {
            "buy":  round_to_nearest_50(price * 1.01),
            "sell": round_to_nearest_50(price * 0.99),
        }
    except Exception:
        logger.warning("Wallex API failed, falling back…")

    # --- Fallback: Flask proxy (if you still have that) ---
    # …your flask fallback code here…

    # --- Fallback: BRS ---
    try:
        for itm in get_brs_api_data().get("currency", []):
            if itm.get("symbol") == "USDT_IRT":
                price = float(itm["price"]) / 10
                return {
                    "buy":  round_to_nearest_50(price * 1.02),
                    "sell": round_to_nearest_50(price * 0.97),
                }
    except Exception:
        logger.warning("BRS USDT fallback failed…")

    # --- Final fallback: static
    return FALLBACK_USDT

def get_lira_rate() -> Dict[str, float]:
    try:
        base_irr = get_rate("try")
        return {
            "buy":  round(base_irr * 1.02, 2),
            "sell": round(base_irr * 0.97, 2),
        }
    except Exception as e:
        logger.error("Could not fetch TL rate: %s", e)
        fb = FALLBACK_VALUES["try"]
        return {
            "buy":  round(fb * 1.02, 2),
            "sell": round(fb * 0.97, 2),
        }

