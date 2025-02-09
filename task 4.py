import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from fpdf import FPDF
import numpy as np

# Initialize session state
if 'workout_data' not in st.session_state:
    st.session_state.workout_data = pd.DataFrame(columns=['Date', 'Exercise', 'Sets', 'Reps', 'Duration (min)'])

if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}

st.set_page_config(page_title="Workout Tracker", layout="wide")

# Landing Page
st.title("🏋️ AI-Powered Workout & Diet Tracker")
st.write("Your personal AI-driven fitness assistant to log workouts, track progress, and get personalized diet suggestions.")

st.image("https://source.unsplash.com/featured/?fitness,workout", use_column_width=True)

st.markdown("## Features:")
st.markdown("✔️ **Personalized Workout Plans** based on your fitness goals\n✔️ **AI-Generated Diet Plans** with Indian food recommendations\n✔️ **Progress Tracking** with charts and stats\n✔️ **Health-Conscious Adjustments** for conditions like diabetes & hypertension\n✔️ **Interactive AI Support** for exercise posture guidance & nutrition advice")

st.markdown("## Ready to Get Started?")
if st.button("🚀 Start Now", use_container_width=True):
    st.session_state['start'] = True

# Function to collect user profile
def collect_user_profile():
    st.subheader("👤 Personal Details")
    name = st.text_input("Enter your name:")
    age = st.number_input("Age", min_value=10, max_value=100, step=1)
    weight = st.number_input("Weight (kg)", min_value=30, max_value=200, step=1)
    height = st.number_input("Height (cm)", min_value=100, max_value=250, step=1)
    body_type = st.selectbox("Body Type", ["Skinny", "Average", "Muscular", "Overweight"])
    goal = st.selectbox("What is your fitness goal?", ["Lose Weight", "Build Muscle", "Healthy Living"])
    activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
    dietary_preference = st.selectbox("Dietary Preference", ["Vegetarian", "Non-Vegetarian", "Vegan", "Keto", "Balanced Diet"])
    health_issues = st.text_input("Any health issues (e.g., Diabetes, Hypertension)?")
    medications = st.text_input("Any medications taken?")
    
    if st.button("Save Profile", use_container_width=True):
        st.session_state.user_profile = {
            "Name": name,
            "Age": age,
            "Weight": weight,
            "Height": height,
            "Body Type": body_type,
            "Goal": goal,
            "Activity Level": activity_level,
            "Dietary Preference": dietary_preference,
            "Health Issues": health_issues,
            "Medications": medications
        }
        st.success("Profile saved successfully!")

# Function to log workouts
def log_workout():
    st.subheader("🏋️ Log Your Workout")
    date = st.date_input("Workout Date", datetime.date.today())
    exercise = st.text_input("Exercise Name")
    sets = st.number_input("Sets", min_value=1, max_value=10, step=1)
    reps = st.number_input("Reps", min_value=1, max_value=50, step=1)
    duration = st.number_input("Duration (min)", min_value=1, max_value=180, step=1)
    posture = st.text_area("Posture Details (Correct form tips)")
    
    if st.button("Add Workout", use_container_width=True):
        new_entry = pd.DataFrame({
            "Date": [date],
            "Exercise": [exercise],
            "Sets": [sets],
            "Reps": [reps],
            "Duration (min)": [duration],
            "Posture": [posture]
        })
        st.session_state.workout_data = pd.concat([st.session_state.workout_data, new_entry], ignore_index=True)
        st.success("Workout logged successfully!")

    # Display previous workouts
    if not st.session_state.workout_data.empty:
        st.subheader("📅 Your Workout History")
        st.dataframe(st.session_state.workout_data)

# Function to visualize progress
def visualize_progress():
    if st.session_state.workout_data.empty:
        st.warning("No workout data available!")
        return

    st.subheader("📊 Progress Tracker")
    df = st.session_state.workout_data.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    progress = df.groupby('Date').sum()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(progress.index, progress['Duration (min)'], marker='o', linestyle='-', color='b', label='Workout Duration')
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Minutes")
    ax.set_title("Workout Progress Over Time")
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.7)
    
    st.pyplot(fig)

# Function to suggest workout plan
def suggest_workout():
    if not st.session_state.user_profile:
        st.warning("Please fill out your profile first!")
        return
    
    st.subheader("🏋️ Personalized Workout Plan")
    goal = st.session_state.user_profile["Goal"]
    
    workout_plan = {
        "Lose Weight": [
            ("Running", "30-45 minutes of moderate-paced running."),
            ("Jump Rope", "10-15 minutes of high-intensity skipping."),
            ("HIIT", "20 minutes of interval training."),
            ("Cycling", "30-60 minutes of moderate-paced cycling.")
        ],
        "Build Muscle": [
            ("Squats", "4 sets of 8-12 reps."),
            ("Deadlifts", "3 sets of 5 reps."),
            ("Bench Press", "4 sets of 8-12 reps."),
            ("Pull-ups", "3 sets of 10-15 reps.")
        ],
        "Healthy Living": [
            ("Yoga", "30-60 minutes of yoga and stretching."),
            ("Walking", "30-45 minutes of brisk walking."),
            ("Stretching", "10-15 minutes of full-body stretching."),
            ("Dancing", "30 minutes of free-movement dancing.")
        ]
    }
    
    st.write(f"### {goal} Workout Plan")
    for exercise, details in workout_plan[goal]:
        st.write(f"- **{exercise}**: {details}")
    
    st.write("💡 Stick to this plan and track your progress!")

# Sidebar Navigation
st.sidebar.title("Navigation 🏃")
option = st.sidebar.radio("Go to:", ["Home", "User Profile", "Suggested Workout", "Log Workout", "View Progress", "Diet Suggestions"])

if option == "Home":
    st.experimental_rerun()
elif option == "User Profile":
    collect_user_profile()
elif option == "Suggested Workout":
    suggest_workout()
elif option == "Log Workout":
    log_workout()
elif option == "View Progress":
    visualize_progress()
elif option == "Diet Suggestions":
    suggest_diet()
