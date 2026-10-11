import streamlit as st
from pathlib import Path
from datetime import datetime

# Update this import to match the file where your function is defined
from src.pipelines.pipeline import run_research_pipeline


st.set_page_config(
    page_title="Research Agent",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Styling ----------
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }
    .hero {
        padding: 1.6rem;
        border: 1px solid rgba(128,128,128,0.3);
        border-radius: 16px;
        margin-bottom: 1.5rem;
        background: linear-gradient(
            120deg,
            rgba(70,100,180,0.16),
            rgba(100,70,180,0.08)
        );
    }
    .hero h1 {
        margin-bottom: 0.4rem;
    }
    .stage-card {
        padding: 1rem;
        border: 1px solid rgba(128,128,128,0.3);
        border-radius: 12px;
        min-height: 115px;
    }
    div.stButton > button[kind="primary"] {
        width: 100%;
        border-radius: 10px;
        min-height: 2.8rem;
    }
</style>
""", unsafe_allow_html=True)


# ---------- Helpers ----------
def as_text(value):
    """Convert common LangChain output types into displayable text."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if hasattr(value, "content"):
        return as_text(value.content)
    return str(value)


def download_report(state):
    topic = state.get("topic", "Research")
    report = as_text(state.get("report"))
    feedback = as_text(state.get("feedback"))

    return f"""# Research Report: {topic}

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}

{report}

---

# Critic Feedback

{feedback}
"""


# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🔎 Research Agent")
    st.caption("Multi-agent research workspace")
    st.divider()

    st.markdown("### Pipeline")
    st.markdown("1. 🌐 Search Agent")
    st.markdown("2. 📖 Reader Agent")
    st.markdown("3. ✍️ Writer Chain")
    st.markdown("4. 🧐 Critic Chain")

    st.divider()
    st.caption("Powered by your LangChain research pipeline.")


# ---------- Header ----------
st.markdown("""
<div class="hero">
    <h1>AI Research Workspace</h1>
    <p>Research a topic, extract deeper context, generate a report,
    and review it with a critic agent.</p>
</div>
""", unsafe_allow_html=True)


# ---------- Topic Input ----------
with st.form("research_form"):
    topic = st.text_area(
        "What would you like to research?",
        placeholder=(
            "e.g. How are AI agents changing cybersecurity "
            "operations in 2026?"
        ),
        height=100,
    )

    submitted = st.form_submit_button(
        "🚀 Start Research",
        type="primary",
        use_container_width=True,
    )


# ---------- Execute Pipeline ----------
if submitted:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        try:
            with st.status(
                "Running your research pipeline...",
                expanded=True,
            ) as status:
                st.write("🌐 Searching for recent, reliable sources...")
                st.write("📖 Reading relevant source content...")
                st.write("✍️ Generating the research report...")
                st.write("🧐 Reviewing the report...")

                result = run_research_pipeline(topic.strip())

                result["topic"] = topic.strip()
                st.session_state["research_result"] = result

                status.update(
                    label="Research pipeline completed!",
                    state="complete",
                    expanded=False,
                )

        except Exception as exc:
            st.error(f"Research failed: {exc}")
            st.exception(exc)


# ---------- Results ----------
result = st.session_state.get("research_result")

if result:
    st.divider()
    st.subheader(f"Research Results: {result.get('topic', 'Topic')}")

    report = as_text(result.get("report"))
    feedback = as_text(result.get("feedback"))
    search_results = as_text(result.get("search_results"))
    scraped_content = as_text(result.get("scraped_content"))

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Pipeline Stages", "4")

    with col2:
        st.metric("Search Output", f"{len(search_results):,} chars")

    with col3:
        st.metric("Reader Output", f"{len(scraped_content):,} chars")

    with col4:
        st.metric("Report Length", f"{len(report):,} chars")

    # Tabs for each stage
    tab1, tab2, tab3, tab4 = st.tabs([
        "🌐 Search Results",
        "📖 Scraped Content",
        "📝 Final Report",
        "🧐 Critic Feedback",
    ])

    with tab1:
        st.markdown("### Search Agent Output")
        if search_results:
            st.text_area(
                "Raw search output",
                value=search_results,
                height=400,
                key="search_output",
            )
        else:
            st.info("No search output was returned.")

    with tab2:
        st.markdown("### Reader Agent Output")
        if scraped_content:
            st.markdown(scraped_content)
        else:
            st.info("No scraped content was returned.")

    with tab3:
        st.markdown("### Final Research Report")
        if report:
            st.markdown(report)
            st.download_button(
                "⬇️ Download report as Markdown",
                data=download_report(result),
                file_name="research_report.md",
                mime="text/markdown",
                use_container_width=True,
            )
        else:
            st.warning("The writer did not return a report.")

    with tab4:
        st.markdown("### Critic Review")
        if feedback:
            st.markdown(feedback)
        else:
            st.info("No critic feedback was returned.")

    st.divider()
    if st.button("🗑️ Clear results"):
        del st.session_state["research_result"]
        st.rerun()

else:
    st.info(
        "Enter a topic above and start your first research run. "
        "Your search results, extracted content, report, and review "
        "will appear here."
    )
