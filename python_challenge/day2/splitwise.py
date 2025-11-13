import streamlit as st
import pandas as pd

# -------------- PAGE CONFIG --------------
st.set_page_config(page_title="Splitwise", layout="centered")

# -------------- CUSTOM CSS --------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif !important;
    background: linear-gradient(135deg, #89f7fe, #66a6ff);
    color: #222;
}

h1, h2, h3, h4 {
    text-align: center;
    font-weight: 600 !important;
}

.stApp {
    background: linear-gradient(135deg, #89f7fe, #66a6ff);
}

.main-title {
    text-align: center;
    font-size: 2rem;
    font-weight: 700;
    color: #1e1e1e;
    margin-bottom: 0.3em;
}

.subtitle {
    text-align: center;
    font-size: 1rem;
    opacity: 0.8;
    margin-bottom: 2em;
}

/* Card container styling */
.block-container {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 20px;
    padding: 3rem 3rem 2rem 3rem;
    box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    margin-top: 2rem;
}

/* Style input boxes */
.stTextInput>div>div>input,
.stNumberInput>div>div>input {
    border-radius: 12px;
    border: 1px solid #dcdcdc;
    padding: 10px;
}

.stTextInput>div>div>input:focus,
.stNumberInput>div>div>input:focus {
    border-color: #66a6ff;
    box-shadow: 0 0 0 3px rgba(102,166,255,0.3);
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #667eea, #764ba2);
    color: white;
    border-radius: 12px;
    padding: 0.6em 1.5em;
    font-weight: 600;
    border: none;
    transition: all 0.2s ease-in-out;
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

/* Section headers */
.section-header {
    font-size: 1.3rem;
    font-weight: 600;
    margin-top: 1.5em;
    color: #333;
}

/* WhatsApp message box */
.whatsapp-box {
    background: #e0ffe0;
    border-left: 5px solid #25D366;
    padding: 1em;
    border-radius: 10px;
    margin-top: 1em;
}
</style>
""", unsafe_allow_html=True)

# -------------- HEADER --------------
st.markdown("<h1 class='main-title'>Split Your Expense</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Split bills fairly, settle instantly, and share results via WhatsApp 💬</p>", unsafe_allow_html=True)

# -------------- INPUT SECTION --------------
st.markdown("<h3 class='section-header'>Enter expense details 💡</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
currency = col1.selectbox("Currency", ["INR", "USD", "EUR", "GBP"])
total_amount = col2.number_input("Total amount", min_value=0.0, value=0.0, step=1.0, format="%.0f")

col3, col4 = st.columns(2)
num_people = int(col3.number_input("Number of people", min_value=1, value=1, step=1))

# -------------- PARTICIPANTS INPUT --------------
st.markdown("<h3 class='section-header'>Participants 🧑‍🤝‍🧑</h3>", unsafe_allow_html=True)

participants = []
for i in range(num_people):
    st.markdown(f"**Name #{i+1}**")
    cols = st.columns([2, 1, 2])
    name = cols[0].text_input(f"Name {i+1}", key=f"name_{i}")
    contributed = cols[1].number_input(f"Contributed {i+1}", min_value=0.0, step=1.0, key=f"contrib_{i}")
    phone = cols[2].text_input(f"Phone (optional) {i+1}", key=f"phone_{i}")
    participants.append((name, contributed, phone))

# -------------- CALCULATION --------------
if st.button("💰 Calculate Split"):
    if total_amount <= 0 or num_people <= 0:
        st.error("Please enter valid amount and participants.")
    else:
        avg_share = total_amount / num_people
        results = []
        for name, contributed, phone in participants:
            balance = round(contributed - avg_share, 2)
            results.append((name, contributed, balance, phone))

        df = pd.DataFrame(results, columns=["Name", "Contributed", "Balance", "Phone"])
        st.markdown("### 💵 Results")
        st.dataframe(df, use_container_width=True)

        # Generate WhatsApp messages
        st.markdown("### 📲 WhatsApp Messages")
        for name, contributed, balance, phone in results:
            if phone:
                if balance < 0:
                    msg = f"Hey {name}, you owe {abs(balance)} {currency} 💸"
                elif balance > 0:
                    msg = f"Hey {name}, you’ll get back {balance} {currency} 🎉"
                else:
                    msg = f"Hey {name}, you’re all settled up ✅"

                wa_link = f"https://wa.me/{phone}?text={msg.replace(' ', '%20')}"
                st.markdown(f"<div class='whatsapp-box'>📞 <b>{name}</b><br>{msg}<br><a href='{wa_link}' target='_blank'>Send via WhatsApp</a></div>", unsafe_allow_html=True)
