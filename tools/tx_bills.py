"""Texas cannabis bill tracker: pull bill histories from the Texas Legislature's official FTP feed
(ftp.legis.state.tx.us, Texas Legislative Council) and keep every cannabis / hemp / THC bill with its
stage and latest action.

usage: python3 tools/tx_bills.py [SESSION ...]      (default 90R; e.g. 89R for the 2025 session)
writes data/tx_bills_<SESSION>.json; data/tx_cache_<SESSION>.json remembers each file's listing date so
later runs only download bills that changed (the first run reads every bill once).
"""
import ftplib, io, json, os, re, sys, time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

HOST = "ftp.legis.state.tx.us"
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TYPES = ["house_bills", "senate_bills", "house_joint_resolutions", "senate_joint_resolutions"]
# what counts as a cannabis bill: caption or official subject index
RELEVANT = re.compile(r"marihuana|marijuana|cannabis|cannabidiol|tetrahydrocannabinol|\bTHC\b|\bhemp\b|"
                      r"compassionate[- ]use|low-THC|psilocyb", re.I)

def ftp():
    f = ftplib.FTP(HOST, timeout=60)
    f.login()
    return f

def listing(f, path):
    """[(name, 'MM-DD-YY HH:MMAM', is_dir)] from the server's DOS-style LIST output."""
    rows = []
    f.retrlines(f"LIST {path}", rows.append)
    out = []
    for r in rows:
        m = re.match(r"(\d\d-\d\d-\d\d)\s+(\d\d:\d\d[AP]M)\s+(<DIR>|\d+)\s+(.+)$", r.strip())
        if m:
            out.append((m.group(4), m.group(1) + " " + m.group(2), m.group(3) == "<DIR>"))
    return out

def stage(bill_id, actions):
    """Furthest point the bill reached, from its action descriptions (in order)."""
    origin = "House" if bill_id.startswith("H") else "Senate"
    other = "Senate" if origin == "House" else "House"
    st = "Filed"
    for a in actions:
        d, ch = a["description"].lower(), a["chamber"]
        here = origin if ch == origin[0] else other
        if "vetoed" in d:
            return "Vetoed"
        if "signed by the governor" in d or "effective" in d or "filed without the governor" in d:
            return "Law"
        if "sent to the governor" in d:
            st = "To governor"
        elif re.search(r"^passed|record vote|passed to engrossment|passed to third|read 3rd time.*passed", d) and "failed" not in d:
            if here == origin and st in ("Filed", "In committee", "Out of committee"):
                st = f"Passed {origin}"
            elif here == other and st not in ("To governor",):
                st = f"Passed {other}"
        elif "referred to" in d and st == "Filed":
            st = "In committee"
        elif re.search(r"reported favorably|reported from committee|committee report", d) and st == "In committee":
            st = "Out of committee"
        elif "referred to" in d and st == f"Passed {origin}":
            st = f"{other} committee"
    return st

def parse(xml_bytes):
    root = ET.fromstring(xml_bytes)
    bill = root.get("bill", "")                      # e.g. "89(R) HB 28"
    bid = bill.split(") ")[-1]
    caption = (root.findtext("caption") or "").strip()
    subjects = [s.text or "" for s in root.findall("subjects/subject")]
    acts = []
    for a in root.findall("actions/action"):
        num = a.findtext("actionNumber") or ""
        acts.append({"chamber": num[:1], "date": a.findtext("date") or "", "description": (a.findtext("description") or "").strip()})
    url = ""
    for v in root.findall("billtext/docTypes/bill/versions/version"):
        url = v.findtext("WebHTMLURL") or url
    return {"id": bid, "caption": caption, "subjects": subjects, "authors": root.findtext("authors") or "",
            "last_action": (root.findtext("lastaction") or "").strip(), "actions": acts, "text_url": url}

def run(session):
    cache_p = os.path.join(SITE, "data", f"tx_cache_{session}.json")
    cache = json.load(open(cache_p)) if os.path.exists(cache_p) else {}
    f = ftp()
    base = f"/bills/{session}/billhistory"
    try:
        top = {n for n, _, _ in listing(f, base)}
    except ftplib.error_perm:
        top = set()
    fetched = 0
    for t in TYPES:
        if t not in top:
            continue
        for group, _, is_dir in listing(f, f"{base}/{t}"):
            if not is_dir:
                continue
            for name, stamp, _ in listing(f, f"{base}/{t}/{group}"):
                if not name.endswith(".xml"):
                    continue
                key = f"{t}/{group}/{name}"
                if key in cache and cache[key]["stamp"] == stamp:
                    continue
                buf = io.BytesIO()
                for attempt in range(3):
                    try:
                        f.retrbinary(f"RETR {base}/{key}", buf.write); break
                    except (ftplib.all_errors) as e:
                        time.sleep(3); f = ftp(); buf = io.BytesIO()
                rec = parse(buf.getvalue())
                hit = bool(RELEVANT.search(rec["caption"] + " " + " ".join(rec["subjects"])))
                cache[key] = {"stamp": stamp, "bill": rec if hit else None}
                fetched += 1
    f.quit()
    json.dump(cache, open(cache_p, "w"), separators=(",", ":"))
    bills = []
    for key, v in cache.items():
        b = v["bill"]
        if not b:
            continue
        b = dict(b)
        b["stage"] = stage(b["id"], b["actions"])
        b["filed"] = b["actions"][0]["date"] if b["actions"] else ""
        b["actions"] = b["actions"][-6:]                 # keep the page light: latest six actions
        num = int(re.sub(r"\D", "", b["id"]) or 0)
        b["url"] = f"https://capitol.texas.gov/BillLookup/History.aspx?LegSess={session}&Bill={b['id'].replace(' ', '')}"
        b["_sort"] = (b["id"].split()[0], num)
        bills.append(b)
    bills.sort(key=lambda b: b.pop("_sort"))
    out = {"session": session, "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "source": "Texas Legislative Council (ftp.legis.state.tx.us)", "count": len(bills), "bills": bills}
    json.dump(out, open(os.path.join(SITE, "data", f"tx_bills_{session}.json"), "w"), indent=1)
    print(f"{session}: {fetched} files downloaded, {len(bills)} cannabis bills")

if __name__ == "__main__":
    for s in (sys.argv[1:] or ["90R"]):
        run(s)
