"""Initialize Database with Seed Data"""

from .base import SessionLocal
from .seed import seed_default_policy


def init_db():
    """Inicializa o banco com dados padrão"""
    db = SessionLocal()
    try:
        seed_default_policy(db)
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
