#!/usr/bin/env python3
"""Script para seed do banco de dados"""
import sys
from pathlib import Path

# Adiciona src ao path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from credit_engine.infrastructure.database.init_db import init_db

if __name__ == "__main__":
    print("Seeding database with default policy...")
    init_db()
    print("✓ Default policy created successfully!")

