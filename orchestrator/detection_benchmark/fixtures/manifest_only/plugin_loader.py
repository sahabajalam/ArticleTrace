"""Loads the face backend as a plugin — no static import ever names it."""
import importlib


def load_backend(name: str = "deepface"):
    mod = importlib.import_module(name)
    return getattr(mod, "DeepFace")
