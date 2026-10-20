"""Motor de generación de horóscopos mensuales.

Un pronóstico = A (situación + esfuerzo) + B (luz) + C opcional (astros o consejo).

Reglas:
  * NINGUNA oración se repite (ni dentro del mes, ni entre signos, ni respecto al historial).
  * La idea central de cada oración (situación, esfuerzo, resultado, consejo) se reparte en
    ciclo, de modo que no se repite dentro del mismo signo y categoría en el mes.
  * Dentro de un mismo texto no se repiten palabras clave entre oraciones (sin redundancias).
  * Tono: una situación o dificultad, el esfuerzo que pide y, al final, la luz.
"""
import calendar
import random
import re
import unicodedata
from dataclasses import dataclass
from datetime import date

from content import (
    A_FORMS, A_LEADS, A_TAILS, B_CONNECTORS, B_TAILS, C_FRAMES, C_LEADS,
    C_PLANETS, C_TIP_FRAMES, C_TIP_LEADS, CATEGORIES, CONTENT, SIGNS,
)

PATTERNS = [("A", "B"), ("A", "B", "C")]
PATTERN_WEIGHTS = [75, 25]
FALLBACK_PATTERN = PATTERNS[0]
VARIANT_TRIES = 60
TEXT_TRIES = 40

MONTHS_ES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]
MONTH_ABBR = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"]

# Palabras de uso común que sí pueden repetirse dentro de un texto.
_STOP = {
    "tendr", "habra", "convi", "deber", "tocar", "sera", "neces", "aunqu", "todo", "todas", "todos",
    "cuand", "menos", "mismo", "porqu", "hacia", "antes", "despu", "sobre", "entre", "desde", "hasta",
    "puede", "tiene", "tienes", "sient", "quier", "algun", "alguie", "pasar", "estar", "estas", "ahora",
    "cosas", "lleva", "luego", "donde", "ya que", "cuyo", "tiemp", "momen", "mejor", "ser", "otros",
    "aquel", "siemp", "nunca", "mucho", "poco", "ratos", "puedes", "hacer", "haces", "hecho", "sigue",
    "buena", "bueno", "justo", "cada", "tarde", "final", "lo", "algo", "pequen", "grand",
    "nuevo", "nueva", "viejo", "vieja", "tuyo", "tuya", "tuyos", "tuyas", "dices", "dicen", "estan", "esta",
    "casi", "tanto", "tanta", "veces", "forma", "manera", "parte", "lugar", "punto", "caso", "frent",
}


@dataclass(frozen=True)
class Entry:
    sign: str
    category: str
    text: str
    day: date


class ExhaustedError(RuntimeError):
    pass


def split_sentences(text):
    return [s for s in re.split(r"(?<=\.)\s+", text.strip()) if s]


def _cap(s):
    return s[0].upper() + s[1:]


def _norm(w):
    return "".join(c for c in unicodedata.normalize("NFD", w.lower()) if unicodedata.category(c) != "Mn")


def _stems(sentence):
    out = set()
    for w in re.findall(r"[a-záéíóúüñ]+", sentence.lower()):
        n = _norm(w)
        if n in ("dia", "noche", "manana"):  # evita "día ... día" en el mismo texto
            out.add(n)
        elif len(n) >= 5:
            st = n[:5]
            if st not in _STOP:
                out.add(st)
    return out


def _redundant(parts):
    """True si dos oraciones del mismo texto comparten alguna palabra clave (o ambas dicen 'pero')."""
    if len(re.findall(r"\bpero\b", " ".join(parts).lower())) > 1:
        return True
    seen = set()
    for p in parts:
        st = _stems(p)
        if seen & st:
            return True
        seen |= st
    return False


# ---- Constructores de oraciones (cada uno recibe rng, categoría y 'cabezas') ----
def _build_a(rng, cat, heads):
    c = CONTENT[cat]
    sit, eff = c["sit"][heads[0]], c["eff"][heads[1]]
    form = rng.choice(A_FORMS)
    tail = rng.choice(A_TAILS) if rng.random() < 0.4 else ""
    lead = rng.choice(A_LEADS)
    if _stems(sit) & (_stems(eff) | _stems(tail)):  # sin repetir ideas dentro de la misma oración
        return None
    t = rng.randrange(5)
    if t == 0:
        s = f"{lead}{sit}, y {form} {eff}{tail}"
    elif t == 1:
        s = f"{lead}{sit}; {form} {eff}{tail}"
    elif t == 2:
        s = f"{lead}{sit}, pero {form} {eff}{tail}"
    elif t == 3:
        s = f"Aunque {sit}, {form} {eff}{tail}"
    else:
        s = f"{lead}{sit}: {form} {eff}{tail}"
    if s.lower().count(" pero ") > 1:
        return None
    return _cap(s) + "."


