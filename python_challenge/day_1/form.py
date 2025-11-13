import streamlit as st

# ---------- Page Setup ----------
st.set_page_config(page_title="Voter Eligibility Form", page_icon="🗳️", layout="centered")

# ---------- CSS Styling ----------
st.markdown("""
<style>
body {
    /* 💜 Updated background gradient */
    background: linear-gradient(135deg, #c3aed6 0%, #fbc2eb 100%);
    font-family: 'Poppins', sans-serif;
}
.stApp {
    background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
    padding: 2rem;
    border-radius: 20px;
    box-shadow: 0px 4px 25px rgba(0,0,0,0.1);
    transition: filter 0.4s ease;
}

/* Blur background when popup visible */
.blurred {
    filter: blur(6px) brightness(0.8);
}

/* 🎨 FORM CARD STYLING */
.form-container {
    background: #ffffffcc; /* soft white with slight transparency */
    padding: 2rem;
    border-radius: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    max-width: 450px;
    margin: 2rem auto;
}

/* Popup overlay */
.popup-overlay {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: rgba(0,0,0,0.4);
    backdrop-filter: blur(8px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
    animation: fadeIn 0.4s ease-in-out;
}

/* Popup content */
.popup-content {
    background: white;
    padding: 25px;
    border-radius: 15px;
    width: 90%;
    max-width: 350px;
    text-align: center;
    box-shadow: 0px 6px 25px rgba(0,0,0,0.3);
    animation: scaleIn 0.4s ease-in-out;
}
@keyframes fadeIn {from {opacity: 0;} to {opacity: 1;}}
@keyframes scaleIn {from {transform: scale(0.8);} to {transform: scale(1);}}

/* OK button inside popup */
.popup-btn {
    background: #4CAF50;
    color: white;
    border: none;
    padding: 10px 25px;
    margin-top: 15px;
    border-radius: 10px;
    cursor: pointer;
    font-weight: 600;
    transition: background 0.3s;
}
.popup-btn:hover {background: #45a049;}
</style>
""", unsafe_allow_html=True)

# ---------- Session State ----------
if "show_popup" not in st.session_state:
    st.session_state.show_popup = False
if "popup_message" not in st.session_state:
    st.session_state.popup_message = ""
if "popup_color" not in st.session_state:
    st.session_state.popup_color = "#4CAF50"

# ---------- Blur background when popup active ----------
container_class = "blurred" if st.session_state.show_popup else ""
st.markdown(f'<div class="{container_class}">', unsafe_allow_html=True)

# ---------- Title ----------
st.markdown("<h1 style='text-align:center;color:#2c3e50;'>Voter Eligibility Form</h1>", unsafe_allow_html=True)

# ---------- Form Container ----------

with st.form("voter_form"):
    name = st.text_input("Enter your Name")
    age = st.slider("Select your Age", 0, 100, 18)
    submitted = st.form_submit_button("Submit")

st.markdown('</div>', unsafe_allow_html=True)

# ---------- Handle submission ----------
if submitted:
    if not name.strip():
        st.warning("Please enter your name before submitting.")
    else:
        if age >= 18:
            st.session_state.popup_message = f"🎉 Hello {name}!<br><b>You are eligible to vote.</b>"
            st.session_state.popup_color = "#4CAF50"
        else:
            st.session_state.popup_message = f"🚫 Hello {name}!<br><b>You are not eligible to vote yet.</b>"
            st.session_state.popup_color = "#e74c3c"
        st.session_state.show_popup = True

st.markdown("</div>", unsafe_allow_html=True)

# ---------- Popup ----------
if st.session_state.show_popup:
    popup_html = f"""
    <div class="popup-overlay">
        <div class="popup-content" style="border-top:6px solid {st.session_state.popup_color};">
            <h3 style="color:{st.session_state.popup_color};">{st.session_state.popup_message}</h3>
            <form action="" method="get">
                <button class="popup-btn" type="submit">OK</button>
            </form>
        </div>
    </div>
    """
    st.markdown(popup_html, unsafe_allow_html=True)
    st.session_state.show_popup = False 


