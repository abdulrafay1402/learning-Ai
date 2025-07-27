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
        goal = st.text_input("Career Goal (e.g., Web Developer, Data Scientist, AI Engineer)")
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
                
                # Create a concise prompt for learning path generation
                prompt = f"""
                Create a simple 5-6 bullet point learning path for becoming a {profile['goal']}.
                
                User Profile:
                - Age: {profile['age']} years old
                - Current Level: {profile['level']}
                - Current Skills: {profile['skills']}
                - Available Time: {profile['time']} hours per week
                
                Format: Just 5-6 bullet points with topic name and time estimate.
                Example:
                • HTML/CSS Basics (2 weeks)
                • JavaScript Fundamentals (3 weeks)
                • React Framework (4 weeks)
                
                Keep it short and practical. No long explanations.
                """

                # Create containers for better organization
                with st.container():
                    st.markdown("### 🎯 Generating Your Personalized Learning Path...")
                    
                    # Progress indicator
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        model = genai.GenerativeModel("gemini-2.0-flash")
                        
                        # Initialize variables
                        streamed_text = ""
                        chunk_count = 0
                        
                        # Show initial status
                        status_text.text("🔄 Connecting to AI...")
                        progress_bar.progress(0.1)
                        
                        # Stream the response with better error handling
                        try:
                            response = model.generate_content(prompt, stream=True)
                            
                            # Process streaming response
                            for chunk in response:
                                chunk_count += 1
                                
                                if hasattr(chunk, 'text') and chunk.text:
                                    streamed_text += chunk.text
                                    
                                    # Update progress (more realistic estimation)
                                    progress = min(0.1 + (chunk_count * 0.8 / 100), 0.9)
                                    progress_bar.progress(progress)
                                    status_text.text(f"🔄 Generating... ({chunk_count} chunks)")
                                    
                                    # Show live preview (limit to last 500 chars to avoid UI lag)
                                    preview = streamed_text[-500:] if len(streamed_text) > 500 else streamed_text
                                    st.markdown(f"**Live Preview:**\n{preview}")
                            
                            # Complete progress
                            progress_bar.progress(1.0)
                            status_text.text("✅ Generation Complete!")
                            
                            # Clear the live preview
                            st.empty()
                            
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
                        
                        except Exception as stream_error:
                            st.error(f"⚠️ Streaming error: {str(stream_error)}")
                            st.info("Trying non-streaming approach...")
                            
                            # Fallback to non-streaming approach
                            try:
                                response = model.generate_content(prompt)
                                if response.text:
                                    streamed_text = response.text
                                    
                                    # Process and display result
                                    roadmap_lines = [line.strip() for line in streamed_text.split("\n") if line.strip()]
                                    
                                    st.session_state.history.append({
                                        "goal": profile["goal"],
                                        "steps": roadmap_lines
                                    })
                                    
                                    st.markdown("### 🎯 Your Personalized Learning Path")
                                    st.markdown("---")
                                    
                                    for line in roadmap_lines:
                                        if line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
                                            st.markdown(f"**{line}**")
                                        elif line.startswith(('•', '-', '*', '→')):
                                            st.markdown(f"  {line}")
                                        else:
                                            st.markdown(line)
                                    
                                    st.success("✅ Learning Path Generated Successfully!")
                                else:
                                    st.error("❌ No response received from AI")
                            
                            except Exception as fallback_error:
                                st.error(f"⚠️ Fallback error: {str(fallback_error)}")
                    
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