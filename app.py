import streamlit as st
import qrcode
import io
from datetime import datetime

st.set_page_config(page_title="GrabNGo", page_icon="🍽️", layout="wide")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #fff7ed, #ffe4e6);
}
.card {
    background: white;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    margin-bottom: 15px;
}
.title {
    font-size: 45px;
    font-weight: 800;
    color: #e11d48;
    text-align: center;
}
.subtitle {
    text-align: center;
    font-size: 20px;
    color: #555;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🍽️ GrabNGo</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Pre-order food. Skip queues. Reduce waste.</div>', unsafe_allow_html=True)

menu = {
    "🥪 Veg Sandwich": 50,
    "🧀 Cheese Maggi": 60,
    "☕ Cold Coffee": 80,
    "🥟 Samosa": 20,
    "🌯 Paneer Roll": 90,
    "🍋 Lemon Juice": 30,
    "🍕 Pizza Slice": 70,
    "🍔 Veg Burger": 85,
    "🥤 Oreo Shake": 100,
    "🍟 French Fries": 65,
    "🍜 Noodles": 75,
    "🥗 Fruit Bowl": 55
}

if "cart" not in st.session_state:
    st.session_state.cart = {}

tab1, tab2, tab3, tab4 = st.tabs(["🍴 Menu", "🛒 Cart", "💳 Payment", "📊 Impact"])

with tab1:
    st.header("Today's Menu")

    cols = st.columns(3)

    for index, (item, price) in enumerate(menu.items()):
        with cols[index % 3]:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader(item)
            st.write(f"₹{price}")
            qty = st.number_input(
                f"Quantity for {item}",
                min_value=0,
                max_value=10,
                step=1,
                key=item
            )

            if st.button(f"Add {item}", key=f"add_{item}"):
                if qty > 0:
                    st.session_state.cart[item] = {
                        "qty": qty,
                        "price": price
                    }
                    st.success(f"{item} added to cart!")
                else:
                    st.warning("Select quantity first.")
            st.markdown('</div>', unsafe_allow_html=True)

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

            payment_text = f"Pay ₹{total} for GrabNGo order"
            qr = qrcode.make(payment_text)

            buffer = io.BytesIO()
            qr.save(buffer, format="PNG")
            buffer.seek(0)

            st.image(buffer, caption="Payment QR Code", width=250)

        if st.button("Confirm Order"):
            if not name or not student_id:
                st.warning("Please enter your name and student ID.")
            else:
                st.success("Order Confirmed!")

                order_id = "GNG" + datetime.now().strftime("%H%M%S")

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

    st.markdown("""
    This app helps the campus cafeteria by:

    ✅ Reducing long queues  
    ✅ Preparing food based on confirmed orders  
    ✅ Avoiding overproduction  
    ✅ Saving student break time  
    ✅ Making pickup faster using QR codes  
    """)

    st.metric("Estimated Waiting Time Saved", "10 minutes")
    st.metric("Food Waste Reduced", "25%")
    st.metric("Student Convenience", "High")
