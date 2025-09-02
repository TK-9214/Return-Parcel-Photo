import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from io import BytesIO

st.set_page_config(page_title="Claim Report PDF Generator", page_icon="📦")

st.title("📦 Claim Report PDF Generator")

# --- Input fields ---
order_id = st.text_input("Order ID")
tracking = st.text_input("Tracking Number")
sku = st.text_input("SKU")
reason = st.selectbox("Reason", ["Damage", "Wrong Item"])

# --- File upload for photos ---
parcel_photo = st.file_uploader("1️⃣ Received Parcel Condition", type=["png", "jpg", "jpeg"])
awb_photo = st.file_uploader("2️⃣ AWB / Tracking Detail", type=["png", "jpg", "jpeg"])
prod1_photo = st.file_uploader("3️⃣ Product Condition Photo 1", type=["png", "jpg", "jpeg"])
prod2_photo = st.file_uploader("4️⃣ Product Condition Photo 2", type=["png", "jpg", "jpeg"])

if st.button("📄 Generate PDF"):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"Order ID: {order_id}", styles["Normal"]))
    story.append(Paragraph(f"Tracking: {tracking}", styles["Normal"]))
    story.append(Paragraph(f"SKU: {sku}", styles["Normal"]))
    story.append(Paragraph(f"Reason: {reason}", styles["Normal"]))
    story.append(Spacer(1, 12))

    def add_photo(title, uploaded_file):
        story.append(Paragraph(title, styles["Heading4"]))
        if uploaded_file:
            img = Image(uploaded_file, width=250, height=250)
            story.append(img)
        else:
            story.append(Paragraph("No image uploaded", styles["Italic"]))
        story.append(Spacer(1, 12))

    add_photo("1. Received Parcel Condition", parcel_photo)
    add_photo("2. AWB / Tracking Detail", awb_photo)
    add_photo("3. Product Condition Photo 1", prod1_photo)
    add_photo("4. Product Condition Photo 2", prod2_photo)

    doc.build(story)
    buffer.seek(0)

    st.download_button(
        label="⬇️ Download PDF",
        data=buffer,
        file_name=f"claim_{order_id or 'report'}.pdf",
        mime="application/pdf",
    )
