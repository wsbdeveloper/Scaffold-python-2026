"""Application Entry Point"""

import sys
from pathlib import Path

import uvicorn

src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# outside of the container we can use the app directly
# from credit_engine.main import app

if __name__ == "__main__":
    uvicorn.run(
        # app,
        "credit_engine.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
