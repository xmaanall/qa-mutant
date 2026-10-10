import json
from pathlib import Path
import streamlit as st

from engine.scoring import summarize
from ai.analyzer import analyze_results

st.set_page_config(page_title="QA-MUTANT", page_icon="🧬", layout="wide")
st.title("🧬 QA-MUTANT")
st.caption("The AI that attacks your tests — experimental adversarial QA")

results_path = Path("experiments/baseline_results.json")
if not results_path.exists():
    st.warning("No experiment results found. Run: python -m engine.run_experiment")
    st.stop()

payload = json.loads(results_path.read_text(encoding="utf-8"))
results = payload["mutations"]
summary = summarize(results)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Mutation Score", f"{summary['mutation_score']}%")
c2.metric("Mutants Tested", summary["total"])
c3.metric("Killed", summary["killed"])
c4.metric("Survived", summary["survived"])

st.divider()
st.subheader("Mutation Lab")
for r in results:
    status = "🟢 KILLED" if r["status"] == "killed" else "🔴 SURVIVED"
    with st.expander(f"{r['mutation_id']} — {status} — {r['description']}"):
        st.code(f"{r['original']}  →  {r['replacement']}", language="python")
        st.write("**Execution evidence**")
        st.code(r["stdout"][-1500:] or r["stderr"][-1500:])

survivors = [r for r in results if r["status"] == "survived"]
st.divider()
st.subheader("AI-Assisted Gap Analysis")
if not survivors:
    st.success("No surviving mutants. The current test suite killed every valid mutant in this experiment.")
else:
    use_llm = st.checkbox("Use OpenAI API for live analysis (requires OPENAI_API_KEY and may incur API charges)", value=False)
    if st.button("Analyze surviving mutants"):
        analyses = analyze_results(results, use_llm=use_llm)
        for analysis in analyses:
            st.markdown(f"### {analysis['mutation_id']}: {analysis['finding']}")
            st.write(analysis["recommendation"])
            st.caption(f"Evidence: {analysis['evidence']} · Confidence: {analysis['confidence']} · Source: {analysis['provider']}")
    else:
        st.caption(f"{len(survivors)} surviving mutants are ready for analysis. Click the button to generate recommendations.")

st.divider()
st.info("AI recommendations are proposals. Execution results, not model output, determine whether a mutant was actually killed.")