def _pick_tail(rng, tails, p=0.45):
    return rng.choice(tails) if rng.random() < p else ""


def _build_b(rng, cat, heads):
    return _cap(f"{rng.choice(B_CONNECTORS)}{CONTENT[cat]['light'][heads[0]]}{_pick_tail(rng, B_TAILS)}") + "."


def _build_astro(rng, cat, heads):
    planet = rng.choice(C_PLANETS)
    return _cap(f"{rng.choice(C_LEADS)}{planet} {rng.choice(C_FRAMES)} {CONTENT[cat]['astro'][heads[0]]}") + "."


def _build_tip(rng, cat, heads):
    frame = rng.choice(C_TIP_FRAMES).format(x=CONTENT[cat]["tips"][heads[0]])
    return _cap(f"{rng.choice(C_TIP_LEADS)}{frame}") + "."


SLOTS = {
    "A": (_build_a, ("sit", "eff")),
    "B": (_build_b, ("light",)),
    "Castro": (_build_astro, ("astro",)),
    "Ctip": (_build_tip, ("tips",)),
}


class _Cycler:
    """Reparte las 'cabezas' en ciclos barajados: no repite hasta agotar todas."""

    def __init__(self, n, rng):
        self.n, self.rng, self.queue = n, rng, []

    def take(self):
        if not self.queue:
            self.queue = list(range(self.n))
            self.rng.shuffle(self.queue)
        return self.queue.pop()

    def put_back(self, head):
        self.queue.insert(0, head)


def generate_month(year, month, used_sentences=None, seed=None):
    """Devuelve la lista de Entry del mes (orden: signo, día, categoría).

    used_sentences: oraciones ya guardadas en el historial (no se reutilizan).
    """
    rng = random.Random(seed)
    used = set(used_sentences or ())
    n_days = calendar.monthrange(year, month)[1]
    entries = []
    cyclers = {}

    def draw(slot, cat, sign):
        """Una oración nueva para el slot, o None si no queda ninguna disponible."""
        build, keys = SLOTS[slot]
        cycs = [cyclers.setdefault((slot, k, cat, sign), _Cycler(len(CONTENT[cat][k]), rng)) for k in keys]
        skipped = []
        try:
            for _ in range(max(c.n for c in cycs)):
                heads = tuple(c.take() for c in cycs)
                for _ in range(VARIANT_TRIES):
                    s = build(rng, cat, heads)
                    if s is not None and s not in used:
                        return s, cycs, heads
                skipped.append(heads)
            return None
        finally:
            for heads in skipped:  # cabezas sin variantes libres: se reintentan más adelante
                for c, h in zip(cycs, heads):
                    c.put_back(h)

    def compose(pattern, cat, sign):
        for _ in range(TEXT_TRIES):
            parts, taken = [], []
            for slot in pattern:
                if slot == "C":
                    order = ["Castro", "Ctip"] if rng.random() < 0.5 else ["Ctip", "Castro"]
                    r = next((x for x in (draw(o, cat, sign) for o in order) if x), None)
                else:
                    r = draw(slot, cat, sign)
                if r is None:
                    release(taken, parts)
                    return None
                s, cycs, heads = r
                used.add(s)  # reserva inmediata: evita repetir dentro del mismo texto
                parts.append(s)
                taken.append((cycs, heads))
            if not _redundant(parts):
                return parts
            release(taken, parts)  # texto redundante: se descarta y se vuelve a armar
        return None

    def release(taken, parts):
        """Devuelve las oraciones y las cabezas reservadas por un texto descartado."""
        used.difference_update(parts)
        for cycs, heads in reversed(taken):
            for c, h in zip(cycs, heads):
                c.put_back(h)

    for sign in SIGNS:
        for d in range(1, n_days + 1):
            for cat in CATEGORIES:
                pattern = rng.choices(PATTERNS, PATTERN_WEIGHTS)[0]
                parts = compose(pattern, cat, sign)
                if parts is None and pattern != FALLBACK_PATTERN:
                    parts = compose(FALLBACK_PATTERN, cat, sign)
                if parts is None:
                    raise ExhaustedError(
                        "Se agotaron las oraciones únicas disponibles. "
                        "Elimina versiones antiguas o amplía content.py."
                    )
                entries.append(Entry(sign, cat, " ".join(parts), date(year, month, d)))
    return entries
