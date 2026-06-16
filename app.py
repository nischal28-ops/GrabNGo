import streamlit as st
import qrcode
import io
from datetime import datetime

st.set_page_config(page_title="GrabNGo", page_icon="🛍️", layout="wide")

st.markdown("""
<style>
.stApp {
    background: #070b1a;
    color: white;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #090d22, #121a3a);
}

h1, h2, h3, p, label, span, div {
    color: white !important;
}

.main-title {
    font-size: 38px;
    font-weight: 900;
    color: #ffffff;
}

.logo {
    font-size: 34px;
    font-weight: 900;
    color: #facc15;
}

.card {
    background: linear-gradient(145deg, #111827, #1e293b);
    border: 1px solid #334155;
    border-radius: 18px;
    padding: 16px;
    margin-bottom: 15px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.4);
}

.food-card {
    background: linear-gradient(145deg, #111827, #1e293b);
    border: 1px solid #334155;
    border-radius: 18px;
    padding: 16px;
    margin-bottom: 12px;
    min-height: 135px;
}

.food-name {
    font-size: 18px;
    font-weight: 800;
    color: #ffffff !important;
}

.price {
    font-size: 16px;
    font-weight: 800;
    color: #22c55e !important;
}

.stButton button {
    background: linear-gradient(90deg, #fb7185, #ec4899);
    color: white !important;
    border-radius: 10px;
    border: none;
    font-weight: 800;
}

.stButton button:hover {
    background: linear-gradient(90deg, #f43f5e, #db2777);
}

.metric-card {
    background: linear-gradient(145deg, #13251c, #1e293b);
    border: 1px solid #22c55e;
    border-radius: 16px;
    padding: 18px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

menu = {
    "🥪 Veg Sandwich": 50,
    "🧀 Cheese Maggi": 60,
    "🌯 Paneer Roll": 90,
    "🍔 Veg Burger": 85,
    "🥟 Samosa": 20,
    "🍟 French Fries": 65,
    "🍕 Pizza Slice": 70,
    "🍜 Schezwan Noodles": 90,
    "🍚 Veg Fried Rice": 95,
    "🍝 White Sauce Pasta": 130,
    "🌮 Tacos": 100,
    "🥗 Fruit Bowl": 55,
    "🥤 Oreo Shake": 100,
    "🍋 Lemon Juice": 30,
    "🧃 Fresh Juice": 60,
    "🍫 Chocolate Brownie": 70,
    "🥞 Pancakes": 120,
    "🥛 Lassi": 45,
    "🍪 Cookies": 35,
    "🥣 Poha": 40,
    "🍳 Egg Roll": 75,
    "☕ Hot Coffee": 50,
    "🥘 Chole Bhature": 110,
    "🥗 Masala Dosa": 90
}

if "cart" not in st.session_state:
    st.session_state.cart = {}

with st.sidebar:
    st.markdown('<div class="logo">🛍️ GrabNGo</div>', unsafe_allow_html=True)
    st.write("Pre-order food. Skip queues. Reduce waste.")
    st.divider()
    st.write("🏠 Menu")
    st.write("🛒 Cart")
    st.write("💳 Payment")
    st.write("📊 Impact")
    st.divider()
    st.info("Your pre-orders help reduce food waste and waiting time 🌱")

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="main-title">👋 Welcome to GrabNGo!</div>', unsafe_allow_html=True)
    st.write("Pre-order your favourite food, pay with QR, and pick it up on time.")
with col2:
    st.markdown(f"""
    <div class="card">
    📅 16 June 2026<br>
    ⏰ {datetime.now().strftime("%I:%M %p")}
    </div>
    """, unsafe_allow_html=True)

tabs = st.tabs(["🍽️ Today's Menu", "🛒 Your Cart", "💳 Payment", "📊 Impact"])

with tabs[0]:
    st.header("🍽️ Today's Menu")

    cols = st.columns(4)

    for i, (item, price) in enumerate(menu.items()):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="food-card">
                <div class="food-name">{item}</div>
                <br>
                <div class="price">₹{price}</div>
            </div>
            """, unsafe_allow_html=True)

            qty = st.number_input(
                "Qty",
                min_value=0,
                max_value=10,
                value=0,
                key=f"qty_{item}"
            )

            if st.button("Add", key=f"add_{item}"):
                if qty > 0:
                    st.session_state.cart[item] = {"qty": qty, "price": price}
                    st.success(f"{item} added to cart!")
                else:
                    st.warning("Choose quantity first.")

