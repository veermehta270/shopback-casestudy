import streamlit as st
from utils import *
from pathlib import Path
import matplotlib.pyplot as plt

st.set_page_config(page_title="ShopBack Brand Automation", layout="wide", page_icon="🟠")

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Background ── */
.stApp {
    background-color: #FFF8F5;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #3D1F0F !important;
    border-right: none;
}
[data-testid="stSidebar"] * {
    color: #F5DDD3 !important;
}
[data-testid="stSidebar"] h1 {
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #FF6633 !important;
    margin-bottom: 1.5rem;
}

/* ── Modern pill nav in sidebar (hide radio circles) ── */
[data-testid="stSidebar"] [data-testid="stRadio"] > div {
    display: flex;
    flex-direction: column;
    gap: 4px;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    border-radius: 8px;
    padding: 9px 14px !important;
    font-size: 0.88rem !important;
    font-weight: 400;
    cursor: pointer;
    transition: background 0.15s ease;
    border: 1px solid transparent;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background-color: rgba(255,102,51,0.18) !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background-color: #FF6633 !important;
    color: #fff !important;
    font-weight: 600 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] [data-testid="stMarkdownContainer"] p {
    font-size: 0.88rem;
}
/* Hide native radio dot */
[data-testid="stSidebar"] [data-testid="stRadio"] input[type="radio"] {
    display: none !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] svg {
    display: none !important;
}

/* ── Page Header ── */
h1, h2, h3 {
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    color: #2D1A0E;
}

/* ── Top page title bar ── */
.page-title {
    border-left: 4px solid #FF6633;
    padding: 0.25rem 0 0.25rem 1rem;
    margin-bottom: 2rem;
    line-height: 1.2;
}
.page-title h2 {
    font-size: 1.6rem;
    margin: 0;
    color: #2D1A0E;
}
.page-title p {
    font-size: 0.85rem;
    color: #B07060;
    margin: 0.2rem 0 0 0;
}

