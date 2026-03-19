import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

def create_label(order_num, item_count, material, design_name):
    # --- RESOLUTION & DIMENSIONS ---
    # 600 DPI calculation: 1 inch = 600px height | 4.5 inches = 2700px width
    scale_factor = 2 
    width, height = 1350 * scale_factor, 300 * scale_factor  
    
    # --- COLOR DEFINITIONS ---
    sage_green = (136, 154, 137)  # Your custom brand color #889a89
    pure_black = (0, 0, 0)        # For high-contrast readable text
    
    # 1. QR CODE GENERATION (Sage Green)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=20,
        border=4, 
    )
    qr.add_data(order_num)
    qr.make(fit=True)
    
    # Create QR with Sage Green fill and White background
    qr_img = qr.make_image(fill_color=sage_green, back_color="white").convert('RGB')
    
    # Resize QR to fit the 600px height with high-quality smoothing
    qr_side = 560 
    qr_img = qr_img.resize((qr_side, qr_side), resample=Image.LANCZOS)
    
    # 2. CANVAS CREATION (RGB Mode for Color Support)
    background = Image.new('RGB', (width, height), color=(255, 255, 255))
    background.paste(qr_img, (20, 20))
    draw = ImageDraw.Draw(background)
    
    # 3. SMART FONT LOADING
    # Optimized for Streamlit Cloud (Linux) servers
    try:
        font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
        font_main = ImageFont.truetype(font_path, 140) # Large for Order #
        font_sub = ImageFont.truetype(font_path, 90)   # Medium for details
    except:
        # Fallback if the server paths differ
        font_main = ImageFont.load_default(size=120)
        font_sub = ImageFont.load_default(size=80)

    # 4. DRAW TEXT (Pure Black)
    text_x = 700
    draw.text((text_x, 60), f"ORDER #: {order_num}", fill=pure_black, font=font_main)
    draw.text((text_x, 210), f"ITEM: {item_count}", fill=pure_black, font=font_sub)
    draw.text((text_x, 330), f"MAT: {material}", fill=pure_black, font=font_sub)
    draw.text((text_x, 450), f"DESIGN: {design_name}", fill=pure_black, font=font_sub)
    
    return background

# --- STREAMLIT USER INTERFACE ---
st.set_page_config(page_title="Custom Label Creator", layout="centered")

st.title("🏷️ Custom Label Creator")
st.write("Professional 1-inch labels at 600 DPI resolution.")

# Input fields for label data
col1, col2 = st.columns(2)
with col1:
    order_id = st.text_input("Order Number", "211720")
    items = st.text_input("Item Count", "1 of 1")
with col2:
    mat = st.text_input("Material", "Linen Cotton Canvas")
    design = st.text_input("Design Name", "Sweetgrass Final PNG")

# Action Button
if st.button("Generate Label"):
    img = create_label(order_id, items, mat, design)
    
    # Display preview at a reasonable size on screen
    st.image(img, caption="High-Res Preview (Actual print will be 1 inch tall)", width=800)
    
    # Prepare the image for download
    buf = io.BytesIO()
    # Save with 600 DPI metadata so printers recognize the physical size
    img.save(buf, format="PNG", dpi=(600, 600))
    
    st.download_button(
        label="Download Label for Printing",
        data=buf.getvalue(),
        file_name=f"{order_id}_code.png",
        mime="image/png"
    )
