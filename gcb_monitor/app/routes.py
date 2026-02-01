from flask import Blueprint, jsonify, render_template
from .models import ATM, NetworkStatus, Alert
from .services import check_atm_status, check_network

app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/')
def dashboard():
    return render_template('dashboard.html')

@app_routes.route('/api/status')
def get_status():
    # Trigger checks
    check_atm_status()
    check_network()

    atms = ATM.query.all()
    network = NetworkStatus.query.order_by(NetworkStatus.checked_at.desc()).first()
    alerts = Alert.query.order_by(Alert.created_at.desc()).limit(5).all()

    return jsonify({
        'atms': [{
            'location': a.location,
            'status': a.status,
            'cash_level': a.cash_level
        } for a in atms],
        'network': {
            'latency': network.latency_ms if network else 0,
            'status': network.status if network else 'UNKNOWN'
        },
        'alerts': [{
            'message': al.message,
            'severity': al.severity,
            'time': al.created_at.strftime('%H:%M:%S')
        } for al in alerts]
    })

# Register blueprint (in __init__.py or here if handled elsewhere)
# For simplicity, we'll register it in __init__.py conceptually, but I need to fix __init__.py to import it.
