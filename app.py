import streamlit as st

from smart_study_assistant import DistractionBlocker, LearnerProfile, SmartStudyAssistant


st.set_page_config(page_title="Smart Study Assistant", page_icon="📘", layout="wide")

assistant = SmartStudyAssistant()
if "blocker" not in st.session_state:
    st.session_state.blocker = DistractionBlocker()

st.title("📘 Smart Study Assistant")
st.caption("Interactive IIT-level study partner with adaptive guidance and focus tools.")

left, right = st.columns([1.25, 1])

with left:
    st.subheader("1) Your Profile")
    name = st.text_input("Name", "Student")
    level = st.selectbox("Current level", ["weak", "intermediate", "intelligent"])
    goals = st.text_input("Goal", "Crack IIT-JEE Advanced")
    style = st.selectbox("Preferred learning style", ["visual", "step-by-step", "practice-heavy"])
    subject = st.selectbox("Primary subject", ["Physics", "Chemistry", "Mathematics"])

    st.subheader("2) Paste Notes")
    notes = st.text_area(
        "Your notes",
        height=220,
        placeholder="Paste chapter notes here. I will summarize and generate IIT-level questions.",
    )

    if st.button("Generate Summary + Questions", type="primary"):
        with st.spinner("Analyzing your notes..."):
            summary = assistant.summarize_notes(notes)
            questions = assistant.generate_iit_level_questions(notes, count=5)

        st.markdown("### Smart Summary")
        for bullet in summary:
            st.write(bullet)

        st.markdown("### IIT-Level Practice Questions")
        for q in questions:
            st.markdown(f"**Q{q['id']} ({q['difficulty']})**: {q['question']}")

with right:
    st.subheader("3) Level Assessment")
    score = st.slider("Last mock-test score (%)", 0, 100, 60)
    assessed_level = assistant.assess_level(score)
    st.metric("Assessed level", assessed_level.upper())

    profile = LearnerProfile(name=name, level=assessed_level, goals=goals, preferred_style=style)

    if st.button("Build My Plan"):
        plan = assistant.build_study_plan(profile)
        rec = assistant.recommendations(subject, assessed_level)
        explainer = assistant.explain_for_student(f"Core concepts in {subject}", assessed_level)

        st.markdown("### Personalized Plan")
        st.write(plan)

        st.markdown("### Suggestions: YouTube")
        for item in rec["youtube"]:
            st.write(f"- {item}")

        st.markdown("### Suggestions: Books")
        for item in rec["books"]:
            st.write(f"- {item}")

        st.markdown("### Improvement Strategy")
        for tip in rec["tips"]:
            st.write(f"- {tip}")

        st.markdown("### Easy-to-Understand Explanation Mode")
        st.code(explainer)

    st.subheader("4) Distraction Restriction (Customizable)")
    apps = st.multiselect(
        "Apps to restrict during study",
        ["YouTube", "Instagram", "Facebook", "X/Twitter", "WhatsApp Web", "Reddit", "Gaming Apps"],
    )
    minutes = st.slider("Study lock duration (minutes)", 15, 240, 60, step=15)

    if st.button("Start Study Lock"):
        st.session_state.blocker.configure(apps, minutes)
        msg = st.session_state.blocker.start()
        st.success(msg)
        st.info("Note: This demo models the behavior. Connect platform APIs for hard blocking.")

    if st.button("End Study Lock"):
        msg = st.session_state.blocker.end()
        st.warning(msg)

st.markdown("---")
st.caption("Built with Streamlit. Student-friendly, interactive, and adaptable.")
