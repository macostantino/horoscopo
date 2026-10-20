import io
import os
import re
import sys
import tempfile
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from openpyxl import load_workbook

import db
import exporter
from content import CATEGORIES, CONTENT, SIGNS
from engine import _redundant, generate_month, split_sentences


def _sentences(entries):
    return [s for e in entries for s in split_sentences(e.text)]


def test_no_sentence_repeats_across_months_and_history():
    p = os.path.join(tempfile.mkdtemp(), "t.db")
    seen = set()
    for m in range(1, 13):  # un año completo de historial
        es = generate_month(2026, m, db.used_sentences(p))
        sents = _sentences(es)
        assert len(sents) == len(set(sents)), "oración repetida dentro del mes"
        assert not seen & set(sents), "oración repetida respecto al historial"
        seen |= set(sents)
        db.save_horoscope(2026, m, es, p)
        assert len({e.text for e in es}) == len(es)


def test_key_ideas_not_repeated_within_sign_and_month():
    es = generate_month(2026, 10, set())
    for sign in SIGNS:
        for cat in CATEGORIES:
            c = CONTENT[cat]
            used = Counter()
            for e in es:
                if e.sign != sign or e.category != cat:
                    continue
                parts = split_sentences(e.text)
                used.update(("sit", p) for p in c["sit"] if p in parts[0].lower())
                used.update(("eff", p) for p in c["eff"] if p in parts[0].lower())
                used.update(("light", p) for p in c["light"] if p in parts[1].lower())
            assert used and max(used.values()) <= 1, (sign, cat, used.most_common(1))


def test_no_redundancy_inside_a_text():
    es = generate_month(2026, 10, set())
    for e in es:
        parts = split_sentences(e.text)
        assert 2 <= len(parts) <= 3
        assert not _redundant(parts), e.text
        assert len(re.findall(r"\bpero\b", e.text.lower())) <= 1, e.text


def test_versions_and_delete():
    p = os.path.join(tempfile.mkdtemp(), "t.db")
    es = generate_month(2026, 12, set())
    db.save_horoscope(2026, 12, es, p)
    h2 = db.save_horoscope(2026, 12, es[:5], p)
    assert sorted(h["version"] for h in db.list_horoscopes(p)) == [1, 2]
    db.delete_horoscope(h2, p)
    assert len(db.list_horoscopes(p)) == 1


def test_excel_format():
    es = generate_month(2026, 10, set())
    rows = [dict(sign=e.sign, category=e.category, day=e.day.isoformat(), text=e.text) for e in es]
    ws = load_workbook(io.BytesIO(exporter.build_xlsx(rows))).active
    assert ws.title == "HORO" and ws.max_row == 1489
    assert [c.value for c in ws[1]] == ["SIGNO", "CATEGORIA", "PRONOSTICO", "FECHA"]
    assert ws["A2"].value == "ARIES" and ws["B2"].value == "Hoy"
