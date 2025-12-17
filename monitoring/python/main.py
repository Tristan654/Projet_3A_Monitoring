"""
Si tu changes le code tu es obligé de faire : docker-compose up --build -d


sudo docker logs -f python-blocker :
    Surveillance en direct : Elle affiche en temps réel tout ce que ton script Python écrit (print), comme la réception des alertes.
    Diagnostic : Elle te permet de vérifier si le "Robot" est bien en ligne ou s'il rencontre des erreurs de connexion SSH.
    Sans interruption : Elle te permet de voir ce qui se passe sans arrêter le conteneur (tu quittes la vue avec CTRL+C).
"""

from flask import Flask, request, jsonify
import paramiko

app = Flask(__name__)

# --- CONFIGURATION ---
ROUTER_IP = "10.100.1.2"
ROUTER_USER = "admin"
ROUTER_PASS = "ranout"
WEBHOOK_TOKEN = "123" # Ta clé de sécurité (Erreur de sécurité car MDP dans le code à regler plus tard)
# ----------------------

def execute_mikrotik_command(command):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ROUTER_IP, username=ROUTER_USER, password=ROUTER_PASS, timeout=5)
        
        ssh.exec_command(command)
        print(f"✅ Commande SSH exécutée sur MikroTik : {command}")
        ssh.close()
    except Exception as e:
        print(f"❌ Erreur SSH : {e}")

@app.route('/webhook', methods=['POST'])
def webhook():
    # 1. Vérification de la sécurité (Brain-protection)
    key = request.headers.get('X-Webhook-Token')
    if key != WEBHOOK_TOKEN:
        print("❌ Accès refusé : Mauvais Token")
        return "Accès refusé", 403

    # 2. Récupération des données JSON
    data = request.get_json(silent=True)
    if not data:
        return "Format JSON invalide", 400
    
    print(f"📦 Données reçues : {data}")

    # 3. Boucle sur les alertes
    for alert in data.get('alerts', []):
        alert_name = alert['labels'].get('alertname')
        status = alert.get('status')
        ifIndex = alert['labels'].get('ifIndex')
        
        print(f"🔔 Analyse : {alert_name} ({status}) sur Port {ifIndex}")

        # LOGIQUE DE RÉPONSE
        if alert_name in ["TrafficHigh", "UplinkSaturation"]:
            if status == 'firing':
                cmd = f'/interface disable [find default-name="ether{ifIndex}"]'
                execute_mikrotik_command(cmd)
            elif status == 'resolved':
                # Optionnel : réactiver le port si l'alerte disparaît
                cmd = f'/interface enable [find default-name="ether{ifIndex}"]'
                execute_mikrotik_command(cmd)
                
    # 4. Réponse obligatoire pour Flask
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)