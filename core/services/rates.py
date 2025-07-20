# core/services/rates.py

import logging
from types import SimpleNamespace
from .wallex_brs import get_usdt_rate, get_lira_rate

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

