"""Motor de generación de horóscopos mensuales.

Garantiza que cada texto sea único dentro del mes y respecto a un conjunto
de textos ya usados (historial). Todos los textos siguen el patrón
situación -> esfuerzo -> luz (+ cierre opcional), de tono positivo.
"""
import calendar
import random
from collections import defaultdict
from dataclasses import dataclass
from datetime import date

from content import CATEGORIES, CONTENT, SIGN_CLOSERS, SIGNS

PATTERNS = [("s1", "s2", "s3"), ("s2", "s3", "s4"), ("s1", "s2", "s3", "s4")]
PATTERN_WEIGHTS = [4, 2, 3]
MAX_ATTEMPTS = 3000

MONTHS_ES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]
MONTH_ABBR = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"]


@dataclass(frozen=True)
class Entry:
    sign: str
    category: str
    text: str
    day: date


class ExhaustedError(RuntimeError):
    pass


def _pick_balanced(pool, usage, rng, avoid=None):
    """Elige un elemento del pool priorizando los menos usados (random en empates)."""
    candidates = [i for i in range(len(pool)) if i != avoid] or list(range(len(pool)))
    low = min(usage[i] for i in candidates)
    best = [i for i in candidates if usage[i] == low]
    return rng.choice(best)


def generate_month(year, month, used_texts=None, seed=None):
    """Devuelve la lista de Entry del mes (orden: signo, día, categoría)."""
    rng = random.Random(seed)
    used = set(used_texts or ())
    n_days = calendar.monthrange(year, month)[1]
    entries = []

    # Contadores de uso por categoría y ranura, para repartir parejo los fragmentos.
    usage = {c: {k: [0] * len(v) for k, v in CONTENT[c].items()} for c in CATEGORIES}
    sign_usage = {(s, c): [0] * len(SIGN_CLOSERS[s]) for s in SIGNS for c in CATEGORIES}

    for sign in SIGNS:
        last = {c: {} for c in CATEGORIES}
        for d in range(1, n_days + 1):
            for cat in CATEGORIES:
                pool = CONTENT[cat]
                text = None
                for attempt in range(MAX_ATTEMPTS):
                    pattern = rng.choices(PATTERNS, PATTERN_WEIGHTS)[0]
                    balanced = attempt < MAX_ATTEMPTS // 3
                    chosen, parts = {}, []
                    for slot in pattern:
                        if slot == "s4":
                            source = rng.choice(["cat", "sign"])
                            frases = pool["s4"] if source == "cat" else SIGN_CLOSERS[sign]
                            use = usage[cat]["s4"] if source == "cat" else sign_usage[(sign, cat)]
                            idx = _pick_balanced(frases, use, rng) if balanced else rng.randrange(len(frases))
                            chosen[slot] = (source, idx)
                            parts.append(frases[idx])
                        else:
                            frases = pool[slot]
                            avoid = last[cat].get(slot)
                            idx = (_pick_balanced(frases, usage[cat][slot], rng, avoid)
                                   if balanced else rng.randrange(len(frases)))
                            chosen[slot] = idx
                            parts.append(frases[idx])
                    candidate = " ".join(parts)
                    if candidate not in used:
                        text = candidate
                        break
                if text is None:
                    raise ExhaustedError(
                        "Se agotaron las combinaciones únicas disponibles. "
                        "Elimina versiones antiguas o amplía content.py."
                    )
                used.add(text)
                for slot, idx in chosen.items():
                    if slot == "s4":
                        source, i = idx
                        if source == "cat":
                            usage[cat]["s4"][i] += 1
                        else:
                            sign_usage[(sign, cat)][i] += 1
                    else:
                        usage[cat][slot][idx] += 1
                        last[cat][slot] = idx
                entries.append(Entry(sign, cat, text, date(year, month, d)))
    return entries
