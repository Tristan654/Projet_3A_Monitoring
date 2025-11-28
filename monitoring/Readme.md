Commande pour lancer les dockers (si le docker-compose s'appelle docker-compose pas besoin du -f): docker-compose -f mon_projet.yml up -d

🐳 Docker

Sert à lancer un seul container à la fois.

Exemple : lancer Prometheus seul

docker run -p 9090:9090 prom/prometheus


Tu dois gérer manuellement chaque container, réseau, volume, ports, etc.

📦 Docker Compose

Sert à lancer plusieurs containers ensemble comme un projet.

Exemple : Prometheus + Grafana + SNMP Exporter

docker compose up


Tu définis tout dans un seul fichier docker-compose.yml : images, volumes, ports, réseaux, liens entre containers.

Docker Compose s’occupe de tout orchestrer automatiquement.



| Service / Container | Rôle principal        | Fonction concrète                                                                                                                                 |
| ------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Prometheus**      | Collecte et stockage  | Scrape les métriques exposées par SNMP Exporter et autres services, les stocke dans sa base de données interne.                                   |
| **Grafana**         | Visualisation         | Lit les données de Prometheus et affiche des dashboards, graphiques, et alertes.                                                                  |
| **SNMP Exporter**   | Traducteur / Exporter | Interroge les périphériques via SNMP (switch, routeur, NAS…), transforme les OIDs en métriques Prometheus et les expose sur HTTP pour Prometheus. |