/* ── Buttons ── */
.stButton > button {
    background-color: #FF6633;
    color: white;
    border: none;
    border-radius: 999px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    font-size: 0.85rem;
    padding: 0.45rem 1.4rem;
    letter-spacing: 0.02em;
    transition: all 0.2s ease;
    box-shadow: 0 2px 8px rgba(255, 102, 51, 0.25);
}
.stButton > button:hover {
    background-color: #FF6633;
    color: white;
    border: none;
    box-shadow: 0 4px 16px rgba(255, 102, 51, 0.38);
    transform: translateY(-1px);
}
.stButton > button:active {
    transform: translateY(0px);
    box-shadow: 0 2px 6px rgba(255, 102, 51, 0.2);
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stSelectbox > div > div {
    border-radius: 6px;
    border: 1px solid #DEDEDE;
    background-color: #fff;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
}
.stTextInput > div > div > input:focus {
    border-color: #FF6633;
    box-shadow: 0 0 0 2px rgba(255,102,51,0.12);
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    border: 1.5px dashed #DEDEDE;
    border-radius: 8px;
    background: #fff;
    padding: 0.5rem;
}
[data-testid="stFileUploader"]:hover {
    border-color: #FF6633;
}

/* ── Expander ── */
.stExpander {
    border: 1px solid #EDEDED !important;
    border-radius: 8px !important;
    background: #fff;
}

/* ── Progress bar ── */
.stProgress > div > div > div {
    background-color: #FF6633;
    border-radius: 4px;
}
.stProgress > div > div {
    background-color: #F0F0F0;
    border-radius: 4px;
}

/* ── Alerts ── */
.stSuccess, .stInfo, .stWarning, .stError {
    border-radius: 6px;
}

/* ── Divider ── */
hr {
    border: none;
    border-top: 1px solid #EDEDED;
    margin: 1.5rem 0;
}

/* ── Status badges ── */
.badge-pending {
    background: #FFF3E0;
    color: #E65100;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.badge-finalized {
    background: #E8F5E9;
    color: #2E7D32;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* ── Image captions ── */
.stImage > div > div > p {
    font-size: 0.78rem;
    color: #999;
    text-align: center;
    margin-top: 4px;
    font-family: 'DM Mono', monospace;
}

/* ── Radio group ── */
.stRadio > label {
    font-size: 0.88rem;
    font-weight: 500;
    color: #555;
}
</style>
""", unsafe_allow_html=True)


# ── Sidebar ─────────────────────────────────────────────────────────────────
st.sidebar.title("ShopBack Automation")
page = st.sidebar.radio(
    "Navigate",
    [
        "Customer Registration / Upload",
        "Pending Approvals",
        "Dashboard",
        "Operations Analytics"
    ]
)

customers = load_customers()


# ── Helper: page title ───────────────────────────────────────────────────────
def page_header(title, subtitle=""):
    sub_html = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(f"""
    <div class="page-title">
        <h2>{title}</h2>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


# ── Page 1: Customer Registration / Upload ───────────────────────────────────
if page == "Customer Registration / Upload":
    page_header("Customer Registration", "Upload and process brand logos for review.")

    option = st.radio("Action", ["Create New Customer", "Update Existing Customer"], horizontal=True)
    st.write("")

    if option == "Create New Customer":
        brand_name = st.text_input("Brand Name")
        email = st.text_input("Customer Email")
    else:
        if customers:
            brand_name = st.selectbox("Select Existing Customer", list(customers.keys()))
            email = customers[brand_name]["email"]
            st.caption(f"📧 {email}")
        else:
            st.warning("No existing customers. Please create a new customer.")
            brand_name = email = None

    st.write("")
    uploaded_files = st.file_uploader("Upload 1–3 logos (PNG / JPG)", type=["png","jpg","jpeg"], accept_multiple_files=True)
    drive_link = st.text_input("Google Drive Link", placeholder="https://drive.google.com/...")

    st.write("")
    if st.button("Submit →"):
        if not brand_name or not email:
            st.error("Brand name and email are required.")
        elif not uploaded_files and not drive_link:
            st.error("Upload at least one image or provide a Drive link.")
        else:
            save_folder = create_customer_folder(brand_name)
            all_files = []

            for file in uploaded_files:
                temp_path = save_folder / "original.png"
                with open(temp_path, "wb") as f:
                    f.write(file.getbuffer())
                all_files.append(temp_path)

            if drive_link:
                try:
                    drive_file = download_drive_file(drive_link, save_folder)
                    all_files.append(drive_file)
                except Exception as e:
                    st.error(f"Drive download failed: {e}")

            valid_files = [f for f in all_files if validate_file(f)]
            if not valid_files:
                st.error("No valid image files found.")
            else:
                sizes = [(500, 500)]
                original_file = valid_files[0]

                resized_files = resize_image(original_file, sizes, save_folder)
                inverted_file = invert_image(original_file, save_folder)

                info_file = create_info_file(
                    save_folder, brand_name, email,
                    original_file.name, resized_files, inverted_file
                )

                customers[brand_name] = {
                    "email": email,
                    "folder": str(save_folder),
                    "status": "Pending"
                }
                save_customers(customers)

                st.success(f"✓ Processed and pending approval for **{brand_name}**.")
                st.caption(f"Saved to: `{save_folder}`")
                st.write("")

                col1, col2 = st.columns(2)
                col1.image(str(inverted_file), caption="Inverted")
                col2.image(str(resized_files[0]), caption="Resized 500×500")
                st.balloons()


# ── Page 2: Pending Approvals ────────────────────────────────────────────────
elif page == "Pending Approvals":
    page_header("Pending Approvals", "Review and finalize submitted brand logos.")

    pending_customers = {k: v for k, v in customers.items() if v["status"] == "Pending"}

    if not pending_customers:
        st.info("All clear — no pending approvals.")
    else:
        for cust_name, info in pending_customers.items():
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:12px; margin: 1.5rem 0 0.5rem 0;">
                <span style="font-size:1.05rem; font-weight:600; color:#1A1A1A;">{cust_name}</span>
                <span class="badge-pending">Pending</span>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("View Processed Images"):
                folder = Path(info["folder"])
                images = list(folder.glob("*.png"))
                cols = st.columns(3)
                for idx, img in enumerate(images):
                    cols[idx % 3].image(str(img), caption=img.name)

            if st.button(f"Finalize {cust_name} →", key=f"fin_{cust_name}"):
                customers[cust_name]["status"] = "Finalized"
                save_customers(customers)

                success = send_completion_email(info["email"], cust_name)
                st.success(f"✓ {cust_name} has been finalized.")
                st.toast("Brand successfully published!", icon="🎉")

                if success:
                    st.info("Confirmation email sent to customer ✅")
                else:
                    st.warning("Email failed to send.")
                st.rerun()

            st.markdown("<hr>", unsafe_allow_html=True)


# ── Page 3: Dashboard ────────────────────────────────────────────────────────
elif page == "Dashboard":
    page_header("Brand Dashboard", "All finalized customer logos at a glance.")

    finalized_customers = {k: v for k, v in customers.items() if v["status"] == "Finalized"}

    if not finalized_customers:
        st.info("No finalized customers yet.")
    else:
        for cust_name, info in finalized_customers.items():
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:12px; margin: 1.5rem 0 0.75rem 0;">
                <span style="font-size:1.05rem; font-weight:600; color:#1A1A1A;">{cust_name}</span>
                <span class="badge-finalized">Finalized</span>
            </div>
            """, unsafe_allow_html=True)

            folder = Path(info["folder"])
            original = folder / "original.png"
            resized  = folder / "resized_500x500.png"
            inverted = folder / "inverted.png"

            col1, col2, col3 = st.columns(3)
            if original.exists():
                col1.image(str(original), caption="Original")
            if resized.exists():
                col2.image(str(resized), caption="Resized (Banner)")
            if inverted.exists():
                col3.image(str(inverted), caption="Inverted")

            st.markdown("<hr>", unsafe_allow_html=True)


# ── Page 4: Operations Analytics ─────────────────────────────────────────────
elif page == "Operations Analytics":
    page_header("Operations Analytics", "Workflow status and progress across all brands.")

    if not customers:
        st.info("No customer data available.")
    else:
        # ── Status Distribution ──
        status_counts = {}
        for cust, info in customers.items():
            s = info["status"]
            status_counts[s] = status_counts.get(s, 0) + 1

        labels = list(status_counts.keys())
        sizes  = list(status_counts.values())
        colors = ["#FF6633", "#1A1A1A", "#BDBDBD"]

        fig, ax = plt.subplots(figsize=(4, 4))
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")
        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, autopct="%1.0f%%",
            colors=colors[:len(labels)],
            startangle=90,
            wedgeprops={"linewidth": 1.5, "edgecolor": "white"}
        )
        for t in texts:
            t.set_fontsize(10)
            t.set_color("#333")
        for at in autotexts:
            at.set_fontsize(9)
            at.set_color("white")
            at.set_fontweight("bold")
        ax.set_title("Brand Workflow Distribution", fontsize=11, fontweight="600", color="#1A1A1A", pad=14)

        col_chart, col_spacer = st.columns([1, 2])
        with col_chart:
            st.pyplot(fig, use_container_width=False)

        st.markdown("<hr>", unsafe_allow_html=True)

        # ── Workflow Progress Per Brand ──
        st.subheader("Workflow Progress")

        workflow_steps = ["Uploaded", "Processed", "Pending", "Finalized"]

        for cust_name, info in customers.items():
            st.write(f"**{cust_name}**")

            if info["status"] == "Pending":
                progress_value = 0.75
            elif info["status"] == "Finalized":
                progress_value = 1.0
            else:
                progress_value = 0.25

            st.progress(progress_value)

            cols = st.columns(len(workflow_steps))
            for i, step in enumerate(workflow_steps):
                if progress_value >= (i + 1) / len(workflow_steps):
                    cols[i].success(step)
                else:
                    cols[i].info(step)

            st.write("")
