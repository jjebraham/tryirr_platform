# core/services/rates.py

import logging
from types import SimpleNamespace
from .wallex_brs import get_usdt_rate, get_lira_rate

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

