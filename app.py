import streamlit as st
import pandas as pd
import math

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
</style>
""", unsafe_allow_html=True)

# Initialize parking data
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

# Header
st.markdown("""
<div class="main-header">
    <h1>♿ Accessible Parking Bengaluru</h1>
    <p>Find disabled-friendly parking spaces across the city</p>
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
                # Card container
                with st.container():
                    # Header with name and status
                    col_a, col_b = st.columns([3, 1])
                    with col_a:
                        st.markdown(f"## {space['icon']} {space['name']}")
                        st.markdown(f"**{space['area']}**")
                    with col_b:
                        st.markdown(f'<div class="{status_class}">{status_text}</div>', unsafe_allow_html=True)
                    
                    # Details
                    st.markdown(f"📍 **Distance:** {space['distance']} km away")
                    st.markdown(f"♿ **Available:** {space['available']} / {space['total']} accessible spaces")
                    st.markdown(f"💵 **Parking:** FREE")
                    
                    # Progress bar
                    if space['total'] > 0:
                        progress = space['available'] / space['total']
                        st.progress(progress)
                    
                    # Features
                    st.markdown("**Accessibility Features:**")
                    features_html = " ".join([f'<span class="feature-badge">{f}</span>' for f in space['features'][:3]])
                    if len(space['features']) > 3:
                        features_html += f' <span class="feature-badge">+{len(space["features"]) - 3} more</span>'
                    st.markdown(features_html, unsafe_allow_html=True)
                    
                    # Contact
                    st.markdown(f"📞 **Contact:** {space['contact']}")
                    
                    # Action buttons
                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        # Create Google Maps directions URL
                        maps_url = f"https://www.google.com/maps/dir/?api=1&destination={space['lat']},{space['lng']}"
                        st.link_button("Get Directions", maps_url, use_container_width=True)
                    with btn_col2:
                        # Create phone call URL
                        phone_url = f"tel:{space['contact']}"
                        st.link_button("Call for Assistance", phone_url, use_container_width=True)
                    
                    st.markdown("---")

# Selected space details in sidebar
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