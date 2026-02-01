import random
from .models import db, ATM, NetworkStatus, Alert
from datetime import datetime

def check_atm_status():
    atms = ATM.query.all()
    if not atms:
        # Seed initial ATM
        atm = ATM(location="GCB Accra Main Branch", status="ONLINE", cash_level=85)
        db.session.add(atm)
        db.session.commit()
        atms = [atm]

    for atm in atms:
        # Simulate status check
        atm.status = random.choice(["ONLINE", "ONLINE", "ONLINE", "OFFLINE"])
        atm.cash_level = max(0, atm.cash_level - random.randint(0, 10))
        atm.last_checked = datetime.utcnow()

        if atm.status == "OFFLINE" or atm.cash_level < 20:
            msg = f"ATM {atm.location} needs attention: {atm.status}, Cash: {atm.cash_level}%"
            alert = Alert(type="ATM", message=msg, severity="CRITICAL")
            db.session.add(alert)

    db.session.commit()

def check_network():
    latency = random.randint(10, 500)
    status = "STABLE" if latency < 300 else "UNSTABLE"
    
    net = NetworkStatus(latency_ms=latency, status=status)
    db.session.add(net)

    if status == "UNSTABLE":
        alert = Alert(type="NETWORK", message=f"High latency detected: {latency}ms", severity="HIGH")
        db.session.add(alert)

    db.session.commit()
    return latency, status
