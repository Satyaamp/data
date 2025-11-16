import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# --- Configuration ---
EXCEL_FILE = 'DATA.xlsx'
COL_COLLEGE = 'College'
COL_NATIONALITY = 'Nationality'
COL_GENDER = 'Gender'
COL_NAME = 'Full Name'
COL_PHONE = 'Official Phone'
COL_WHATSAPP = 'WhatsApp Number'
COL_HOD_PHONE = 'HOD Contact No'
COL_HOD_NAME = 'HOD Name'
COL_HOD_MAIL = 'HOD Mail ID'

st.set_page_config(page_title="Dashboard", page_icon="🎓", layout="wide")

# --- Enhanced CSS with Modern 3D Design ---
ENHANCED_STYLES = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main background with gradient overlay */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://images.unsplash.com/photo-1534796636912-3b95b3ab5986?auto=format&fit=crop&w=1400");
        background-attachment: fixed;
        background-size: cover;
        perspective: 1500px; /* This is your 3D 'stage' camera */
        transform-style: preserve-3d; /* --- 3D CHANGE --- */
    }
    
    /* Header styling */
    [data-testid="stHeader"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        transform: translateZ(0px); /* --- 3D CHANGE (Keep header at the back) --- */
    }
    
    /* Enhanced glassmorphism cards (Your original class) */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: all 0.3s ease;
        transform-style: preserve-3d; /* --- 3D CHANGE --- */
    }
    
    .glass-card:hover {
        transform: translateY(-5px) translateZ(50px); /* --- 3D CHANGE --- */
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.5);
    }
    
    /* Metric cards */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.25);
        padding: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease-out; /* --- 3D CHANGE (Added ease-out) --- */
        transform: translateZ(30px); /* --- 3D CHANGE (Default float) --- */
        transform-style: preserve-3d; /* --- 3D CHANGE --- */
    }
    
    /* --- 3D CHANGE (Replaced your old hover) --- */
    div[data-testid="stMetric"]:hover {
        transform: translateZ(100px) rotateX(15deg) rotateY(10deg) scale(1.1);
        box-shadow: 0 25px 60px 0 rgba(0, 0, 0, 0.6);
        border-color: rgba(255, 255, 255, 0.6);
    }
    
    /* --- NEW: Add a 'pop' effect to the metric text on hover --- */
    div[data-testid="stMetric"]:hover [data-testid="stMetricValue"],
    div[data-testid="stMetric"]:hover label {
        transform: scale(1.05);
        text-shadow: 0 0 15px rgba(255, 255, 255, 0.7);
        transition: all 0.3s ease-in-out;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"],
    div[data-testid="stMetric"] label {
        transition: all 0.3s ease-in-out; /* Smooth transition back */
    }

    div[data-testid="stMetric"] > div {
        background: transparent;
    }
    
    div[data-testid="stMetric"] label {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
    }
    
    /* Expander styling */
    div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 1rem 0;
        transition: all 0.3s ease; /* --- 3D CHANGE --- */
        transform: translateZ(15px); /* --- 3D CHANGE (Default float) --- */
    }

    /* --- 3D CHANGE (Added hover effect) --- */
    div[data-testid="stExpander"]:hover {
        transform: translateZ(40px) scale(1.02);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    /* Dataframe styling */
    div[data-testid="stDataFrame"] {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(15px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 1rem;
        transition: all 0.3s ease; /* --- 3D CHANGE --- */
        transform: translateZ(15px); /* --- 3D CHANGE (Default float) --- */
    }
    
    /* --- 3D CHANGE (Added hover effect) --- */
    div[data-testid="stDataFrame"]:hover {
        transform: translateZ(50px) rotateX(5deg) scale(1.02);
        box-shadow: 0 12px 35px rgba(0,0,0,0.35);
    }

    /* Center align text in dataframe cells */
    div[data-testid="stDataFrame"] div[data-testid="stHorizontalBlock"] > div {
        text-align: center;
    }
    
    /* Chart containers */
    div[data-testid="stPlotlyChart"] {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 1rem;
        transition: all 0.3s ease-out; /* --- 3D CHANGE (Added ease-out) --- */
        transform: translateZ(20px); /* --- 3D CHANGE (Default float) --- */
        transform-style: preserve-3d; /* --- 3D CHANGE --- */
    }
    
    /* --- 3D CHANGE (Replaced your old hover) --- */
    div[data-testid="stPlotlyChart"]:hover {
        transform: translateZ(80px) rotateX(10deg) rotateY(5deg) scale(1.05);
        box-shadow: 0 20px 50px 0 rgba(0, 0, 0, 0.5);
        border-color: rgba(255, 255, 255, 0.5);
    }
    
    /* Button styling */
    .stButton > button {
        background: rgba(255, 255, 255, 0.15);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 12px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        transform: translateZ(10px); /* --- 3D CHANGE --- */
    }
    
    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.25);
        border-color: rgba(255, 255, 255, 0.5);
        transform: translateY(-2px) translateZ(30px); /* --- 3D CHANGE --- */
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #ff00cc 0%, #333399 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        transform: translateZ(10px); /* --- 3D CHANGE --- */
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-3px) translateZ(30px); /* --- 3D CHANGE --- */
        box-shadow: 0 8px 30px rgba(255, 0, 204, 0.5);
    }
    
    /* Selectbox styling */
    div[data-baseweb="select"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transform: translateZ(10px); /* --- 3D CHANGE --- */
    }
    
    /* Title styling */
    h1, h2, h3 {
        color: white !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
        transform: translateZ(10px); /* --- 3D CHANGE --- */
    }
    
    h1 {
        font-size: 3rem !important;
        background: linear-gradient(135deg, #ffffff 0%, #e0e0e0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Text styling */
    p, label, span {
        color: rgba(255, 255, 255, 0.95) !important;
        transform: translateZ(5px); /* --- 3D CHANGE --- */
    }
    
    /* Login form specific */
    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.25);
        padding: 3rem;
        box-shadow: 0 15px 50px 0 rgba(0, 0, 0, 0.5);
        animation: slideUp 0.5s ease-out;
        transform: translateZ(50px); /* --- 3D CHANGE --- */
        transform-style: preserve-3d; /* --- 3D CHANGE --- */
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(30px) translateZ(50px); /* --- 3D CHANGE --- */
        }
        to {
            opacity: 1;
            transform: translateY(0) translateZ(50px); /* --- 3D CHANGE --- */
        }
    }
    
    /* Input field styling */
    input[type="password"], input[type="text"] {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
        color: white !important;
        padding: 0.75rem !important;
        transform: translateZ(10px); /* --- 3D CHANGE --- */
    }
    
    input[type="password"]:focus, input[type="text"]:focus {
        border-color: rgba(255, 255, 255, 0.6) !important;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.3);
    }
    
    /* Animation for page load */
    .element-container {
        animation: fadeIn 0.6s ease-in;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
</style>
"""

@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_excel(file_path)
        for col in [COL_COLLEGE, COL_NATIONALITY, COL_GENDER, COL_HOD_NAME, COL_HOD_PHONE, COL_HOD_MAIL]:
            if col in df.columns:
                df[col] = df[col].fillna('Unknown')
        return df
    except FileNotFoundError:
        st.error(f"❌ ERROR: The file '{file_path}' was not found.")
        st.info("💡 Please make sure the Excel file is in the same directory as the dashboard script.")
        return None
    except Exception as e:
        st.error(f"❌ An error occurred while reading the Excel file: {e}")
        return None

def check_password():
    if st.session_state.get("password_correct", False):
        return True

    st.markdown(ENHANCED_STYLES, unsafe_allow_html=True)
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("🔐 Secure Access")
        st.markdown("### Welcome Back!")
        st.write("Please enter your credentials to continue")
        
        with st.form("password_form"):
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("🚀 Log In", use_container_width=True)
            
            if submitted:
                if password == st.secrets["password"]:
                    st.session_state["password_correct"] = True
                    st.rerun()
                else:
                    st.error("😕 Incorrect password. Please try again.")
    
    return False

def main():
    if not check_password():
        st.stop()

    st.markdown(ENHANCED_STYLES, unsafe_allow_html=True)
    
    df = load_data(EXCEL_FILE)
    
    if df is None:
        st.warning("⚠️ Dashboard cannot be displayed because the data could not be loaded.")
        return

    # --- Header with logout ---
    col1, col2 = st.columns([0.88, 0.12])
    with col1:
        st.title('🎓 Dashboard')
        st.markdown("### Real-time insights and data management")
    with col2:
        st.write("")  # Spacing
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state["password_correct"] = False
            st.rerun()

    st.markdown("---")

    # --- Filters ---
    with st.expander("🔍 **Advanced Filters**", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            college_options = ['All'] + sorted(df[COL_COLLEGE].unique().tolist())
            selected_college = st.selectbox('🏫 College', college_options)
        
        with col2:
            nationality_options = ['All'] + sorted(
                df[df[COL_COLLEGE] == selected_college][COL_NATIONALITY].unique() 
                if selected_college != 'All' else df[COL_NATIONALITY].unique()
            )
            selected_nationality = st.selectbox('🌍 Nationality', nationality_options)
        
        with col3:
            if selected_college != 'All' and selected_nationality != 'All':
                gender_data = df[(df[COL_COLLEGE] == selected_college) & (df[COL_NATIONALITY] == selected_nationality)]
            elif selected_college != 'All':
                gender_data = df[df[COL_COLLEGE] == selected_college]
            elif selected_nationality != 'All':
                gender_data = df[df[COL_NATIONALITY] == selected_nationality]
            else:
                gender_data = df
            
            gender_options = ['All'] + sorted(gender_data[COL_GENDER].unique())
            selected_gender = st.selectbox('👤 Gender', gender_options)

    # --- Apply filters ---
    filtered_df = df.copy()
    if selected_college != 'All':
        filtered_df = filtered_df[filtered_df[COL_COLLEGE] == selected_college]
    if selected_nationality != 'All':
        filtered_df = filtered_df[filtered_df[COL_NATIONALITY] == selected_nationality]
    if selected_gender != 'All':
        filtered_df = filtered_df[filtered_df[COL_GENDER] == selected_gender]

    st.markdown("<br>", unsafe_allow_html=True)

    # --- KPI Metrics ---
    st.markdown("## 📊 Key Metrics")
    col1, col2, col3 = st.columns(3)
    
    total_students = len(filtered_df)
    total_colleges = filtered_df[COL_COLLEGE].nunique()
    total_nationalities = filtered_df[COL_NATIONALITY].nunique()
    
    with col1:
        st.metric("👥 Total Students", f"{total_students:,}")
    with col2:
        st.metric("🏫 Total Colleges", f"{total_colleges:,}")
    with col3:
        st.metric("🌍 Nationalities", f"{total_nationalities:,}")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Visualizations ---
    st.markdown("## 📈 Data Visualizations")
    
    if not filtered_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            nationality_counts = filtered_df[COL_NATIONALITY].value_counts().reset_index()
            nationality_counts.columns = [COL_NATIONALITY, 'Count']
            
            fig_bar = px.bar(
                nationality_counts,
                x=COL_NATIONALITY,
                y='Count',
                title='<b>Students by Nationality</b>',
                color='Count',
                color_continuous_scale='Turbo'
            )
            fig_bar.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                font_family='Inter',
                title_font_size=18,
                margin=dict(t=60, l=30, r=30, b=30),
                showlegend=False,
                xaxis_title="",
                yaxis_title="Number of Students"
            )
            fig_bar.update_traces(marker_line_color='rgba(255,255,255,0.3)', marker_line_width=1.5)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            gender_counts = filtered_df[COL_GENDER].value_counts()
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=gender_counts.index,
                values=gender_counts.values,
                hole=0.4,
                marker=dict(
                    colors=px.colors.qualitative.Vivid,
                    line=dict(color='rgba(255,255,255,0.3)', width=2)
                ),
                textinfo='label+percent',
                textfont=dict(size=14, color='white', family='Inter')
            )])
            
            fig_pie.update_layout(
                title='<b>Gender Distribution</b>',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                font_family='Inter',
                title_font_size=18,
                margin=dict(t=60, l=30, r=30, b=30),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5
                )
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # College distribution (full width)
        college_counts = filtered_df[COL_COLLEGE].value_counts().reset_index()
        college_counts.columns = [COL_COLLEGE, 'Count']
        
        fig_college = px.bar(
            college_counts,
            x=COL_COLLEGE,
            y='Count',
            title='<b>Students by College</b>',
            color='Count',
            color_continuous_scale='Cividis'
        )
        fig_college.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            font_family='Inter',
            title_font_size=20,
            margin=dict(t=60, l=30, r=30, b=50),
            showlegend=False,
            xaxis_title="",
            yaxis_title="Number of Students",
            height=400
        )
        fig_college.update_traces(marker_line_color='rgba(255,255,255,0.3)', marker_line_width=1.5)
        st.plotly_chart(fig_college, use_container_width=True)
    else:
        st.info("📭 No data available for the current selection.")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Student Data Table ---
    st.markdown("## 📋 Filtered Data")
    st.markdown(f"**Filters Applied:** {selected_college} → {selected_nationality} → {selected_gender}")
    st.markdown(f"**Records Found:** `{len(filtered_df)}`")
    
    if not filtered_df.empty:
        st.dataframe(
            filtered_df[[COL_NAME, COL_PHONE, COL_WHATSAPP, COL_COLLEGE, COL_NATIONALITY, COL_GENDER]],
            use_container_width=True,
            height=400
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # --- HOD Information Section ---
    st.markdown("## 👔 HOD Information")
    hod_cols_to_display = [COL_HOD_NAME, COL_HOD_PHONE, COL_HOD_MAIL]
    
    # Check if all required HOD columns exist in the dataframe
    if all(col in filtered_df.columns for col in hod_cols_to_display):
        # Get unique HOD information from the filtered data
        hod_df = filtered_df[hod_cols_to_display].drop_duplicates().dropna(how='all')

        if not hod_df.empty:
            st.markdown(f"**Records Found:** `{len(hod_df)}`")
            st.dataframe(
                hod_df,
                use_container_width=True
            )
        else:
            st.info("📭 No HOD information available for the current selection.")
    else:
        st.warning("⚠️ HOD columns ('HOD Name', 'HOD Contact No', 'HOD Mail ID') not found in the Excel file.")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Download Button ---
    if not filtered_df.empty:
        # Download button
        @st.cache_data
        def convert_df_to_csv(df_to_convert):
            return df_to_convert.to_csv(index=False).encode('utf-8')
        
        csv_data = convert_df_to_csv(filtered_df)
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv_data,
            file_name='student_data_filtered.csv',
            mime='text/csv',
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Student Details ---
    st.markdown("## 👤 View Full Details")
    
    student_names = ['🔍 Select a student...'] + sorted(filtered_df[COL_NAME].unique().tolist())
    selected_student_name = st.selectbox("Select a student to see their full details", student_names, label_visibility="collapsed")
    
    if selected_student_name and not selected_student_name.startswith('🔍'):
        student_data = filtered_df[filtered_df[COL_NAME] == selected_student_name].iloc[0]
        
        with st.expander(f"📇 **Contact Card: {student_data[COL_NAME]}**", expanded=True):
            col1, col2 = st.columns(2)
            
            def clean_phone(num):
                return ''.join(filter(str.isdigit, str(num)))
            
            items = list(student_data.items())
            for i, (col_name, col_value) in enumerate(items):
                current_col = col1 if i % 2 == 0 else col2
                
                # Format phone numbers to remove decimals
                def format_phone_display(num):
                    return f"{int(num)}" if pd.notna(num) and isinstance(num, (int, float)) else num

                if col_name == COL_PHONE and pd.notna(col_value) and str(col_value).strip():
                    current_col.markdown(f"**📞 {col_name}:** {format_phone_display(col_value)} [Call](tel:{clean_phone(col_value)})")
                elif col_name == COL_WHATSAPP and pd.notna(col_value) and str(col_value).strip():
                    current_col.markdown(f"**💬 {col_name}:** {format_phone_display(col_value)} [WhatsApp](https://wa.me/{clean_phone(col_value)})")
                elif col_name == COL_HOD_PHONE and pd.notna(col_value):
                    current_col.markdown(f"**👔 {col_name}:** {format_phone_display(col_value)} ([📞](tel:{clean_phone(col_value)}) | [💬](https://wa.me/{clean_phone(col_value)}))")
                else:
                    current_col.markdown(f"**{col_name}:** {col_value}")

if __name__ == "__main__":
    main()