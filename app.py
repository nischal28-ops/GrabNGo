import streamlit as st
import qrcode
import io
from datetime import datetime

st.set_page_config(page_title="GrabNGo", page_icon="🍽️", layout="wide")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #111827, #1f2937);
    color: white;
}
h1, h2, h3, p, label, span {
    color: white !important;
}
.card {
    background: #ffffff;
    color: #111827;
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.35);
    margin-bottom: 20px;
}
.card h3, .card p {
    color: #111827 !important;
}
.title {
    font-size: 50px;
    font-weight: 900;
    color: #facc15;
    text-align: center;
}
.subtitle {
    text-align: center;
    font-size: 20px;
    color: #e5e7eb;
}
.stButton button {
    background-color: #facc15;
    color: #111827;
    border-radius: 12px;
    font-weight: bold;
    border: none;
}
.stButton button:hover {
    background-color: #fde047;
    color: black;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🍽️ GrabNGo</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Pre-order food • Skip queues • Scan QR • Reduce waste</div>', unsafe_allow_html=True)

menu = {
    "🥪 Veg Sandwich": 50,
    "🧀 Cheese Maggi": 60,
    "☕ Cold Coffee": 80,
    "🥟 Samosa": 20,
    "🌯 Paneer Roll": 90,
    "🍋 Lemon Juice": 30,
    "🍕 Pizza Slice": 70,
    "🍔 Veg Burger": 85,
    "🍟 French Fries": 65,
    "🥤 Oreo Shake": 100,
    "🍜 Schezwan Noodles": 90,
    "🥗 Fruit Bowl": 55,
    "🍚 Veg Fried Rice": 95,
    "🥘 Chole Bhature": 110,
    "🥞 Pancakes": 120,
    "🍝 White Sauce Pasta": 130,
    "🌮 Tacos": 100,
    "🥛 Lassi": 45,
    "🧃 Fresh Juice": 60,
    "🍩 Chocolate Donut": 50,
    "🍪 Cookies": 35,
    "🍫 Brownie": 70,
    "🥣 Poha": 40,
    "🍳 Egg Roll": 75
}

if "cart" not in st.session_state:
    st.session_state.cart = {}

tab1, tab2, tab3, tab4 = st.tabs(["🍴 Menu", "🛒 Cart", "💳 Payment", "📊 Impact"])

with tab1:
    st.header("Today's Menu")

    cols = st.columns(4)

    for index, (item, price) in enumerate(menu.items()):
        with cols[index % 4]:
            st.markdown(f"""
            <div class="card">
                <h3>{item}</h3>
                <p><b>Price:</b> ₹{price}</p>
            </div>
            """, unsafe_allow_html=True)

            qty = st.number_input(
                f"Quantity",
                min_value=0,
                max_value=10,
                step=1,
                key=f"qty_{item}"
            )

            if st.button(f"Add to Cart", key=f"add_{item}"):
                if qty > 0:
                    st.session_state.cart[item] = {
                        "qty": qty,
                        "price": price
                    }
                    st.success(f"{item} added!")
                else:
                    st.warning("Select quantity first.")

with tab2:
    st.header("🛒 Your Cart")

    if not st.session_state.cart:
        st.info("Your cart is empty.")
    else:
        total = 0

        for item, details in st.session_state.cart.items():
            item_total = details["qty"] * details["price"]
            total += item_total
            st.write(f"**{item}** x {details['qty']} = ₹{item_total}")

        st.subheader(f"Total Amount: ₹{total}")

        if st.button("Clear Cart"):
            st.session_state.cart = {}
            st.success("Cart cleared.")

with tab3:
    st.header("💳 Payment & Pickup")

    name = st.text_input("Student Name")
    student_id = st.text_input("Student ID")

    pickup_time = st.selectbox(
        "Pickup Time",
        ["10:45 AM", "11:00 AM", "12:30 PM", "1:15 PM", "3:00 PM", "5:00 PM"]
    )

    payment_method = st.radio(
        "Payment Method",
        ["UPI QR Code", "Cash at Counter", "Meal Card"]
    )

    if st.session_state.cart:
        total = sum(d["qty"] * d["price"] for d in st.session_state.cart.values())

        if payment_method == "UPI QR Code":
            st.subheader("Scan to Pay")

            payment_text = f"GrabNGo Payment ₹{total}"
            qr = qrcode.make(payment_text)

            buffer = io.BytesIO()
            qr.save(buffer, format="PNG")
            buffer.seek(0)

            st.image(buffer, caption="Payment QR Code", width=250)

        if st.button("Confirm Order"):
            if not name or not student_id:
                st.warning("Enter name and student ID.")
            else:
                order_id = "GNG" + datetime.now().strftime("%H%M%S")

                st.success("Order Confirmed!")
                st.subheader("✅ Order Receipt")

                st.write(f"**Order ID:** {order_id}")
                st.write(f"**Name:** {name}")
                st.write(f"**Student ID:** {student_id}")
                st.write(f"**Pickup Time:** {pickup_time}")
                st.write(f"**Payment Method:** {payment_method}")
                st.write(f"**Total:** ₹{total}")

                pickup_qr_text = f"Order ID: {order_id}\nName: {name}\nPickup: {pickup_time}\nTotal: ₹{total}"
                pickup_qr = qrcode.make(pickup_qr_text)

                buffer2 = io.BytesIO()
                pickup_qr.save(buffer2, format="PNG")
                buffer2.seek(0)

                st.image(buffer2, caption="Pickup QR Code", width=250)
                st.balloons()
    else:
        st.info("Add items to cart first.")

with tab4:
    st.header("📊 Waste Reduction Impact")

    st.metric("Estimated Waiting Time Saved", "10 mins")
    st.metric("Food Waste Reduced", "25%")
    st.metric("Orders Prepared Accurately", "High")

    st.write("""
    GrabNGo helps cafeterias prepare food based on confirmed orders,
    reducing overproduction, long queues, and food wastage.
    """)