with tabs[1]:
    st.header("🛒 Your Cart")

    if not st.session_state.cart:
        st.info("Your cart is empty.")
    else:
        total = 0

        for item, details in st.session_state.cart.items():
            item_total = details["qty"] * details["price"]
            total += item_total
            st.markdown(f"""
            <div class="card">
            <b>{item}</b><br>
            Quantity: {details['qty']}<br>
            Amount: ₹{item_total}
            </div>
            """, unsafe_allow_html=True)

        st.subheader(f"Total Amount: ₹{total}")

        if st.button("Clear Cart"):
            st.session_state.cart = {}
            st.rerun()

with tabs[2]:
    st.header("💳 Payment & Pickup")

    name = st.text_input("Your Name")
    student_id = st.text_input("Student ID")

    pickup_time = st.selectbox(
        "Choose pickup time",
        ["10:30 AM - 10:45 AM", "12:30 PM - 1:00 PM", "1:15 PM - 1:30 PM", "3:00 PM - 3:15 PM", "5:00 PM - 5:15 PM"]
    )

    payment_method = st.radio(
        "Payment Method",
        ["UPI QR Code", "Cash at Counter", "Meal Card"]
    )

    if st.session_state.cart:
        total = sum(details["qty"] * details["price"] for details in st.session_state.cart.values())

        st.subheader(f"Amount to Pay: ₹{total}")

        payment_qr_text = f"GrabNGo Payment Amount ₹{total}"
        payment_qr = qrcode.make(payment_qr_text)
        buffer = io.BytesIO()
        payment_qr.save(buffer, format="PNG")
        buffer.seek(0)

        if payment_method == "UPI QR Code":
            st.image(buffer, caption="Scan to Pay", width=250)

        if st.button("Confirm Order"):
            if not name or not student_id:
                st.warning("Enter your name and student ID.")
            else:
                order_id = "GNG" + datetime.now().strftime("%H%M%S")

                st.success("Order confirmed successfully!")

                st.markdown(f"""
                <div class="card">
                <b>Order ID:</b> {order_id}<br>
                <b>Name:</b> {name}<br>
                <b>Student ID:</b> {student_id}<br>
                <b>Pickup Time:</b> {pickup_time}<br>
                <b>Total:</b> ₹{total}
                </div>
                """, unsafe_allow_html=True)

                pickup_qr_text = f"Order ID: {order_id}\nName: {name}\nPickup: {pickup_time}\nTotal: ₹{total}"
                pickup_qr = qrcode.make(pickup_qr_text)
                buffer2 = io.BytesIO()
                pickup_qr.save(buffer2, format="PNG")
                buffer2.seek(0)

                st.image(buffer2, caption="Pickup QR Code", width=250)
                st.balloons()
    else:
        st.info("Add food items to cart first.")

with tabs[3]:
    st.header("📊 Our Impact")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown('<div class="metric-card"><h2>10+ mins</h2><p>Avg. Time Saved</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-card"><h2>25%</h2><p>Food Waste Reduced</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-card"><h2>500+</h2><p>Happy Students</p></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="metric-card"><h2>1200+</h2><p>Orders Completed</p></div>', unsafe_allow_html=True)

    st.info("GrabNGo prepares food based on confirmed orders, helping reduce overproduction and waste.")
