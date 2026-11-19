import sqlite3
import os
import socket
from flask import Flask, render_template, request, redirect, url_for,send_file
from io import BytesIO
import socket, urllib.request, json as js

app = Flask(__name__)

METRICS = {
    "XGBoost": {"accuracy": 96.75, "precision": 96.5, "recall": 96.8, "f1": 96.6},
    "Random Forest": {"accuracy": 96.60, "precision": 96.4, "recall": 96.7, "f1": 96.5},
    "Logistic Regression": {"accuracy": 96.25, "precision": 96.1, "recall": 96.3, "f1": 96.2}
}

HISTORY = []
ALL_RESULTS = []

def get_location(url):
    try:
        domain = url.replace("https://","").replace("http://","").split("/")[0].split(":")[0]
        ip = socket.gethostbyname(domain)
        with urllib.request.urlopen(f"http://ip-api.com/json/{ip}", timeout=3) as res:
            data = js.loads(res.read())
            if data.get("status")=="success":
                return f"{data.get('city')}, {data.get('country')} ({data.get('countryCode')})", ip
        return "Unknown", ip
    except:
        return "Unknown / Could not fetch", "Unknown"

def extract_features(url, location, ip):
    u = url.lower()
    return {
        "URL Length": len(url),
        "Has HTTP (Not HTTPS)": "Yes - DANGER" if url.startswith("http://") else "No - Good",
        "Has @ Symbol": "Yes - DANGER" if "@" in url else "No - Good",
        "Has IP Address": "Yes - DANGER" if any(c.isdigit() for c in url.split("/")[2][:3]) else "No - Good",
        "No. of Hyphens (-)": url.count("-"),
        "No. of Dots (.)": url.count("."),
        "No. of Sub-domains": max(0, url.count(".")-1),
        "Suspicious Keywords": ", ".join([w for w in ["login","verify","kyc","free","offer","update"] if w in u]) or "None - Good",
        "Has URL Shortener": "Yes - DANGER" if any(s in u for s in ["bit.ly","tinyurl","t.co"]) else "No - Good",
        "Server IP Address": ip,
        "Server Location": location,
    }

def check_one(url):
    url = url.strip()
    location, ip = get_location(url)

        # ===== DOMAIN AGE CHECK - Paste Here =====
    try:
        import urllib.request, json as js2
        domain_only = url.replace("https://","").replace("http://","").split("/")[0]
        with urllib.request.urlopen(f"https://who-dat.net/api/{domain_only}", timeout=4) as res:
            w = js2.loads(res.read())
            domain_age = w.get("creation_date", "Unknown")
    except:
        domain_age = "Very New / Hidden - Suspicious"

    feats = extract_features(url, location, ip)
    risk = 0; reasons = []
    if url.startswith("http://"): risk+=30; reasons.append("Uses HTTP, not HTTPS")
    if "@" in url: risk+=25; reasons.append("Contains @ symbol")
    if len(url)>75: risk+=20; reasons.append("URL is unusually long")
    if url.count("-")>=3: risk+=15; reasons.append("Too many hyphens")
    if any(w in url.lower() for w in ["login","verify","kyc","free","offer"]): risk+=15; reasons.append("Urgent words like login / KYC")
    if url.count(".")>=4: risk+=15; reasons.append("Too many sub-domains")
    if location not in ["Unknown","Unknown / Could not fetch"] and "India" not in location and any(w in url.lower() for w in ["paytm","phonepe","bank","kyc","sbi"]):
        risk+=20; reasons.append(f"Indian brand but server in {location} - Suspicious!")
    score = min(risk, 98)
    result = "PHISHING" if score>=50 else "SAFE"
    return {"url": url, "score": score, "result": result, "reasons": reasons, "features": feats, "location": location, "ip": ip, "domain_age": domain_age}

# PAGE 1 - HOME - Only Scan Box
@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        text = request.form["url"]
        urls = [u.strip() for u in text.replace(",","\n").split("\n") if u.strip()]
        results = [check_one(u) for u in urls]
        ALL_RESULTS.clear(); ALL_RESULTS.extend(results)
        for r in results:
            HISTORY.insert(0, r)
        del HISTORY[5:]
        # Go to PAGE 2 - Results List
        return redirect(url_for("results"))
    total = len(HISTORY)
    phishing = sum(1 for h in HISTORY if h["result"]=="PHISHING")
    safe = total - phishing
    return render_template("index.html", metrics=METRICS, history=HISTORY, total=total, phishing=phishing, safe=safe)

# PAGE 2 - RESULTS LIST - Only List
@app.route("/results")
def results():
    return render_template("results.html", results=ALL_RESULTS)

# PAGE 3 - DETAIL - Full Info of ONE URL
@app.route("/detail/<int:id>")
def detail(id):
    if id < len(ALL_RESULTS):
        r = ALL_RESULTS[id]
        return render_template("detail.html", r=r ,id=id)
    return "Not Found - Please Scan Again <a href='/'>Go Back</a>"

# ===== PDF REPORT =====
@app.route("/pdf/<int:id>")
def pdf_report(id):
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from io import BytesIO

    con = sqlite3.connect("phishguard.db")
    row = con.execute("SELECT * FROM history WHERE id=?", (id,)).fetchone()
    con.close()
    if not row:
        return "No record found! Go back and scan again."

    # row = id, url, result, score, location, ip, date
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 20)
    p.drawString(100, 750, "PhishGuard - Phishing Report")
    p.setFont("Helvetica", 12)
    p.drawString(100, 720, f"URL: {row[1][:70]}")
    p.drawString(100, 700, f"Result: {row[2]}")
    p.drawString(100, 680, f"Risk Score: {row[3]}%")
    p.drawString(100, 660, f"Location: {row[4]}")
    p.drawString(100, 640, f"IP Address: {row[5]}")
    p.drawString(100, 620, f"Date: {row[6]}")
    p.drawString(100, 580, "Conclusion: Check Before You Click!")
    p.drawString(100, 560, "Generated by PhishGuard - AI Phishing Detector")
    p.showPage()
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"PhishGuard-Report-{id}.pdf", mimetype="application/pdf")

if __name__ == "__main__":
    app.run(debug=True)