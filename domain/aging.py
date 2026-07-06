"""Aging (antigüedad) del cobro pendiente."""
import pandas as pd

from config.umbrales import AGING_BUCKETS_DIAS, AGING_ETIQUETAS


def clasificar_aging(dias_pendiente: pd.Series,
                      bordes=AGING_BUCKETS_DIAS,
                      etiquetas=AGING_ETIQUETAS) -> pd.Categorical:
    """Clasifica días de antigüedad en buckets (0-30 / 31-60 / 61-90 / +90).

    >>> import pandas as pd
    >>> list(clasificar_aging(pd.Series([5, 45, 75, 120])))
    ['0-30 días', '31-60 días', '61-90 días', '+90 días']
    """
    return pd.cut(dias_pendiente, bins=[-1] + bordes[1:] + [10**6], labels=etiquetas)
