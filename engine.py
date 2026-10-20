"""Motor de generación de horóscopos mensuales.

Regla fundamental: NINGUNA oración se repite (ni dentro del mes, ni entre signos,
ni respecto al historial guardado). Además, la frase clave de cada oración
(complemento / esfuerzo / objeto) se reparte en ciclo, de modo que tampoco se
repite dentro del mismo signo y mes. Tono: situación -> esfuerzo -> luz.
"""
import calendar
import random
import re
from dataclasses import dataclass
from datetime import date

from content import (
    CATEGORIES, CONTENT, S1_LEADS, S1_VERBS, S2_FORMS, S2_PREFIXES, S2_TAILS,
    S3_TIMES, S3_VERBS, S4_TAILS, S4_VERBS, SIGN_LEADS, SIGN_PREDICATES,
    SIGN_SUBJECTS, SIGNS,
)

PATTERNS = [("s1", "s2", "s3"), ("s2", "s3", "s4"), ("s1", "s2", "s3", "s4")]
PATTERN_WEIGHTS = [4, 2, 3]
FALLBACK_PATTERN = PATTERNS[0]
VARIANT_TRIES = 60

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


def split_sentences(text):
    return [s for s in re.split(r"(?<=\.)\s+", text.strip()) if s]


def _join(verb, comp):
    """'da paso a' + 'el X' -> 'da paso al X'."""
    if verb.endswith(" a") and comp.startswith("el "):
        return f"{verb[:-2]} al {comp[3:]}"
    return f"{verb} {comp}"


def _cap(s):
    return s[0].upper() + s[1:]


# Cada constructor recibe (rng, cat, sign, head) y devuelve una oración candidata.
def _s1(rng, cat, sign, head):
    c = CONTENT[cat]
    return f"{rng.choice(S1_LEADS)}, {rng.choice(c['s1_subj'])} {_join(rng.choice(S1_VERBS), c['s1_comp'][head])}."


def _s2(rng, cat, sign, head):
    prefix, form, tail = rng.choice(S2_PREFIXES), rng.choice(S2_FORMS), rng.choice(S2_TAILS)
    if prefix.startswith("Aunque") and "aunque" in tail:
        tail = ""  # evita "Aunque cueste, ... aunque cueste al principio"
    return _cap(f"{prefix}{form} {CONTENT[cat]['s2_effort'][head]}{tail}.")


def _s3(rng, cat, sign, head):
    c = CONTENT[cat]
    return f"{rng.choice(S3_TIMES)}, {rng.choice(c['s3_subj'])} {_join(rng.choice(S3_VERBS), c['s3_comp'][head])}."


def _s4_cat(rng, cat, sign, head):
    return f"{rng.choice(S4_VERBS)} {CONTENT[cat]['s4_obj'][head]}{rng.choice(S4_TAILS)}."


def _s4_sign(rng, cat, sign, head):
    return f"{rng.choice(SIGN_LEADS)}, {rng.choice(SIGN_SUBJECTS[sign])} {SIGN_PREDICATES[head]}."


SLOTS = {
    "s1": (_s1, lambda cat, sign: len(CONTENT[cat]["s1_comp"])),
    "s2": (_s2, lambda cat, sign: len(CONTENT[cat]["s2_effort"])),
    "s3": (_s3, lambda cat, sign: len(CONTENT[cat]["s3_comp"])),
    "s4cat": (_s4_cat, lambda cat, sign: len(CONTENT[cat]["s4_obj"])),
    "s4sign": (_s4_sign, lambda cat, sign: len(SIGN_PREDICATES)),
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
        build, size = SLOTS[slot]
        key = (slot, cat, sign)
        cyc = cyclers.setdefault(key, _Cycler(size(cat, sign), rng))
        skipped = []
        try:
            for _ in range(cyc.n):
                head = cyc.take()
                for _ in range(VARIANT_TRIES):
                    s = build(rng, cat, sign, head)
                    if s not in used:
                        return s
                skipped.append(head)
            return None
        finally:
            for h in skipped:  # cabezas sin variantes libres: se reintentan más adelante
                cyc.put_back(h)

    def compose(pattern, cat, sign):
        parts = []
        for slot in pattern:
            if slot == "s4":
                order = ["s4cat", "s4sign"] if rng.random() < 0.5 else ["s4sign", "s4cat"]
                s = next((x for x in (draw(o, cat, sign) for o in order) if x), None)
            else:
                s = draw(slot, cat, sign)
            if s is None:
                return None
            used.add(s)  # reserva inmediata: evita repetir dentro del mismo texto
            parts.append(s)
        return parts

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
