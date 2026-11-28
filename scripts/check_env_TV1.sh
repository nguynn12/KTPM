#!/usr/bin/env bash
# Kiểm tra môi trường trước khi cài — TV1. Chạy: bash scripts/check_env_TV1.sh
echo "=== TV1 env check ==="
docker --version || echo "THIEU Docker"
docker compose version || echo "THIEU Docker Compose"
docker info >/dev/null 2>&1 \
  && echo "Docker daemon: RUNNING" \
  || echo "Docker daemon: CHUA CHAY -> mo Docker Desktop len"
python3 --version || echo "Python3: CHUA CO (can de chay Schemathesis + scripts/seed_and_verify_flows_TV1.py)"
schemathesis --version || echo "Schemathesis: CHUA CAI (pip install schemathesis==4.30.1)"
df -h / | awk 'NR==2{print "O dia trong: "$4" (can >= 10 GB)"}'
free -g | awk 'NR==2{print "RAM: "$2" GB (can >= 8 GB)"}'
