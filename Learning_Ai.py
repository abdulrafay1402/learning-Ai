import streamlit as st
from dotenv import load_dotenv
import os, google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# Initialize session state
if "profile" not in st.session_state:
    st.session_state.profile = {}   # stores user info
if "history" not in st.session_state:
    st.session_state.history = []   # stores all generated paths

# Set page configuration
st.set_page_config(
    page_title="Learning - AI",
    page_icon="Logo.jpg",
    layout="wide"
)

# Sidebar Navigation
st.sidebar.title("Learning - AI")
page = st.sidebar.selectbox(
    "Go to:",
    ["Home", "Profile Setup", "Get Recommendations", "History", "Settings", "About"]
)
st.sidebar.markdown("---")
st.sidebar.write("**Theme:**")
theme = st.sidebar.selectbox("Choose Theme:", ["Light", "Dark", "Auto"])

st.sidebar.markdown("---")
st.sidebar.info("Made with ❤️ using Streamlit")

# Page Content Logic
if page == "Home":
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.image("Logo.jpg", use_container_width=True)
    st.title("Learning - AI")
    st.header("AI based Learning Path Recommender")
    st.subheader("Welcome! Start your learning journey.")
    st.write(
        """
        This web app will help you generate **personalized learning paths** 
        based on your skills, interests, and career goals.
        """
    )
    st.button("Get Started")

elif page == "Profile Setup":
    st.title("📝 Profile Setup")
    st.write("Tell us about yourself so we can create the best path for you.")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name")
        age = st.number_input("Age", 15, 80)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        education = st.selectbox("Education", ["High School", "Undergraduate", "Post Graduate"])
        
    with col2:
        skills = st.text_area("Current Skills (comma separated)")
        level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"])
        goal = st.selectbox("Career Goal", ["Web Developer", "Data Scientist", "AI Engineer", "Mobile Developer", "Other"])
        time = st.slider("Hours available per week:", 1, 40, 5)

    if st.button("Save Profile"):
        st.session_state.profile = {
            "name": name,
            "age": age,
            "gender": gender,
            "education": education,
            "skills": skills,
            "level": level,
            "goal": goal,
            "time": time
        }
        st.success("Profile Saved Successfully ✅")


elif page == "Get Recommendations":
    st.title("🤖 AI-Powered Recommendations")

    if not st.session_state.profile:
        st.warning("⚠️ Please set up your profile first!")
    else:
        st.write(f"Hello **{st.session_state.profile['name']}**, ready for your learning path?")

        if st.button("🚀 Generate Learning Path"):
            profile = st.session_state.profile
            prompt = f"""
            Create a learning roadmap in bullet points (max 7-8 steps) for a {profile['level']} learner
            who wants to become a {profile['goal']}. 
            Current skills: {profile['skills']}.
            Education: {profile['education']}.
            Time available: {profile['time']} hours/week.
            For each step, include a free course/resource link.
            """

            # Placeholder for streaming output
            output_placeholder = st.empty()
            streamed_text = ""

            try:
                model = genai.GenerativeModel("gemini-2.0-flash")

                with st.spinner("✨ Generating..."):
                    # Streaming response
                    for chunk in model.generate_content(prompt, stream=True):
                        if chunk.text:
                            streamed_text += chunk.text
                            output_placeholder.markdown(f"### Your Roadmap:\n{streamed_text}")

                # Split into steps
                roadmap = [line.strip() for line in streamed_text.split("\n") if line.strip()]

                # Save to history
                st.session_state.history.append({
                    "goal": profile["goal"],
                    "steps": roadmap
                })

                st.success("✅ Learning Path Completed!")

            except Exception as e:
                st.error(f"⚠️ Error generating recommendations: {e}")

elif page == "History":
    st.title("📜 Your Past Learning Paths")

    if not st.session_state.history:
        st.info("No learning paths yet! Go to 'Get Recommendations' to generate one.")
    else:
        for idx, item in enumerate(st.session_state.history, 1):
            st.markdown(f"### {idx}. Goal: **{item['goal']}**")
            for step in item["steps"]:
                st.write(f"- {step}")
            st.markdown("---")

elif page == "Settings":
    st.title("⚙️ Settings")
    st.checkbox("Enable Notifications")
    st.checkbox("Show tips on dashboard")
    st.button("Clear All Data")

elif page == "About":
    st.title("ℹ️ About This App")
    st.markdown("""
        <div style='font-size:17px;'>
        <b>AI Learning Path Recommender</b><br>
        <b>Version:</b> 1.0.0<br>
        <b>Built with:</b> Streamlit, Firebase, and Gemini API<br><br>
        This application helps users discover <b>personalized learning paths</b> based on their unique skills, interests, and career aspirations. Whether you're a student, beginner, or professional, get tailored recommendations for courses, tools, and platforms to accelerate your learning journey!
        </div>
        <hr>
        <h4>Developer Info</h4>
        <ul>
        <li><b>Name:</b> Abdul Rafay</li>
        <li><b>Contact:</b> <a href='mailto:abdulrafayhere07@gmail.com'>Email:- abdulrafay</a></li>
        <li><b>GitHub:</b> <a href='https://github.com/abdulrafay1402' target='_blank'>github.com/abdulrafay1402</a></li>
        <li><b>Education:</b> Software Engineering student at FAST-NUCES, Karachi, Pakistan</li>
        </ul>
    """, unsafe_allow_html=True)

# Footer (appears on every page)
st.markdown("""
    <hr style='margin-top:40px;margin-bottom:10px;'>
    <div style='text-align:center; color:gray; font-size:16px;'>
        Created by Abdul Rafay | <a href='mailto:abdulrafayhere07@gmail.com'>Email:- abdulrafay</a> | <a href='https://github.com/abdulrafay1402' target='_blank'>GitHub</a><br>
        Software Engineering student at FAST-NUCES, Karachi, Pakistan<br>
        &copy; 2024-2025 Abdul Rafay. All rights reserved.
    </div>
""", unsafe_allow_html=True)