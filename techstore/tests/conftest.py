"""Shared test setup, applied before any test module imports config.

- Tests never send Langfuse traces, even on a machine whose .env has keys.
- The FAQ shortcut is off for agents built with default settings: once FAQ answers are
  approved, questions like "Is delivery free?" would be answered without a model request
  and tests of the request path would silently stop testing it. CI never noticed because it
  does not install the embedding model. Tests of the FAQ itself turn it on explicitly.
"""
import os

os.environ["LANGFUSE_TRACING"] = "off"
os.environ["FAQ_SHORTCUT"] = "off"
