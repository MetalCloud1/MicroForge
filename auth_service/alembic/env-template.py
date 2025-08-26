# -----------------------------------------------------------------------------
# Template created by Gilbert Ramirez GitHub: https://github.com/MetalCloud1
# Licensed under CC BY-NC-ND (custom) – see LICENSE.md for details
# You may view, study, and modify this template.
# Substantial modifications that add new functionality or transform the project
# may be used as your own work, as long as the original template is properly
# acknowledged.
# -----------------------------------------------------------------------------

import os
import sys
import json
import base64
from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
from urllib.parse import quote_plus

# Adjust path to src
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
)
from src.database import Base
import src.models
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logger = logging.getLogger(__name__)

# Alembic config
config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

ENV = os.getenv("ENVIRONMENT", "development")

def _running_in_kubernetes() -> bool:
    """Detect if running inside Kubernetes"""
    if os.getenv("KUBERNETES_SERVICE_HOST"):
        return True
    if os.path.exists("/var/run/secrets/kubernetes.io/serviceaccount/token"):
        return True
    return False

# --- Secrets and configuration ---
if ENV == "production":
    # Placeholder for AWS Secrets Manager integration
    secret_name = os.getenv("AWS_SECRET_NAME", "<your-aws-secret-name>")
    region_name = os.getenv("AWS_REGION", "<your-aws-region>")
    # Users should replace this with their actual implementation
    secret = {
        "username": "<db-username>",
        "password": "<db-password>",
        "host": "<db-host>",
        "port": 5432,
        "db_name": "<db-name>",
    }
else:
    # For development or local testing
    forced_db_url = os.getenv("DATABASE_URL")
    if forced_db_url:
        DATABASE_URL = forced_db_url
        logger.info("Using DATABASE_URL from environment override.")
    else:
        in_k8s = _running_in_kubernetes()
        default_host = "postgres-service" if in_k8s else "localhost"

        # Environment variables as placeholders
        username = os.getenv("POSTGRES_USER", "<db-user>")
        raw_password = os.getenv("POSTGRES_PASSWORD", "<db-password-base64>")
        host = os.getenv("POSTGRES_HOST", default_host)
        port = int(os.getenv("POSTGRES_PORT", 5432))
        db_name = os.getenv("POSTGRES_DB", "<db-name>")

        # Try to decode base64, fallback to raw string
        try:
            password = base64.b64decode(raw_password).decode("utf-8")
        except Exception:
            password = raw_password

        secret = {
            "username": username,
            "password": password,
            "host": host,
            "port": port,
            "db_name": db_name,
        }

        user_esc = quote_plus(secret["username"])
        pwd_esc = quote_plus(secret["password"])
        host_part = f"{secret['host']}:{secret['port']}"
        DATABASE_URL = f"postgresql+psycopg2://{user_esc}:{pwd_esc}@{host_part}/{secret['db_name']}"

        logger.info(
            "Alembic: ENV=%s, running_in_k8s=%s, host=%s, user=%s, db=%s",
            ENV, in_k8s, secret["host"], secret["username"], secret["db_name"]
        )

# --- Alembic migration functions ---
def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
    