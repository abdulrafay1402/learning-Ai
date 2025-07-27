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
if "theme_preferences" not in st.session_state:
    st.session_state.theme_preferences = {
        "mode": "Dark",
        "primary_color": "#FF6B6B",
        "secondary_color": "#4ECDC4",
        "background_color": "#1E1E1E",
        "text_color": "#FFFFFF"
    }
if "page" not in st.session_state:
    st.session_state.page = "Home"  # stores current page
if "show_redirect" not in st.session_state:
    st.session_state.show_redirect = False  # controls redirect button visibility
if "show_success" not in st.session_state:
    st.session_state.show_success = False  # controls success message visibility

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
    ["Home", "Profile Setup", "Get Recommendations", "History", "Settings", "About"],
    index=["Home", "Profile Setup", "Get Recommendations", "History", "Settings", "About"].index(st.session_state.page)
)

# Update session state when page changes
if page != st.session_state.page:
    st.session_state.page = page
    st.rerun()

# Use session state page for navigation
page = st.session_state.page
st.sidebar.markdown("---")

# Theme Configuration - Collapsible
with st.sidebar.expander("🎨 Theme Settings", expanded=False):
    # Theme mode selection
    theme_mode = st.selectbox(
        "Theme Mode:",
        ["Light", "Dark", "Auto"],
        index=["Light", "Dark", "Auto"].index(st.session_state.theme_preferences["mode"]),
        help="Choose your preferred theme mode"
    )

    # Update session state and auto-adjust colors based on theme mode
    old_mode = st.session_state.theme_preferences["mode"]
    st.session_state.theme_preferences["mode"] = theme_mode
    
    # Auto-adjust colors when switching between light and dark modes
    if old_mode != theme_mode:
        if theme_mode == "Light":
            # Set light theme default colors
            st.session_state.theme_preferences.update({
                "primary_color": "#FF6B6B",
                "secondary_color": "#4ECDC4",
                "background_color": "#FFFFFF",
                "text_color": "#2C3E50"
            })
        elif theme_mode == "Dark":
            # Set dark theme default colors
            st.session_state.theme_preferences.update({
                "primary_color": "#FF6B6B",
                "secondary_color": "#4ECDC4",
                "background_color": "#1E1E1E",
                "text_color": "#FFFFFF"
            })
        st.rerun()

    # Preset themes
    st.markdown("**🎨 Quick Themes:**")
    preset_col = st.columns(2)
    with preset_col[0]:
        if st.button("Ocean", help="Blue ocean theme", key="ocean_btn"):
            st.session_state.theme_preferences.update({
                "primary_color": "#0066CC",
                "secondary_color": "#00CCFF",
                "background_color": "#F0F8FF",
                "text_color": "#003366"
            })
            st.rerun()
        if st.button("Forest", help="Green forest theme", key="forest_btn"):
            st.session_state.theme_preferences.update({
                "primary_color": "#228B22",
                "secondary_color": "#90EE90",
                "background_color": "#F0FFF0",
                "text_color": "#006400"
            })
            st.rerun()

    with preset_col[1]:
        if st.button("Sunset", help="Orange sunset theme", key="sunset_btn"):
            st.session_state.theme_preferences.update({
                "primary_color": "#FF6B35",
                "secondary_color": "#FFB347",
                "background_color": "#FFF8DC",
                "text_color": "#8B4513"
            })
            st.rerun()
        if st.button("Purple", help="Purple theme", key="purple_btn"):
            st.session_state.theme_preferences.update({
                "primary_color": "#8A2BE2",
                "secondary_color": "#DDA0DD",
                "background_color": "#F8F0FF",
                "text_color": "#4B0082"
            })
            st.rerun()

    # Custom colors section
    with st.expander("🎨 Custom Colors", expanded=False):
        primary_color = st.color_picker(
            "Primary Color", 
            st.session_state.theme_preferences["primary_color"]
        )
        secondary_color = st.color_picker(
            "Secondary Color", 
            st.session_state.theme_preferences["secondary_color"]
        )
        background_color = st.color_picker(
            "Background Color", 
            st.session_state.theme_preferences["background_color"]
        )
        text_color = st.color_picker(
            "Text Color", 
            st.session_state.theme_preferences["text_color"]
        )

        # Update session state with new colors
        st.session_state.theme_preferences.update({
            "primary_color": primary_color,
            "secondary_color": secondary_color,
            "background_color": background_color,
            "text_color": text_color
        })

        # Reset button
        if st.button("🔄 Reset to Default", help="Reset all theme settings to default", key="reset_btn"):
            st.session_state.theme_preferences = {
                "mode": "Dark",
                "primary_color": "#FF6B6B",
                "secondary_color": "#4ECDC4",
                "background_color": "#1E1E1E",
                "text_color": "#FFFFFF"
            }
            st.rerun()

