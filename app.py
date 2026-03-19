import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

def create_label(order_num, item_count, size_val, design_name):
    # --- RESOLUTION & DIMENSIONS ---
    scale_factor = 2 
    width, height = 1350 * scale_factor, 300 * scale_factor  
    
    # --- COLOR DEFINITIONS ---
    custom_blue = (131, 158, 185)  # #839eb9
    pure_black = (0, 0, 0)        
    
    # 1. QR CODE GENERATION
    qr = qrcode.QRCode(version=1, box_size=20, border=4)
    qr.add_data(order_num)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=custom_blue, back_color="white").convert('RGB')
    
    qr_side = 560 
    qr_img = qr_img.resize((qr_side, qr_side), resample=Image.LANCZOS)
    
    # 2. CANVAS CREATION
    background = Image.new('RGB', (width, height), color=(255, 255, 255))
    background.paste(qr_img, (20, 20))
    draw = ImageDraw.Draw(background)
    
    # 3. SMART FONT LOADING
    try:
        font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
        font_main = ImageFont.truetype(font_path, 140)
        font_sub = ImageFont.truetype(font_path, 90)
    except:
        font_main = ImageFont.load_default(size=120)
        font_sub = ImageFont.load_default(size=80)

    # 4. DRAW TEXT (Updated 'MAT' to 'SIZE')
    text_x = 700
    draw.text((text_x, 60), f"ORDER #: {order_num}", fill=pure_black, font=font_main)
    draw.text((text_x, 210), f"ITEM: {item_count}", fill=pure_black, font=font_sub)
    draw.text((text_x, 330), f"SIZE: {size_val}", fill=pure_black, font=font_sub)
    draw.text((text_x, 450), f"DESIGN: {design_name}", fill=pure_black, font=font_sub)
    
    return background

# --- STREAMLIT USER INTERFACE ---
st.set_page_config(page_title="Custom Label Creator", layout="centered")

st.title("🏷️ Custom Label Creator")
st.write("Professional 1-inch labels at 600 DPI resolution.")

col1, col2 = st.columns(2)
with col1:
    order_id = st.text_input("Order Number", )
    items = st.text_input("Item Count", "1 of 1")
with col2:
    size_input = st.text_input("Size", ) # Updated Label
    design = st.text_input("Design Name", )

if st.button("Generate Label"):
    img = create_label(order_id, items, size_input, design)
    st.image(img, caption="High-Res Preview", width=800)
    
    buf = io.BytesIO()
    img.save(buf, format="PNG", dpi=(600, 600))
    
    st.download_button(
        label="Download Label",
        data=buf.getvalue(),
        file_name=f"{order_id}_code.png",
        mime="image/png"
    )
