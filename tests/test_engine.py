import io
import os
import sys
import tempfile
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from openpyxl import load_workbook

import db
import exporter
from content import CATEGORIES, CONTENT, SIGNS
from engine import generate_month, split_sentences


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


def test_key_phrase_not_repeated_within_sign_and_month():
    from content import S1_LEADS, S1_VERBS, S2_FORMS, S3_TIMES

    def role(sent):
        if any(sent.startswith(t + ",") for t in S3_TIMES):
            return "s3_comp"
        if any(sent.startswith(l + ",") for l in S1_LEADS) and any(f" {v} " in sent for v in S1_VERBS):
            return "s1_comp"
        if any(f in sent.lower() for f in S2_FORMS):
            return "s2_effort"
        return None

    es = generate_month(2026, 10, set())
    for sign in SIGNS:
        for cat in CATEGORIES:
            used = Counter()
            for e in es:
                if e.sign != sign or e.category != cat:
                    continue
                for sent in split_sentences(e.text):
                    key = role(sent)
                    if key:
                        used.update(p for p in CONTENT[cat][key] if p in sent and sent.endswith(p + ".") or
                                    (key == "s2_effort" and p in sent))
            assert used and max(used.values()) <= 1, (sign, cat, used.most_common(1))


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
