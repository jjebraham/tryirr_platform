# core/services/rates.py

import logging
from types import SimpleNamespace
from .wallex_brs import get_usdt_rate, get_lira_rate, round_to_nearest_10

logger = logging.getLogger(__name__)

def fetch_try_irr_rates():
    usdt = get_usdt_rate()
    lira = get_lira_rate()
    if not usdt or not lira:
        logger.warning("USDT or TRY feed unavailable")
        return SimpleNamespace(TRY_IRR=None, IRR_TRY=None)

    tmn_per_usdt = (usdt["buy"] + usdt["sell"]) / 2
    tmn_per_try  = (lira["buy"] + lira["sell"]) / 2

    irr_per_try = tmn_per_try * 10
    try:
        try_per_irr = 1 / irr_per_try
    except Exception:
        try_per_irr = None

    return SimpleNamespace(TRY_IRR=irr_per_try, IRR_TRY=try_per_irr)


def fetch_all_rates():
    """Return detailed rates used across the platform.

    The result contains six values mirroring the ones provided by the
    Telegram bot for buying/selling TRY and USDT.  It uses the same
    formulas so the website and bot stay in sync.
    """

    usdt = get_usdt_rate()
    lira = get_lira_rate()
    if not usdt or not lira:
        logger.warning("USDT or TRY feed unavailable")
        return None

    tmn_per_usdt = (usdt["buy"] + usdt["sell"]) / 2
    tmn_per_try = (lira["buy"] + lira["sell"]) / 2

    usdt_irr = tmn_per_usdt * 10  # Rial price of 1 USDT
    usdt_try = tmn_per_usdt / tmn_per_try  # TRY price of 1 USDT

    eff = usdt_irr / 10  # back to Toman

    return {
        "buy_lira": round_to_nearest_10((eff / usdt_try) * 1.02),
        "sell_lira": round_to_nearest_10((eff / usdt_try) * 0.97),
        "buy_usdt": round_to_nearest_10(eff * 1.01),
        "sell_usdt": round_to_nearest_10(eff * 0.99),
        "try_to_usdt": round(usdt_try * 1.02, 2),
        "usdt_to_try": round(usdt_try * 0.98, 2),
    }

