# core/services/rates.py

import logging
from types import SimpleNamespace
from .wallex_brs import get_usdt_rate, get_lira_rate, round_to_nearest_10

logger = logging.getLogger(__name__)

def fetch_try_irr_rates():
    usdt = get_usdt_rate()
    lira = get_lira_rate()
    if not usdt or not lira:
        logger.warning("USDT or TL feed unavailable")
        return SimpleNamespace(TL_IRR=None, IRR_TL=None,
                               USDT_TL=None, TL_USDT=None)

    tmn_per_usdt = (usdt["buy"] + usdt["sell"]) / 2
    irr_per_usdt = tmn_per_usdt * 10
    irr_per_tl   = (lira["buy"] + lira["sell"]) / 2
    try:
        tl_per_irr = 1 / irr_per_tl
    except Exception:
        tl_per_irr = None

    tl_per_usdt = irr_per_usdt / irr_per_tl
    try:
        usdt_per_tl = 1 / tl_per_usdt
    except Exception:
        usdt_per_tl = None

    return SimpleNamespace(
        TL_IRR=irr_per_tl,
        IRR_TL=tl_per_irr,
        USDT_TL=tl_per_usdt,
        TL_USDT=usdt_per_tl,
    )


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

