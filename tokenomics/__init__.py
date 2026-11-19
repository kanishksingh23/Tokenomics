"""Tokenomics: cut LLM tokens and cost without making answers worse.

The product. Every technique here works on an OpenAI-style request and knows nothing about
any particular app; `gateway.py` applies them to any app's traffic. TechStore (../techstore)
is the test app that uses this package.
"""
__version__ = "0.1.0"
