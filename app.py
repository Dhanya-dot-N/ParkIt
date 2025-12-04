import streamlit as st
import pandas as pd
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Accessible Parking Bengaluru",
    page_icon="♿",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .login-container {
        max-width: 500px;
        margin: 50px auto;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .parking-card {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .available {
        background-color: #4caf50;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
    }
    .limited {
        background-color: #ff9800;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
    }
    .full {
        background-color: #f44336;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
    }
    .feature-badge {
        background-color: #e3f2fd;
        color: #1976d2;
        padding: 0.3rem 0.6rem;
        border-radius: 5px;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
    }
    .user-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for user management
if 'users' not in st.session_state:
    st.session_state.users = {}
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# User authentication functions
def register_user(email, password, name, accessibility_needs, proof_uploaded):
    if email in st.session_state.users:
        return False, "Email already registered"
    
    st.session_state.users[email] = {
        'password': password,
        'name': name,
        'accessibility_needs': accessibility_needs,
        'proof_uploaded': proof_uploaded,
        'registered_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return True, "Registration successful!"

def login_user(email, password):
    if email not in st.session_state.users:
        return False, "Email not found"
    
    if st.session_state.users[email]['password'] == password:
        st.session_state.logged_in = True
        st.session_state.current_user = email
        return True, "Login successful!"
    else:
        return False, "Incorrect password"

def logout_user():
    st.session_state.logged_in = False
    st.session_state.current_user = None

# Parking data function
def get_parking_data():
    return [
        {
            'id': 1,
            'name': 'Orion Mall',
            'area': 'Brigade Gateway, Rajajinagar',
            'lat': 12.9898,
            'lng': 77.5351,
            'available': 4,
            'total': 8,
            'distance': 5.2,
            'type': 'Mall',
            'icon': '🏬',
            'features': ['Wheelchair ramp', 'Accessible restroom', 'Elevator access'],
            'contact': '+91 80 4723 7000'
        },
        {
            'id': 2,
            'name': 'Phoenix Marketcity',
            'area': 'Whitefield',
            'lat': 12.9975,
            'lng': 77.6969,
            'available': 6,
            'total': 10,
            'distance': 8.7,
            'type': 'Mall',
            'icon': '🏬',
            'features': ['Wide parking bays', 'Wheelchair ramp', 'Accessible restroom', 'Security assistance'],
            'contact': '+91 80 4175 5000'
        },
        {
            'id': 3,
            'name': 'UB City Mall',
            'area': 'Vittal Mallya Road',
            'lat': 12.9726,
            'lng': 77.5999,
            'available': 2,
            'total': 6,
            'distance': 1.8,
            'type': 'Mall',
            'icon': '🏬',
            'features': ['Valet service', 'Wheelchair ramp', 'Premium access'],
            'contact': '+91 80 4132 6666'
        },
        {
            'id': 4,
            'name': 'Bangalore Airport',
            'area': 'Kempegowda International Airport',
            'lat': 13.1986,
            'lng': 77.7066,
            'available': 12,
            'total': 20,
            'distance': 35.4,
            'type': 'Transport',
            'icon': '✈️',
            'features': ['Drop-off assistance', 'Wheelchair service', 'Buggy service', 'Priority check-in'],
            'contact': '+91 80 6678 2251'
        },
        {
            'id': 5,
            'name': 'Victoria Hospital',
            'area': 'Fort, Bengaluru',
            'lat': 12.9698,
            'lng': 77.5855,
            'available': 8,
            'total': 15,
            'distance': 2.1,
            'type': 'Hospital',
            'icon': '🏥',
            'features': ['Near entrance', 'Wheelchair available', 'Staff assistance', '24/7 access'],
            'contact': '+91 80 2670 1150'
        },
        {
            'id': 6,
            'name': 'Manipal Hospital',
            'area': 'HAL Airport Road',
            'lat': 12.9591,
            'lng': 77.6450,
            'available': 5,
            'total': 12,
            'distance': 6.8,
            'type': 'Hospital',
            'icon': '🏥',
            'features': ['Covered parking', 'Wheelchair service', 'Porter service', 'Emergency access'],
            'contact': '+91 80 2502 4444'
        },
        {
            'id': 7,
            'name': 'Cubbon Park',
            'area': 'Kasturba Road',
            'lat': 12.9762,
            'lng': 77.5929,
            'available': 0,
            'total': 4,
            'distance': 1.2,
            'type': 'Public',
            'icon': '🌳',
            'features': ['Paved pathways', 'Near main entrance'],
            'contact': '+91 80 2286 4362'
        },
        {
            'id': 8,
            'name': 'Lalbagh Botanical Garden',
            'area': 'Mavalli',
            'lat': 12.9507,
            'lng': 77.5848,
            'available': 3,
            'total': 5,
            'distance': 3.4,
            'type': 'Public',
            'icon': '🌳',
            'features': ['Wheelchair rental', 'Paved paths', 'Accessible entry'],
            'contact': '+91 80 2657 8072'
        },
        {
            'id': 9,
            'name': 'MG Road Metro Station',
            'area': 'Mahatma Gandhi Road',
            'lat': 12.9753,
            'lng': 77.6057,
            'available': 4,
            'total': 8,
            'distance': 1.5,
            'type': 'Transport',
            'icon': '🚇',
            'features': ['Elevator access', 'Wide entry gates', 'Staff assistance', 'CCTV monitored'],
            'contact': '+91 80 2535 2222'
        },
        {
            'id': 10,
            'name': 'Garuda Mall',
            'area': 'Magrath Road',
            'lat': 12.9716,
            'lng': 77.6188,
            'available': 3,
            'total': 6,
            'distance': 2.8,
            'type': 'Mall',
            'icon': '🏬',
            'features': ['Elevator access', 'Wide parking bays', 'Security assistance'],
            'contact': '+91 80 4115 5000'
        }
    ]

def get_availability_status(available, total):
    if available == 0:
        return "full", "Full"
    ratio = available / total
    if ratio < 0.3:
        return "limited", "Limited"
    elif ratio < 0.6:
        return "limited", "Moderate"
    else:
        return "available", "Available"

# Login/Signup Page
def show_login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: #667eea;">♿ Accessible Parking</h1>
            <h3 style="color: #764ba2;">Bengaluru</h3>
            <p style="color: #666;">Find accessible parking spaces designed for your convenience</p>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            st.subheader("Welcome Back!")
            login_email = st.text_input("Email", key="login_email", placeholder="your.email@example.com")
            login_password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
            
            if st.button("Login", use_container_width=True, type="primary"):
                if login_email and login_password:
                    success, message = login_user(login_email, login_password)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.warning("Please fill in all fields")
        
        with tab2:
            st.subheader("Create Your Account")
            signup_name = st.text_input("Full Name", key="signup_name", placeholder="Your full name")
            signup_email = st.text_input("Email", key="signup_email", placeholder="your.email@example.com")
            signup_password = st.text_input("Password", type="password", key="signup_password", placeholder="Create a password")
            signup_confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password", placeholder="Re-enter password")
            
            st.markdown("#### Accessibility Information")
            accessibility_needs = st.multiselect(
                "Select your accessibility needs (optional)",
                ["Wheelchair user", "Mobility assistance", "Visual impairment", "Hearing impairment", "Other"],
                help="This helps us provide better recommendations"
            )
            
            st.markdown("#### Proof of Accessibility Permit (Optional)")
            st.info("📄 Uploading proof helps verify your eligibility for reserved parking spaces. This is optional but recommended.")
            uploaded_file = st.file_uploader(
                "Upload disability certificate/accessibility permit",
                type=['pdf', 'jpg', 'jpeg', 'png'],
                help="Accepted formats: PDF, JPG, PNG (Max 5MB)"
            )
            
            if st.button("Create Account", use_container_width=True, type="primary"):
                if signup_name and signup_email and signup_password and signup_confirm_password:
                    if signup_password != signup_confirm_password:
                        st.error("Passwords don't match!")
                    elif len(signup_password) < 6:
                        st.error("Password must be at least 6 characters long")
                    else:
                        success, message = register_user(
                            signup_email,
                            signup_password,
                            signup_name,
                            accessibility_needs,
                            uploaded_file is not None
                        )
                        if success:
                            st.success(message)
                            st.info("Please login with your credentials")
                        else:
                            st.error(message)
                else:
                    st.warning("Please fill in all required fields")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Main parking locator page
def show_parking_page():
    # User info banner
    user_data = st.session_state.users[st.session_state.current_user]
    
    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown(f"""
        <div class="user-badge">
            👋 Welcome back, <strong>{user_data['name']}</strong>!
            {'✅ Verified Account' if user_data['proof_uploaded'] else ''}
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("Logout", type="secondary"):
            logout_user()
            st.rerun()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>♿ Accessible Parking Bengaluru</h1>
        <p>Find accessible parking spaces designed for your convenience</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Important information banner
    st.info("ℹ️ **Important Information:** All listed parking spaces are designed with accessibility in mind. Free parking is available at most locations with valid accessibility permit.")
    
    # Location display
    st.markdown("📍 **Your Location:** Bengaluru, Karnataka")
    
    # Filters
    st.markdown("### Filter Parking Spaces")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        show_all = st.checkbox("All Locations", value=True)
    with col2:
        show_available = st.checkbox("Available Only")
    with col3:
        show_mall = st.checkbox("🏬 Malls")
    with col4:
        show_hospital = st.checkbox("🏥 Hospitals")
    with col5:
        show_transport = st.checkbox("🚇 Transport")
    with col6:
        show_public = st.checkbox("🌳 Public Places")
    
    # Get and filter data
    parking_spaces = get_parking_data()
    filtered_spaces = parking_spaces.copy()
    
    # Apply filters
    if not show_all:
        filtered_spaces = []
        for space in parking_spaces:
            if show_available and space['available'] == 0:
                continue
            if show_mall and space['type'] != 'Mall':
                continue
            if show_hospital and space['type'] != 'Hospital':
                continue
            if show_transport and space['type'] != 'Transport':
                continue
            if show_public and space['type'] != 'Public':
                continue
            if show_available or show_mall or show_hospital or show_transport or show_public:
                filtered_spaces.append(space)
    
    if not show_all and not any([show_available, show_mall, show_hospital, show_transport, show_public]):
        filtered_spaces = []
    
    # Sort by distance
    filtered_spaces.sort(key=lambda x: x['distance'])
    
    # Display parking spaces
    st.markdown("---")
    st.markdown(f"### Showing {len(filtered_spaces)} Parking Locations")
    
    # Create grid layout
    for i in range(0, len(filtered_spaces), 2):
        cols = st.columns(2)
        
        for j, col in enumerate(cols):
            if i + j < len(filtered_spaces):
                space = filtered_spaces[i + j]
                status_class, status_text = get_availability_status(space['available'], space['total'])
                
                with col:
                    with st.container():
                        col_a, col_b = st.columns([3, 1])
                        with col_a:
                            st.markdown(f"## {space['icon']} {space['name']}")
                            st.markdown(f"**{space['area']}**")
                        with col_b:
                            st.markdown(f'<div class="{status_class}">{status_text}</div>', unsafe_allow_html=True)
                        
                        st.markdown(f"📍 **Distance:** {space['distance']} km away")
                        st.markdown(f"♿ **Available:** {space['available']} / {space['total']} accessible spaces")
                        st.markdown(f"💵 **Parking:** FREE")
                        
                        if space['total'] > 0:
                            progress = space['available'] / space['total']
                            st.progress(progress)
                        
                        st.markdown("**Accessibility Features:**")
                        features_html = " ".join([f'<span class="feature-badge">{f}</span>' for f in space['features'][:3]])
                        if len(space['features']) > 3:
                            features_html += f' <span class="feature-badge">+{len(space["features"]) - 3} more</span>'
                        st.markdown(features_html, unsafe_allow_html=True)
                        
                        st.markdown(f"📞 **Contact:** {space['contact']}")
                        
                        btn_col1, btn_col2 = st.columns(2)
                        with btn_col1:
                            maps_url = f"https://www.google.com/maps/dir/?api=1&destination={space['lat']},{space['lng']}"
                            st.link_button("Get Directions", maps_url, use_container_width=True)
                        with btn_col2:
                            phone_url = f"tel:{space['contact']}"
                            st.link_button("Call for Assistance", phone_url, use_container_width=True)
                        
                        st.markdown("---")
    
    # Sidebar
    st.sidebar.markdown("## Your Profile")
    st.sidebar.markdown(f"**Name:** {user_data['name']}")
    st.sidebar.markdown(f"**Email:** {st.session_state.current_user}")
    if user_data['accessibility_needs']:
        st.sidebar.markdown(f"**Needs:** {', '.join(user_data['accessibility_needs'])}")
    st.sidebar.markdown(f"**Verified:** {'✅ Yes' if user_data['proof_uploaded'] else '❌ No'}")
    
    st.sidebar.markdown("## About This App")
    st.sidebar.info("""
    This app helps you find accessible parking spaces across Bengaluru designed for maximum convenience and accessibility.
    
    **Features:**
    - Real-time availability
    - Comprehensive accessibility information
    - Free parking locations
    - Direct contact information
    - Distance from your location
    """)
    
    st.sidebar.markdown("## Statistics")
    total_spaces = sum(space['total'] for space in parking_spaces)
    available_spaces = sum(space['available'] for space in parking_spaces)
    st.sidebar.metric("Total Accessible Spaces", total_spaces)
    st.sidebar.metric("Currently Available", available_spaces)
    st.sidebar.metric("Locations", len(parking_spaces))

# Main app logic
if st.session_state.logged_in:
    show_parking_page()
else:
    show_login_page()