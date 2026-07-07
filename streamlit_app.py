"""Streamlit Cloud entry point."""

from pathlib import Path

exec(open(Path(__file__).parent / "clean_app.py", encoding="utf-8").read())
