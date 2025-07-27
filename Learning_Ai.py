import streamlit as st
from dotenv import load_dotenv
import os, google.generativeai as genai
import time

# Load environment variables
load_dotenv()

# Check if API key is available
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("❌ GEMINI_API_KEY not found in environment variables!")
    st.info("Please create a .env file with your GEMINI_API_KEY")
    st.info(f"Current working directory: {os.getcwd()}")
    st.info(f"Files in directory: {os.listdir('.')}")
    st.stop()

# Configure the API
try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"❌ Error configuring API: {str(e)}")
    st.stop()


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
    st.write("Tell us about yourself so we can create the best learning path for you.")

    # Personal Information
    st.subheader("👤 Personal Information")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
        age = st.number_input("Age", 15, 80, 25)
        gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"])
        
    with col2:
        education = st.selectbox("Education Level", [
            "High School", "Some College", "Associate's Degree", 
            "Bachelor's Degree", "Master's Degree", "PhD", "Other"
        ])
        experience = st.selectbox("Work Experience", [
            "No Experience", "1-2 years", "3-5 years", 
            "6-10 years", "10+ years"
        ])

    # Learning Goals
    st.subheader("🎯 Learning Goals")
    goal = st.text_input("What career/job do you want to pursue?", 
                        placeholder="e.g., Full Stack Developer, Data Scientist, AI Engineer")
    
    # Current Skills Assessment
    st.subheader("💡 Current Skills")
    skills = st.text_area("What skills do you already have? (comma separated)", 
                         placeholder="e.g., Python, HTML, JavaScript, Excel")
    level = st.selectbox("How would you rate your current skill level?", 
                        ["Complete Beginner", "Some Experience", "Intermediate", "Advanced"])

    # Time Availability
    st.subheader("⏰ Time Availability")
    st.write("Let's calculate your total available learning time:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        hours_per_day = st.slider("Hours per day:", 0.5, 8.0, 2.0, 0.5)
    with col2:
        days_per_week = st.slider("Days per week:", 1, 7, 5)
    with col3:
        weeks_available = st.slider("Weeks available:", 1, 52, 12)
    
    # Calculate total time
    total_hours = hours_per_day * days_per_week * weeks_available
    total_months = weeks_available / 4.33  # Average weeks per month
    
    st.info(f"""
    📊 **Your Learning Time Summary:**
    - **Daily:** {hours_per_day} hours
    - **Weekly:** {hours_per_day * days_per_week} hours  
    - **Total Available:** {total_hours:.1f} hours ({total_months:.1f} months)
    """)

    if st.button("Save Profile"):
        st.session_state.profile = {
            "name": name,
            "age": age,
            "gender": gender,
            "education": education,
            "experience": experience,
            "skills": skills,
            "level": level,
            "goal": goal,
            "hours_per_day": hours_per_day,
            "days_per_week": days_per_week,
            "weeks_available": weeks_available,
            "total_hours": total_hours,
            "total_months": total_months
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
                
                # Create a comprehensive prompt for learning path generation
                prompt = f"""
                Create a detailed learning path for becoming a {profile['goal']}.
                
                USER PROFILE:
                - Age: {profile['age']} years old
                - Education: {profile['education']}
                - Experience: {profile['experience']}
                - Current Skills: {profile['skills']}
                - Skill Level: {profile['level']}
                - Total Available Time: {profile['total_hours']:.1f} hours ({profile['total_months']:.1f} months)
                - Daily: {profile['hours_per_day']} hours, Weekly: {profile['days_per_week']} days
                
                REQUIREMENTS:
                - Create exactly 5-6 learning topics
                - Each topic must include a specific course link (Udemy, Coursera, freeCodeCamp, etc.)
                - Distribute the {profile['total_hours']:.1f} hours across all topics
                - Respect the {profile['total_months']:.1f} month timeline
                - Start from {profile['level']} level
                
                RESPONSE FORMAT (exactly like this):
                • Topic Name (X weeks) - [Course Link]
                • Topic Name (X weeks) - [Course Link]
                • Topic Name (X weeks) - [Course Link]
                • Topic Name (X weeks) - [Course Link]
                • Topic Name (X weeks) - [Course Link]
                
                Rules:
                - Use bullet points (•) only
                - Include time estimate in weeks
                - Include actual course URLs from popular platforms
                - Total weeks should not exceed {profile['total_months']:.0f} months
                - No explanations or conversations
                - Just topic names, time estimates, and course links
                """

                # Create containers for better organization
                with st.container():
                    st.markdown("### 🎯 Generating Your Personalized Learning Path...")
                    
                    # Progress indicator
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        model = genai.GenerativeModel("gemini-2.0-flash")
                        
                        # Show processing steps with spinners
                        with st.spinner("🔍 Analyzing your profile..."):
                            time.sleep(1)
                            progress_bar.progress(0.2)
                            status_text.text("🔍 Analyzing your profile...")
                        
                        with st.spinner("🤖 Connecting to AI..."):
                            time.sleep(1)
                            progress_bar.progress(0.4)
                            status_text.text("🤖 Connecting to AI...")
                        
                        with st.spinner("📝 Generating learning path..."):
                            time.sleep(1)
                            progress_bar.progress(0.6)
                            status_text.text("📝 Generating learning path...")
                        
                        # Get the response
                        response = model.generate_content(prompt)
                        
                        with st.spinner("✨ Finalizing..."):
                            time.sleep(0.5)
                            progress_bar.progress(0.8)
                            status_text.text("✨ Finalizing...")
                        
                        # Complete progress
                        progress_bar.progress(1.0)
                        status_text.text("✅ Generation Complete!")
                        
                        # Get the response text
                        if response.text:
                            streamed_text = response.text
                            
                            # Process and format the final result
                            roadmap_lines = [line.strip() for line in streamed_text.split("\n") if line.strip()]
                            
                            # Save to history
                            st.session_state.history.append({
                                "goal": profile["goal"],
                                "steps": roadmap_lines
                            })
                            
                            # Display final formatted result
                            st.markdown("### 🎯 Your Personalized Learning Path")
                            st.markdown("---")
                            
                            for line in roadmap_lines:
                                if line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
                                    st.markdown(f"**{line}**")
                                elif line.startswith(('•', '-', '*', '→')):
                                    # Check if line contains a URL
                                    if 'http' in line:
                                        # Split the line into topic and link
                                        parts = line.split(' - ')
                                        if len(parts) >= 2:
                                            topic = parts[0].replace('•', '').strip()
                                            link = parts[1].strip()
                                            st.markdown(f"  **{topic}** - [{link}]({link})")
                                        else:
                                            st.markdown(f"  {line}")
                                    else:
                                        st.markdown(f"  {line}")
                                else:
                                    st.markdown(line)
                            
                            st.success("✅ Learning Path Generated Successfully!")
                            
                            # Add download option
                            if st.button("📥 Download Learning Path"):
                                # Create downloadable text
                                download_text = f"Learning Path for {profile['goal']}\n"
                                download_text += "=" * 50 + "\n\n"
                                download_text += streamed_text
                                
                                st.download_button(
                                    label="📄 Download as Text File",
                                    data=download_text,
                                    file_name=f"learning_path_{profile['goal'].replace(' ', '_')}.txt",
                                    mime="text/plain"
                                )
                        else:
                            st.error("❌ No response received from AI")
                    
                    except Exception as e:
                        st.error(f"⚠️ Error initializing AI model: {str(e)}")
                        st.info("Please check your API key and internet connection.")
                        st.code(f"Error details: {type(e).__name__}: {str(e)}")

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