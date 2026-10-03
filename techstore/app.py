"""Streamlit demo for the TechStore support agent (Phase 0).

    streamlit run app.py

The right-hand inspector is the important half. In Phase 0 it shows retrieval,
tokens, cost and latency. When the router lands in Week 4 it gains rows for
cache status, complexity score, tier, uncertainty signals and savings -- the
same panel, more fields. Keeping it here from the start means the response
schema grows with it instead of being retrofitted in Week 12.
"""
from __future__ import annotations

import streamlit as st

import config
from agent import SupportAgent

st.set_page_config(page_title="TechStore Support", page_icon="🎧", layout="wide")

PRESETS = [
    "Can I return opened headphones?",
    "Where is my order #48213?",
    "I was charged for order 48712 three times. Where is my money?",
    "X200 or Y500 for a noisy office?",
]


@st.cache_resource
def get_agent(model: str, retriever: str, top_k: int, mock: bool) -> SupportAgent:
    return SupportAgent(model=model, retriever_mode=retriever, top_k=top_k, mock=mock)


if "history" not in st.session_state:
    st.session_state.history = []
    st.session_state.spend = 0.0

# ---------------------------------------------------------------- sidebar
with st.sidebar:
    st.subheader("Try these")
    for i, preset in enumerate(PRESETS):
        if st.button(preset, use_container_width=True, key=f"preset_{i}"):
            st.session_state.pending = preset

    st.divider()
    st.subheader("⚙️ Configuration")
    model = st.selectbox("Model", [config.FRONTIER_MODEL, config.ECONOMY_MODEL])
    retriever = st.selectbox("Retriever", ["keyword", "embedding", "auto"],
                             help="keyword: BM25, no dependencies. embedding: MiniLM on CPU. "
                                  "auto: embedding if installed, else keyword.")
    top_k = st.slider("Documents retrieved", 1, 6, config.TOP_K)
    mock = st.toggle("Mock mode (no API key, no spend)", value=not bool(config.API_KEY))
    if mock:
        st.caption("⚠️ Stub model. Retrieval and cost accounting are real; the answer text is not.")
    elif not config.API_KEY:
        st.error("No OPENAI_API_KEY set. Enable mock mode or add a key to .env")

    if st.session_state.history and st.button("Clear conversation", use_container_width=True):
        st.session_state.history = []
        st.session_state.spend = 0.0
        st.rerun()

    st.divider()
    st.caption(f"Endpoint `{config.BASE_URL}`")
    st.caption(f"Pricing as of {config.PRICING_AS_OF}")

agent = get_agent(model, retriever, top_k, mock)

# chat_input must be called at the top level, not inside a column, or Streamlit
# renders it inline instead of pinning it to the bottom of the viewport.
typed = st.chat_input("Ask about orders, returns, products, billing...")
question = typed or st.session_state.pop("pending", None)

if question:
    with st.spinner("Thinking..."):
        result = agent.ask(question)
    st.session_state.history.append(result)
    st.session_state.spend += result.cost_usd

# ---------------------------------------------------------------- layout
left, right = st.columns([3, 2], gap="large")

with left:
    st.title("🎧 TechStore Support")
    st.caption("Phase 0 — direct to model. No router, no cache, no escalation.")

    if not st.session_state.history:
        st.info("Ask a question below, or pick one from the sidebar.")
    for turn in st.session_state.history:
        with st.chat_message("user"):
            st.write(turn.question)
        with st.chat_message("assistant"):
            st.write(turn.error or turn.answer)

with right:
    st.subheader("🔍 Inspector")
    if not st.session_state.history:
        st.caption("Shows what happened underneath each answer.")
    else:
        r = st.session_state.history[-1]
        titles = {d.id: d.title for d in agent.docs}

        st.caption(f"Latest turn · *{r.question[:60]}{'...' if len(r.question) > 60 else ''}*")

        a, b = st.columns(2)
        if r.cost_is_estimate:
            a.metric("Est. cost", f"~${r.cost_usd:.6f}",
                     help=f"Estimate. Prompt tokens counted locally; output assumed to be "
                          f"{config.MOCK_OUTPUT_TOKENS} tokens. A real answer may be longer, "
                          "and output costs 5x input on Sol.")
        else:
            a.metric("Cost", f"${r.cost_usd:.6f}",
                     help="From provider-reported token counts x the pricing table in config.py.")
        b.metric("Latency", "—" if r.cost_is_estimate else f"{r.latency_ms:.0f} ms")
        a.metric("Prompt tokens", r.prompt_tokens)
        b.metric("Output tokens (assumed)" if r.cost_is_estimate else "Output tokens",
                 r.completion_tokens)
        if r.cached_prompt_tokens:
            st.caption(f"{r.cached_prompt_tokens} prompt tokens served from provider cache "
                       "(billed at 10%)")

        st.divider()
        st.caption(f"**Retrieved documents** · top {len(r.retrieved)} of {len(agent.docs)}")
        for doc_id in r.retrieved:
            st.markdown(f"**{titles.get(doc_id, doc_id)}**  \n`{doc_id}`")
        if r.orders_used:
            st.caption("**Order records injected**")
            for o in r.orders_used:
                st.markdown(f"`#{o}`")
        st.caption(f"Retrieval {r.retrieval_ms:.2f} ms via **{r.retriever}** · `{r.model}`")

        st.divider()
        est = any(t.cost_is_estimate for t in st.session_state.history)
        st.metric("Est. session spend" if est else "Session spend",
                  f"{'~' if est else ''}${st.session_state.spend:.5f}",
                  help="Phase 0 has no router, so this is the baseline cost. "
                       "From Week 4 the inspector also shows what the router saved.")
        st.caption(f"{len(st.session_state.history)} question(s) this session")

        st.divider()
        st.caption("⬜ Cache · ⬜ Tier routing · ⬜ Escalation — arrive Weeks 4–8")