# Apply theme
if theme_mode == "Dark":
    st.markdown("""
    <style>
    .stApp {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .stButton > button {
        background-color: """ + primary_color + """;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stSelectbox > div > div {
        background-color: #2D2D2D;
        color: #FFFFFF;
    }
    .stTextInput > div > div > input {
        background-color: #2D2D2D;
        color: #FFFFFF;
        border: 1px solid #444;
    }
    .stTextArea > div > div > textarea {
        background-color: #2D2D2D;
        color: #FFFFFF;
        border: 1px solid #444;
    }
    .stSlider > div > div > div > div {
        background-color: """ + secondary_color + """;
    }
    </style>
    """, unsafe_allow_html=True)
elif theme_mode == "Light":
    st.markdown("""
    <style>
    .stApp {
        background-color: """ + background_color + """;
        color: """ + text_color + """;
    }
    .stButton > button {
        background-color: """ + primary_color + """;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stSelectbox > div > div {
        background-color: #FFFFFF;
        color: """ + text_color + """;
    }
    .stTextInput > div > div > input {
        background-color: #FFFFFF;
        color: """ + text_color + """;
        border: 1px solid #ddd;
    }
    .stTextArea > div > div > textarea {
        background-color: #FFFFFF;
        color: """ + text_color + """;
        border: 1px solid #ddd;
    }
    .stSlider > div > div > div > div {
        background-color: """ + secondary_color + """;
    }
    .stProgress > div > div > div {
        background-color: """ + primary_color + """;
    }
    .stSuccess {
        background-color: #D4EDDA;
        color: #155724;
        border: 1px solid #C3E6CB;
        border-radius: 5px;
        padding: 10px;
    }
    .stWarning {
        background-color: #FFF3CD;
        color: #856404;
        border: 1px solid #FFEAA7;
        border-radius: 5px;
        padding: 10px;
    }
    .stError {
        background-color: #F8D7DA;
        color: #721C24;
        border: 1px solid #F5C6CB;
        border-radius: 5px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
else:  # Auto mode - follows system preference
    st.markdown("""
    <style>
    @media (prefers-color-scheme: dark) {
        .stApp {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }
        .stButton > button {
            background-color: """ + primary_color + """;
            color: white;
            border-radius: 10px;
            border: none;
            padding: 10px 20px;
            font-weight: bold;
        }
        .stSelectbox > div > div {
            background-color: #2D2D2D;
            color: #FFFFFF;
        }
        .stTextInput > div > div > input {
            background-color: #2D2D2D;
            color: #FFFFFF;
            border: 1px solid #444;
        }
        .stTextArea > div > div > textarea {
            background-color: #2D2D2D;
            color: #FFFFFF;
            border: 1px solid #444;
        }
        .stSlider > div > div > div > div {
            background-color: """ + secondary_color + """;
        }
    }
    @media (prefers-color-scheme: light) {
        .stApp {
            background-color: """ + background_color + """;
            color: """ + text_color + """;
        }
        .stButton > button {
            background-color: """ + primary_color + """;
            color: white;
            border-radius: 10px;
            border: none;
            padding: 10px 20px;
            font-weight: bold;
        }
        .stSelectbox > div > div {
            background-color: #FFFFFF;
            color: """ + text_color + """;
        }
        .stTextInput > div > div > input {
            background-color: #FFFFFF;
            color: """ + text_color + """;
            border: 1px solid #ddd;
        }
        .stTextArea > div > div > textarea {
            background-color: #FFFFFF;
            color: """ + text_color + """;
            border: 1px solid #ddd;
        }
        .stSlider > div > div > div > div {
            background-color: """ + secondary_color + """;
        }
        .stProgress > div > div > div {
            background-color: """ + primary_color + """;
        }
    }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.info("Made with ❤️ using Streamlit")

# Footer in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align:center; padding:10px; color:gray; font-size:14px;'>
Developed by <strong>Abdul Rafay</strong>
</div>
""", unsafe_allow_html=True)

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
    
    # Get Started button that redirects to Profile Setup
    if st.button("Get Started", key="get_started_btn"):
        # Change the page to Profile Setup
        st.session_state.page = "Profile Setup"
        st.rerun()

elif page == "Profile Setup":
    st.title("📝 Profile Setup")
    st.write("Tell us about yourself so we can create the best learning path for you.")
    st.info("💡 Fields marked with * are required")

    # Personal Information
    st.subheader("👤 Personal Information")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name *", placeholder="Enter your full name")
        age = st.number_input("Age *", 15, 80, 25)
        gender = st.selectbox("Gender *", ["Male", "Female", "Other", "Prefer not to say"])
        
    with col2:
        education = st.selectbox("Education Level *", [
            "High School", "Some College", "Associate's Degree", 
            "Bachelor's Degree", "Master's Degree", "PhD", "Other"
        ])
        experience = st.selectbox("Work Experience *", [
            "No Experience", "1-2 years", "3-5 years", 
            "6-10 years", "10+ years"
        ])

    # Learning Goals
    st.subheader("🎯 Learning Goals")
    goal = st.text_input("What career/job do you want to pursue? *", 
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

    # Validation
    required_fields = {
        "Full Name": name,
        "Career Goal": goal
    }
    
    missing_fields = [field for field, value in required_fields.items() if not value or value.strip() == ""]
    
    if st.button("Save Profile"):
        if missing_fields:
            st.error(f"❌ Please fill in the required fields: {', '.join(missing_fields)}")
        else:
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
            # Set flags for success display
            st.session_state.show_redirect = True
            st.session_state.show_success = True
            st.rerun()

# Show success message and celebrations if profile was just saved
if st.session_state.get("show_success", False):
    st.success("Profile Saved Successfully ✅")
    
    # Add balloons celebration
    st.balloons()
    
    # Add confetti effect
    st.markdown("""
    <div style="text-align: center; font-size: 24px; margin: 20px 0;">
    🎉 🎊 🎈 🎉 🎊 🎈
    </div>
    """, unsafe_allow_html=True)
    
    # Clear the success flag after showing
    st.session_state.show_success = False

# Show redirect button if profile was just saved
if st.session_state.get("show_redirect", False):
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Get Your Learning Path", key="go_to_recommendations", use_container_width=True):
            st.session_state.page = "Get Recommendations"
            st.session_state.show_redirect = False  # Clear the flag
            st.rerun()
    
    # Show a message to guide users
    st.info("💡 Click the button above to generate your personalized learning path!")


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
                - Each topic must include one specific course link (Udemy, Coursera, freeCodeCamp, etc.)
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
                - Include ONLY ONE course URL per topic (no duplicates)
                - Use actual course URLs from popular platforms (Udemy, Coursera, freeCodeCamp, etc.)
                - Total weeks should not exceed {profile['total_months']:.0f} months
                - No explanations or conversations
                - Just topic names, time estimates, and course links
                - Do NOT repeat URLs or add multiple links per topic
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
        <b>Built with:</b> Streamlit, and Gemini API<br><br>
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
        Developed by Abdul Rafay | <a href='mailto:abdulrafayhere07@gmail.com'>Email:- abdulrafay</a> | <a href='https://github.com/abdulrafay1402' target='_blank'>GitHub</a><br>
        Software Engineering student at FAST-NUCES, Karachi, Pakistan<br>
        &copy; 2024-2025 Abdul Rafay. All rights reserved.
    </div>
""", unsafe_allow_html=True)