import streamlit as st

# --------------------------- #
#       APP CONFIG            #
# --------------------------- #
st.set_page_config(page_title="Quiz Master 🧠", page_icon="🎯", layout="centered")

st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    }
    .title {
        text-align: center;
        color: #1E88E5;
        font-size: 40px !important;
        font-weight: bold;
        margin-bottom: 30px;
    }
    .question {
        color: #333333;
        font-size: 20px;
        font-weight: 600;
    }
    .footer {
        text-align: center;
        margin-top: 40px;
        color: grey;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# --------------------------- #
#       QUIZ DATA             #
# --------------------------- #
quiz_data = [
    {"question": "Which planet is known as the Red Planet?",
     "options": ["Earth", "Mars", "Jupiter", "Saturn"],
     "answer": "Mars"},
    {"question": "Who developed the theory of relativity?",
     "options": ["Isaac Newton", "Albert Einstein", "Galileo", "Marie Curie"],
     "answer": "Albert Einstein"},
    {"question": "What is the capital of France?",
     "options": ["Paris", "London", "Berlin", "Madrid"],
     "answer": "Paris"},
    {"question": "Which is the largest ocean on Earth?",
     "options": ["Indian Ocean", "Atlantic Ocean", "Arctic Ocean", "Pacific Ocean"],
     "answer": "Pacific Ocean"},
    {"question": "Who wrote 'Romeo and Juliet'?",
     "options": ["Charles Dickens", "William Shakespeare", "Leo Tolstoy", "Mark Twain"],
     "answer": "William Shakespeare"}
]

# --------------------------- #
#     SESSION VARIABLES       #
# --------------------------- #
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "answers" not in st.session_state:
    st.session_state.answers = [None] * len(quiz_data)
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# Clamp index to valid range
st.session_state.current_q = max(0, min(st.session_state.current_q, len(quiz_data) - 1))

# --------------------------- #
#       MAIN UI LAYOUT        #
# --------------------------- #
st.markdown('<div class="main">', unsafe_allow_html=True)
st.markdown('<h1 class="title">🎯 Ultimate Quiz Challenge</h1>', unsafe_allow_html=True)

if not st.session_state.submitted:
    q_index = st.session_state.current_q
    q_data = quiz_data[q_index]

    st.markdown(f"<p class='question'>Q{q_index + 1}. {q_data['question']}</p>", unsafe_allow_html=True)

    # Show options
    st.session_state.answers[q_index] = st.radio(
        "Choose your answer:",
        q_data["options"],
        index=q_data["options"].index(st.session_state.answers[q_index]) if st.session_state.answers[q_index] else None,
        key=f"q_{q_index}"
    )

    # Navigation Buttons
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("⬅️ Previous", disabled=q_index == 0):
            st.session_state.current_q = max(0, st.session_state.current_q - 1)
            st.rerun()

    with col2:
        if st.button("➡️ Next", disabled=q_index == len(quiz_data) - 1):
            st.session_state.current_q = min(len(quiz_data) - 1, st.session_state.current_q + 1)
            st.rerun()

    with col3:
        all_answered = all(a is not None for a in st.session_state.answers)
        if st.button("✅ Submit Quiz", disabled=not all_answered):
            st.session_state.submitted = True
            st.rerun()

else:
    # ------------------ #
    #   RESULT SECTION   #
    # ------------------ #
    score = 0
    st.success("🎉 Quiz Completed! Here’s your result:")
    st.write("---")

    for i, q in enumerate(quiz_data):
        user_ans = st.session_state.answers[i]
        correct_ans = q["answer"]
        st.markdown(f"**Q{i+1}. {q['question']}**")

        if user_ans == correct_ans:
            st.markdown(f"✅ Your Answer: **{user_ans}** (Correct!)")
            score += 1
        else:
            st.markdown(f"❌ Your Answer: **{user_ans}**")
            st.markdown(f"✅ Correct Answer: **{correct_ans}**")

        st.write("---")

    st.markdown(f"## 🏁 Final Score: **{score} / {len(quiz_data)}** 🎯")

    if score == len(quiz_data):
        st.balloons()
        st.success("Perfect! You nailed it! 🧠")
    elif score >= len(quiz_data) * 0.7:
        st.info("Great job! You’re almost perfect 👏")
    else:
        st.warning("Keep learning — you’ll improve soon 💪")

    if st.button("🔁 Play Again"):
        st.session_state.current_q = 0
        st.session_state.answers = [None] * len(quiz_data)
        st.session_state.submitted = False
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<p class="footer">Made with ❤️ using Streamlit</p>', unsafe_allow_html=True)
