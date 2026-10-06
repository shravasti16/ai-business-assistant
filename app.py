import streamlit as st
from utils.llm import ask_ai
from utils.db import init_db, add_client, get_all_clients, update_status, delete_client

init_db()

st.set_page_config(page_title="AI Business Assistant", page_icon="🤖", layout="wide")

# ---------- CUSTOM STYLING ----------
st.markdown("""
    <style>
    .stApp {
        background-color: #0f172a;
    }
    [data-testid="stSidebar"] {
        background-color: #1e293b;
    }
    [data-testid="stSidebar"] * {
        color: #f1f5f9 !important;
    }
    [data-testid="stSidebar"] a {
        color: #38bdf8 !important;
    }
    h1, h2, h3, h4 {
        color: #38bdf8 !important;
    }
    .stApp p, .stApp label, .stMarkdown, .stCaption, span {
        color: #e2e8f0 !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 15px;
        font-weight: 600;
        padding: 10px 18px;
        background-color: #1e293b;
        border-radius: 8px 8px 0 0;
        color: #e2e8f0 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #38bdf8 !important;
        color: #0f172a !important;
    }
    .stButton>button {
        background-color: #38bdf8;
        color: #0f172a !important;
        border-radius: 8px;
        font-weight: 700;
        border: none;
        padding: 0.6em 1.6em;
        transition: 0.2s;
    }
    .stButton>button:hover {
        background-color: #0ea5e9;
        color: white !important;
        transform: scale(1.02);
    }
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        border-radius: 8px;
        background-color: #1e293b !important;
        color: white !important;
        border: 1px solid #334155 !important;
    }
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 8px;
        background-color: #1e293b !important;
    }
    .stSelectbox div[data-baseweb="select"] * {
        color: white !important;
    }
    [data-testid="stMetricValue"] {
        color: #38bdf8 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #e2e8f0 !important;
    }
    [data-testid="stDataFrame"] {
        background-color: #1e293b;
    }

    /* Deadline date box fix */
    div[data-testid="stDateInput"] input {
        background-color: #1e293b !important;
        border: 1px solid #38bdf8 !important;
    }

    /* Form submit (Add) button */
    [data-testid="stFormSubmitButton"] button {
        background-color: #38bdf8 !important;
        color: #0f172a !important;
        font-weight: 700 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.header("👋 About")
    st.write(
        "An AI-powered assistant that automates business workflows — "
        "proposal writing, profile branding, content creation and project tracking."
    )
    st.divider()
    st.write("**Built by:** Shravasti Athawale")
    st.write("🔗 [LinkedIn Profile](https://www.linkedin.com/in/shravasti-athawale-216557280)")
    st.divider()
    st.caption("Powered by Gemini AI")

    with st.expander("📄 Project Description"):
        st.markdown("""
**AI Business Automation Assistant**

An AI-powered web application built with Python and Streamlit that automates
repetitive business and career-branding tasks.

**Modules:**
- **Proposal Generator** — generates a personalised, client-ready proposal from a job/project description and your skills.
- **Profile Optimizer** — rewrites your headline and About section to be keyword-rich and achievement-based.
- **Post Generator** — creates engagement-focused posts with a hook, body, CTA and hashtags.
- **Project Tracker** — SQLite-backed dashboard to log clients/projects, track status, and view earnings.

**Tech stack:** Python, Streamlit, Google Gemini API, SQLite, Pandas
        """)

# ---------- HEADER ----------
st.title("🤖 AI Business Automation Assistant")
st.caption("An all-in-one toolkit for client communication, personal branding and project tracking.")
st.divider()

tabs = st.tabs(["📝 Proposal Generator", "💼 Profile Optimizer", "📢 Post Generator", "📊 Project Tracker"])

# ---------- TAB 1: PROPOSAL GENERATOR ----------
with tabs[0]:
    st.subheader("📝 Proposal Generator")
    st.caption("Paste any job or project description and get a personalised, client-ready proposal in seconds.")

    col1, col2 = st.columns(2)
    with col1:
        job = st.text_area("Paste the job/project description", height=200)
    with col2:
        skills = st.text_area("Your skills / experience", height=200)

    tone = st.selectbox("Tone", ["Professional", "Friendly", "Confident"])

    if st.button("Generate Proposal", key="proposal_btn"):
        if not job or not skills:
            st.warning("Please fill in both the description and your skills.")
        else:
            with st.spinner("Writing your proposal..."):
                system = (
                    "You are an expert proposal writer. "
                    "Write concise, personalised proposals that win clients."
                )
                user = f"""Project description:
{job}

My skills and experience:
{skills}

Tone: {tone}

Write a proposal of about 150 words. Start with a hook that shows I understood
the client's problem, mention 2-3 relevant skills, and end with a clear call to action."""
                result = ask_ai(system, user)
            st.success("Ready!")
            st.markdown(result)

# ---------- TAB 2: PROFILE OPTIMIZER ----------
with tabs[1]:
    st.subheader("💼 Profile Optimizer")
    st.caption("Turn your professional profile into a recruiter magnet with keyword-rich, achievement-based content.")

    headline = st.text_input("Current headline")
    about = st.text_area("Current About section", height=200)
    target_role = st.text_input("Target role (e.g. 'Data Analyst')")

    if st.button("Optimize Profile", key="optimize_btn"):
        if not headline or not about or not target_role:
            st.warning("Please fill in all three fields.")
        else:
            with st.spinner("Optimizing your profile..."):
                system = (
                    "You are a personal branding expert who helps candidates "
                    "get noticed by recruiters using keyword-rich, achievement-based profiles."
                )
                user = f"""Current headline:
{headline}

Current About section:
{about}

Target role: {target_role}

1. Rewrite the headline (max 220 characters), keyword-rich, specific to the target role.
2. Rewrite the About section (150-200 words), quantify achievements where possible,
   add a clear call to action at the end.
3. List 5 skills the profile should highlight for this target role.

Format the response with clear headings: "New Headline", "New About Section", "Recommended Skills"."""
                result = ask_ai(system, user)
            st.success("Ready!")
            st.markdown(result)

# ---------- TAB 3: POST GENERATOR ----------
with tabs[2]:
    st.subheader("📢 Post Generator")
    st.caption("Generate scroll-stopping professional posts with hooks, hashtags and CTAs.")

    topic = st.text_input("What should the post be about?")
    audience = st.text_input("Target audience (e.g. 'recruiters', 'clients')")
    post_tone = st.selectbox("Post tone", ["Professional", "Storytelling", "Motivational", "Casual"])

    if st.button("Generate Post", key="post_btn"):
        if not topic:
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Writing your post..."):
                system = (
                    "You are a content strategist who writes posts that get high "
                    "engagement — strong hooks, short punchy sentences, and clear takeaways."
                )
                user = f"""Topic: {topic}
Audience: {audience if audience else 'general professional audience'}
Tone: {post_tone}

Write a social media post with:
1. A strong 1-line hook (first line, must stop scrolling)
2. Body (short paragraphs, line breaks, 100-150 words)
3. A clear call to action at the end
4. 5 relevant hashtags

Format clearly with headings: "Hook", "Body", "Hashtags"."""
                result = ask_ai(system, user)
            st.success("Ready!")
            st.markdown(result)

# ---------- TAB 4: PROJECT TRACKER ----------
with tabs[3]:
    st.subheader("📊 Project Tracker")
    st.caption("Track your leads, projects and earnings — all in one place.")

    with st.form("add_client_form", clear_on_submit=True):
        st.write("**Add a new client/project**")
        col1, col2 = st.columns(2)
        with col1:
            c_name = st.text_input("Client name")
            c_status = st.selectbox("Status", ["Lead", "Proposal Sent", "In Progress", "Completed", "Paid"])
        with col2:
            c_project = st.text_input("Project name")
            c_amount = st.number_input("Amount (₹)", min_value=0.0, step=500.0)
        c_deadline = st.text_input("Deadline (YYYY-MM-DD)",placeholder="e.g. 2026-10-15")
        submitted = st.form_submit_button("Add")

        if submitted:
            if not c_name:
                st.warning("Client name is required.")
            else:
                add_client(c_name, c_project, c_status, c_amount, c_deadline)
                st.success("Added!")

    st.divider()
    st.write("### Pipeline Overview")

    df = get_all_clients()

    if df.empty:
        st.info("No entries added yet.")
    else:
        st.dataframe(df, use_container_width=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Projects", len(df))
        with col2:
            st.metric("Active Projects", len(df[df["status"].isin(["Lead", "Proposal Sent", "In Progress"])]))
        with col3:
            st.metric("Total Earnings (Paid)", f"₹{df[df['status'] == 'Paid']['amount'].sum():,.0f}")

        st.write("#### Update / Delete a row")
        col4, col5 = st.columns(2)
        with col4:
            selected_id = st.selectbox("Select ID", df["id"].tolist())
        with col5:
            new_status = st.selectbox("New status", ["Lead", "Proposal Sent", "In Progress", "Completed", "Paid"], key="update_status")

        col6, col7 = st.columns(2)
        with col6:
            if st.button("Update Status"):
                update_status(selected_id, new_status)
                st.rerun()
        with col7:
            if st.button("Delete Row"):
                delete_client(selected_id)
                st.rerun()

        st.write("#### Status Breakdown")
        st.bar_chart(df["status"].value_counts())