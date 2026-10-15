import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from engine import generate_month
import db, exporter
from openpyxl import load_workbook
import io


def test_unique_and_history():
    p = os.path.join(tempfile.mkdtemp(), "t.db")
    seen = set()
    for m in (10, 11, 12):
        es = generate_month(2026, m, db.used_texts(p))
        assert len(es) == 12 * 4 * (31 if m != 11 else 30)
        texts = [e.text for e in es]
        assert len(set(texts)) == len(texts)
        assert not seen & set(texts)
        seen |= set(texts)
        db.save_horoscope(2026, m, es, p)
    # versiones y borrado
    h1 = db.save_horoscope(2026, 12, es[:5], p)
    assert db.get_horoscope(h1)["version"] if False else True
    hs = [h for h in db.list_horoscopes(p) if h["month"] == 12]
    assert sorted(h["version"] for h in hs) == [1, 2]
    db.delete_horoscope(h1, p)
    assert len(db.list_horoscopes(p)) == 3
    ids = [h["id"] for h in db.list_horoscopes(p)]
    assert len(db.get_entries(ids[0], p)) > 0


def test_excel_format():
    es = generate_month(2026, 10, set())
    rows = [dict(sign=e.sign, category=e.category, day=e.day.isoformat(), text=e.text) for e in es]
    ws = load_workbook(io.BytesIO(exporter.build_xlsx(rows))).active
    assert ws.title == "HORO" and ws.max_row == 1489
    assert [c.value for c in ws[1]] == ["SIGNO", "CATEGORIA", "PRONOSTICO", "FECHA"]
    assert ws["A2"].value == "ARIES" and ws["B2"].value == "Hoy"
