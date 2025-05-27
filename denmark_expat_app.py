import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Page configuration
st.set_page_config(
    page_title="Denmark Expat Initiatives Map",
    page_icon="🇩🇰",
    layout="wide"
)

# Danish city coordinates lookup
hyperlink_data = {'Workindenmark/EURES': 'https://www.workindenmark.dk', 'Welcome September': 'https://www.odense.dk/ico/events/welcome-day', 'Young Professionals in Denmark': 'https://www.students.aau.dk/choices-along-the-way-and-jobs/gain-experience-while-you-study/young-professionals-in-denmark', 'SIRI Family Member Support': 'https://www.nyidanmark.dk/en-GB', 'Relocare Spouse Job Search': 'https://spousecare.dk/en/our-mission/', 'International House North Denmark': 'https://ihnd.dk', 'IHND Spouse Support (Spouse Space)': 'https://ihnd.dk/spouse-space', 'European School Copenhagen': 'https://escph.dk', 'International Montessori School': 'https://internationalschools.dk/skoler/international-montessori-school-copenhagen/', 'Sankt Petri Skole': 'https://www.sanktpetriskole.dk/en/', 'Viking International School': 'https://www.vikinginternationalschool.dk/', 'Waldorf International School': 'https://waldorf.dk/en/', 'Aarhus International School': 'https://ais-aarhus.com/', 'Henriette Hørlücks Skole': 'https://www.hhs.dk/', 'Skipper Clement Skolen': 'https://www.skipperclementskolen.dk/', 'Esbjerg International School': 'https://www.eis.school/', 'Lolland International School': 'https://www.lollandinternationalschool.dk/', 'Bernadotteskolen': 'https://www.bernadotteskolen.dk/', 'International School of Hellerup': 'https://ish.dk/', 'Rygaards Skole': 'https://rygaards.com/', 'Prins Henriks skole': 'https://prinshenriksskole.dk/', "Skt. Josef's International School": 'https://sktjosef.dk/international/', 'Sønderborg International School': 'https://sis.sonderborg.dk/', 'Viborg private Realskole': 'https://viborgprivaterealskole.dk/', 'Copenhagen Career Program for Spouses': 'https://ihcph.kk.dk/en/copenhagen-career-program', 'International Community Aarhus': 'https://internationalcommunity.dk/', 'International Employment Unit (Aarhus)': 'https://international.aarhus.dk/job/international-employment-unit/', 'Aarhus City Welcome': 'https://international.aarhus.dk/events/aarhus-city-welcome/', 'AU Expat Partner Programme': 'https://international.au.dk/life/expat-partner-programme', 'International Community Odense': 'https://internationalcommunityodense.dk/', 'Host Programme (Odense)': 'https://internationalcommunityodense.dk/host-programme', 'International Welcome Fund (Lolland)': 'https://www.lolland.dk/borger/international-welcome-fund', 'Healthcare Professionals Program (Lolland)': 'https://www.lolland.dk/borger/healthcare-professionals', 'Virksomhedsforum (Kalundborg)': 'https://www.kalundborg.dk/erhverv/virksomhedsforum', 'Liv i Kalundborg': 'https://www.kalundborg.dk/borger/kultur-og-fritid/liv-i-kalundborg', 'International Policy Framework (Kolding)': 'https://www.kolding.dk/erhverv/international-policy', 'Career Kick Start (UCPH)': 'https://studies.ku.dk/masters/career-kick-start/', 'Greater Copenhagen Career Program': 'https://www.cphbusiness.dk/english/programmes-and-courses/greater-copenhagen-career-programme/', 'Work & Study Programme (Computer Science, Aarhus)': 'https://cs.au.dk/education/work-and-study-programme', 'Talent to a Green Denmark': 'https://studenterhusaarhus.dk/en/talent-to-a-green-denmark/', 'AU Student Job Fair': 'https://studerende.au.dk/en/career/jobbank/job-fairs', 'Studenterhus Aarhus Social Programs': 'https://studenterhusaarhus.dk/en/', 'IT and Academic Job Fair (Odense)': 'https://itjobfair.dk/', 'SDU Career Services': 'https://mitsdu.dk/en/mit_studie/karriere', 'Roskilde University Career Services': 'https://ruc.dk/en/career-guidance', 'SDU Spouse Support': 'https://mitsdu.dk/en/mit_studie/ny_i_danmark/familie', 'VIA University Partnerships': 'https://en.via.dk/about-via/partnerships', 'VIA University College Career Services': 'https://en.via.dk/student/career', 'LEGO Family Programme': 'https://www.lego.com/en-us/careers/working-at-the-lego-group/relocation', 'LEGO Family Onboarding': 'https://www.lego.com/en-us/careers/working-at-the-lego-group/relocation', 'CPH STAGE Festival': 'https://www.cphstage.dk/english/', 'Spousehouse Vejle': 'https://www.facebook.com/spousehousevejle/'}

CITY_COORDS = {
    'Copenhagen': [55.6761, 12.5683],
    'Aarhus': [56.1629, 10.2039],
    'Odense': [55.4038, 10.4024],
    
    'Kalundborg': [55.6794, 11.0888],
    'Kolding': [55.4904, 9.4719],
    'Aalborg': [57.0488, 9.9217],
    'Esbjerg': [55.4700, 8.4520],
    'Horsens': [55.8607, 9.8500],
    'Hellerup': [55.7267, 12.5700],
    'Frederiksberg': [55.6867, 12.5339],
    'Roskilde': [55.6415, 12.0803],
    'Hørsholm': [55.8817, 12.4983],
    'Næstved': [55.2297, 11.7603],
    'Sønderborg': [54.9089, 9.7927],
    'Billund': [55.7308, 9.1153],
    'Ikast': [56.1386, 9.1575],
    'Holbæk': [55.7167, 11.7167],
    'Viborg': [56.4533, 9.4017],
    'Maribo': [54.7719, 11.5008],
    'Nordhavn': [55.7061, 12.5914],
    'Vejle': [55.7058, 9.5378],
    'National': [56.2639, 9.5018]
}

# Copenhagen Capacity recommendation mapping (EXACTLY as they wrote it)
RECOMMENDATIONS = {
    '1a': "Job market accessibility - Targeted programs",
    '1b': "Job market accessibility - Job portals with relevant jobs", 
    '2a': "International students - Career services",
    '2b': "International students - Integration resources",
    '3a': "Inclusion and belonging - Onboarding programs",
    '3b': "Inclusion and belonging - More social events",
    '3c': "Inclusion and belonging - Encourage cultural engagement",
    '4a': "Spouses/partners & family - Job opportunities",
    '4b': "Spouses/partners & family - Inclusive education for children"
}

# Color mapping for Copenhagen Capacity's 4 main categories
REC_COLORS = {
    '1a': 'blue', '1b': 'lightblue',                       # Job market - blues
    '2a': 'green', '2b': 'lightgreen',                     # Students - greens  
    '3a': 'red', '3b': 'lightred', '3c': 'darkred',        # Inclusion - reds
    '4a': 'purple', '4b': 'pink'                           # Family - purples
}

@st.cache_data
def load_data():
    # Restructured data following Copenhagen Capacity's official 4 recommendations
    data = [
        # National programs
        {'location': 'National', 'recommendation': '1a', 'program': 'Workindenmark/EURES', 'organization': 'Government/EU partnership', 'status': 'Active'},
        {'location': 'National', 'recommendation': '3b', 'program': 'Welcome September', 'organization': 'Life in Denmark', 'status': 'Active'},
        {'location': 'National', 'recommendation': '2a', 'program': 'Young Professionals in Denmark', 'organization': 'Confederation of Danish Industry', 'status': 'Active'},
        {'location': 'National', 'recommendation': '2a', 'program': 'Student Job Portals', 'organization': 'Workindenmark', 'status': 'Active'},
        {'location': 'National', 'recommendation': '4a', 'program': 'SIRI Family Member Support', 'organization': 'Danish Agency for International Recruitment', 'status': 'Active'},
        {'location': 'National', 'recommendation': '4a', 'program': 'Relocare Spouse Job Search', 'organization': 'Private Relocation Services', 'status': 'Active'},
        
        # Copenhagen comprehensive programs
        {'location': 'Copenhagen', 'recommendation': '2a', 'program': 'Career Kick Start', 'organization': 'University of Copenhagen', 'status': 'Active'},
        {'location': 'Copenhagen', 'recommendation': '2a', 'program': 'Greater Copenhagen Career Program', 'organization': 'Copenhagen Capacity', 'status': 'Active'},
        {'location': 'Copenhagen', 'recommendation': '2a', 'program': 'Young Professionals in Denmark', 'organization': 'Confederation of Danish Industry', 'status': 'Active'},
        {'location': 'Copenhagen', 'recommendation': '2b', 'program': 'University Career Services', 'organization': 'Danish Universities', 'status': 'Active'},
        {'location': 'Copenhagen', 'recommendation': '2b', 'program': 'Company Thesis Collaboration', 'organization': 'Universities & Employers', 'status': 'Active'},
        {'location': 'Copenhagen', 'recommendation': '4b', 'program': 'European School Copenhagen', 'organization': 'Public School', 'status': 'Active'},
        {'location': 'Copenhagen', 'recommendation': '4b', 'program': 'International Montessori School', 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Copenhagen', 'recommendation': '4b', 'program': 'Sankt Petri Skole', 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Copenhagen', 'recommendation': '4b', 'program': 'Viking International School', 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Copenhagen', 'recommendation': '4b', 'program': 'Waldorf International School', 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Copenhagen', 'recommendation': '4a', 'program': 'Copenhagen Career Program for Spouses', 'organization': 'Municipality', 'status': 'Active'},
        
        # Aarhus - comprehensive programs covering all recommendations  
        {'location': 'Aarhus', 'recommendation': '1a', 'program': 'International Community Aarhus', 'organization': 'Erhverv Aarhus', 'status': 'Active'},
        {'location': 'Aarhus', 'recommendation': '1a', 'program': 'International Employment Unit', 'organization': 'Jobcenter Aarhus', 'status': 'Active'},
        {'location': 'Aarhus', 'recommendation': '1a', 'program': 'Work & Study Programme (Computer Science)', 'organization': 'Aarhus University', 'status': 'Pilot (2025-2027)'},
        {'location': 'Aarhus', 'recommendation': '1a', 'program': 'Employer Outreach & Awareness Campaigns', 'organization': 'Erhverv Aarhus', 'status': 'Active'},
        {'location': 'Aarhus', 'recommendation': '2a', 'program': 'Talent to a Green Denmark', 'organization': 'Studenterhus Aarhus', 'status': 'Active (2023-2025)'},
        {'location': 'Aarhus', 'recommendation': '2b', 'program': 'University-Business Talent Partnerships', 'organization': 'Aarhus University', 'status': 'Active'},
        {'location': 'Aarhus', 'recommendation': '2a', 'program': 'AU Student Job Fair', 'organization': 'Aarhus University', 'status': 'Active'},
        {'location': 'Aarhus', 'recommendation': '3a', 'program': 'Aarhus City Welcome', 'organization': 'Municipality', 'status': 'Active'},
        {'location': 'Aarhus', 'recommendation': '3a', 'program': 'International Employment Unit Onboarding', 'organization': 'Jobcenter Aarhus', 'status': 'Active'},
        {'location': 'Aarhus', 'recommendation': '4a', 'program': 'AU Expat Partner Programme', 'organization': 'Aarhus University', 'status': 'Active'},
        {'location': 'Aarhus', 'recommendation': '4a', 'program': 'International Employment Unit Partner Support', 'organization': 'Jobcenter Aarhus', 'status': 'Active'},
        {'location': 'Aarhus', 'recommendation': '4b', 'program': 'Aarhus International School', 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Aarhus', 'recommendation': '3b', 'program': 'Aarhus City Welcome Events', 'organization': 'Municipality', 'status': 'Active'},
        {'location': 'Aarhus', 'recommendation': '3b', 'program': 'International Community Events', 'organization': 'Erhverv Aarhus', 'status': 'Active'},
        {'location': 'Aarhus', 'recommendation': '3b', 'program': 'Studenterhus Aarhus Social Programs', 'organization': 'Studenterhus Aarhus', 'status': 'Active'},
        {'location': 'Aarhus', 'recommendation': '3c', 'program': 'Sports Integration Initiatives', 'organization': 'Municipality & Sports Clubs', 'status': 'Active'},
        {'location': 'Aarhus', 'recommendation': '3c', 'program': 'Cultural Clubs Integration', 'organization': 'Municipality & NGOs', 'status': 'Active'},
        
        # Other major cities
        {'location': 'Odense', 'recommendation': '3a', 'program': 'International Community Odense', 'organization': 'City of Odense', 'status': 'Active'},
        {'location': 'Odense', 'recommendation': '1b', 'program': 'IT and Academic Job Fair', 'organization': 'Jobcenter Odense', 'status': 'Active'},
        {'location': 'Odense', 'recommendation': '2a', 'program': 'SDU Career Services', 'organization': 'University of Southern Denmark', 'status': 'Active'},
        {'location': 'Odense', 'recommendation': '4b', 'program': 'Henriette Hørlücks Skole', 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Odense', 'recommendation': '4a', 'program': 'Host Programme', 'organization': 'Odense Kommune', 'status': 'Active'},
        
        # Aalborg
        {'location': 'Aalborg', 'recommendation': '1a', 'program': 'International House North Denmark', 'organization': 'IHND (Municipal/Regional)', 'status': 'Active'},
        {'location': 'Aalborg', 'recommendation': '3a', 'program': 'IHND Onboarding Services', 'organization': 'IHND', 'status': 'Active'},
        {'location': 'Aalborg', 'recommendation': '4a', 'program': 'IHND Spouse Support', 'organization': 'IHND', 'status': 'Active'},
        {'location': 'Aalborg', 'recommendation': '2b', 'program': 'University/Business Network Collaboration', 'organization': 'Invest in Aalborg', 'status': 'Active'},
        {'location': 'Aalborg', 'recommendation': '3b', 'program': 'Welcome September', 'organization': 'Local Municipality', 'status': 'Active'},
        {'location': 'Aalborg', 'recommendation': '2a', 'program': 'University Career Centre', 'organization': 'Aalborg University', 'status': 'Active'},
        {'location': 'Aalborg', 'recommendation': '2b', 'program': 'Internship Programmes', 'organization': 'Aalborg University', 'status': 'Active'},
        {'location': 'Aalborg', 'recommendation': '4b', 'program': 'Skipper Clement Skolen', 'organization': 'Private School', 'status': 'Active'},
        
        # Esbjerg
        {'location': 'Esbjerg', 'recommendation': '1a', 'program': 'Jobcenter & EURES Collaboration', 'organization': 'Local Jobcenter', 'status': 'Active'},
        {'location': 'Esbjerg', 'recommendation': '2b', 'program': 'University-Company Integration', 'organization': 'University of Southern Denmark', 'status': 'Active'},
        {'location': 'Esbjerg', 'recommendation': '3b', 'program': 'Welcome September', 'organization': 'Local Municipality', 'status': 'Active'},
        {'location': 'Esbjerg', 'recommendation': '4b', 'program': 'Esbjerg International School', 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Esbjerg', 'recommendation': '4a', 'program': 'Settling-in Coordinator', 'organization': 'Municipality', 'status': 'Active'},
        
        # Smaller municipalities
        {'location': 'Maribo', 'recommendation': '3b', 'program': 'International Welcome Fund', 'organization': 'Lolland Kommune', 'status': 'Active'},
        {'location': 'Maribo', 'recommendation': '3a', 'program': 'Healthcare Professionals Program', 'organization': 'Lolland Kommune', 'status': 'Active'},
        {'location': 'Maribo', 'recommendation': '4b', 'program': 'Lolland International School', 'organization': 'Public School', 'status': 'Active'},
        {'location': 'Kalundborg', 'recommendation': '1a', 'program': 'Virksomhedsforum', 'organization': 'Kalundborg Jobcenter', 'status': 'Active'},
        {'location': 'Kalundborg', 'recommendation': '3b', 'program': 'Liv i Kalundborg', 'organization': 'Business Council', 'status': 'Active'},
        {'location': 'Kolding', 'recommendation': '1a', 'program': 'International Policy Framework', 'organization': 'Kolding Kommune', 'status': 'Active'},
        {'location': 'Kolding', 'recommendation': '3a', 'program': 'International Policy Framework', 'organization': 'Kolding Kommune', 'status': 'Active'},
        
        # International schools across Denmark (4b)
        {'location': 'Hellerup', 'recommendation': '4b', 'program': 'Bernadotteskolen', 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Hellerup', 'recommendation': '4b', 'program': 'International School of Hellerup', 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Hellerup', 'recommendation': '4b', 'program': 'Rygaards Skole', 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Frederiksberg', 'recommendation': '4b', 'program': 'Prins Henriks skole', 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Frederiksberg', 'recommendation': '1a', 'program': 'Inclusive Municipal Hiring', 'organization': 'Municipality', 'status': 'Active'},
        {'location': 'Frederiksberg', 'recommendation': '3b', 'program': 'CPH STAGE Festival', 'organization': 'Event Organizations', 'status': 'Active'},
        {'location': 'Frederiksberg', 'recommendation': '2a', 'program': 'Career Kick Start (coverage)', 'organization': 'University of Copenhagen', 'status': 'Active'},
        {'location': 'Roskilde', 'recommendation': '4b', 'program': "Skt. Josef's International School", 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Roskilde', 'recommendation': '2a', 'program': 'Roskilde University Career Services', 'organization': 'Roskilde University', 'status': 'Active'},
        {'location': 'Sønderborg', 'recommendation': '4b', 'program': 'Sønderborg International School', 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Sønderborg', 'recommendation': '4a', 'program': 'SDU Spouse Support', 'organization': 'University of Southern Denmark', 'status': 'Active'},
        {'location': 'Billund', 'recommendation': '4b', 'program': 'International School of Billund', 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Billund', 'recommendation': '4a', 'program': 'LEGO Family Programme', 'organization': 'LEGO Group', 'status': 'Active'},
        {'location': 'Billund', 'recommendation': '3a', 'program': 'LEGO Family Onboarding', 'organization': 'LEGO Group', 'status': 'Active'},
        {'location': 'Ikast', 'recommendation': '4b', 'program': 'International School Ikast-Brande', 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Viborg', 'recommendation': '4b', 'program': 'Viborg private Realskole', 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Viborg', 'recommendation': '2a', 'program': 'VIA University Partnerships', 'organization': 'VIA University', 'status': 'Active'},
        {'location': 'Horsens', 'recommendation': '4a', 'program': 'International House Horsens Spouse Support', 'organization': 'International House Horsens', 'status': 'Active'},
        {'location': 'Horsens', 'recommendation': '2a', 'program': 'VIA University College Career Services', 'organization': 'VIA University College', 'status': 'Active'},
        {'location': 'Kolding', 'recommendation': '2a', 'program': 'SDU Career Services', 'organization': 'University of Southern Denmark', 'status': 'Active'},
        {'location': 'Vejle', 'recommendation': '4a', 'program': 'Spousehouse Vejle', 'organization': 'Facebook Community Group', 'status': 'Active'},
    ]
    return pd.DataFrame(data)

    """Create folium map with filtered data"""
    m = folium.Map(location=[56.0, 10.0], zoom_start=7)
    
    if gap_mode and selected_recs:
        # Gap mode: show cities that DON'T have selected recommendations
        all_cities = set(CITY_COORDS.keys()) - {'National'}  # Exclude National
        
        # Find cities that have ANY of the selected recommendations
        df_full = load_data()  # Use full dataset, not filtered
        cities_with_any_selected_rec = set()
        for rec in selected_recs:
            cities_with_rec = set(df_full[df_full['recommendation'] == rec]['location'].unique())
            cities_with_any_selected_rec.update(cities_with_rec)
        
        # Remove 'National' if it somehow got in there
        cities_with_any_selected_rec.discard('National')
        
        # Cities missing ALL selected recommendations
        missing_cities = all_cities - cities_with_any_selected_rec
        
        # Add red markers for cities missing the selected recommendations
        for city in missing_cities:
            if city in CITY_COORDS:
                lat, lon = CITY_COORDS[city]
                missing_recs = [RECOMMENDATIONS[r] for r in selected_recs]
                popup_text = f"<b>{city}</b><br><br>⚠️ <b>Missing:</b><br>"
                for rec in missing_recs:
                    popup_text += f"• {rec}<br>"
                
                folium.Marker(
                    [lat, lon],
                    popup=folium.Popup(html=f"<div style='max-height:200px; overflow-y:auto;'>{popup_text}</div>", max_width=300),
                    tooltip=f"{city} (Missing {len(selected_recs)} recommendations)",
                    icon=folium.Icon(color='red', icon='exclamation-sign')
                ).add_to(m)
    
    # Regular markers for cities with initiatives
    if not gap_mode:
        # Group by location to avoid duplicate markers
        
        for location, group in location_groups:
            if location in CITY_COORDS:
                lat, lon = CITY_COORDS[location]
                
                # Separate schools from other initiatives
                schools = group[group['program'].str.contains('School|skole', case=False, na=False)]
                other_initiatives = group[~group['program'].str.contains('School|skole', case=False, na=False)]
                
                # Main marker for non-school initiatives
                if not other_initiatives.empty:
                    popup_text = f"<b>{location}</b><br><br>"
                    for _, row in other_initiatives.iterrows():
                        rec_text = RECOMMENDATIONS[row['recommendation']]
                        popup_text += f"• <b>{row['program']}</b><br>"
                        popup_text += f"  {rec_text}<br>"
                        popup_text += f"  <i>{row['organization']}</i><br><br>"
                    
                    # Use color of first recommendation for the marker
                    color = REC_COLORS[other_initiatives.iloc[0]['recommendation']]
                    
                    folium.Marker(
                        [lat, lon],
                        popup=folium.Popup(html=f"<div style='max-height:200px; overflow-y:auto;'>{popup_text}</div>", max_width=300),
                        tooltip=f"{location} ({len(other_initiatives)} initiatives)",
                        icon=folium.Icon(color=color, icon='info-sign')
                    ).add_to(m)
                
                # School markers (if enabled)
                if show_schools and not schools.empty:
                    school_popup = f"<b>{location} - International Schools</b><br><br>"
                    for _, row in schools.iterrows():
                        school_popup += f"🏫 <b>{row['program']}</b><br>"
                        school_popup += f"   {row['organization']}<br><br>"
                    
                    folium.Marker(
                        [lat + 0.02, lon + 0.02],  # Slight offset to avoid overlap
                        popup=folium.Popup(html=f"<div style='max-height:200px; overflow-y:auto;'>{school_popup}</div>", max_width=300),
                        tooltip=f"{location} ({len(schools)} schools)",
                        icon=folium.Icon(color='blue', icon='home')
                    ).add_to(m)
    
    return m

def main():
    st.title("🇩🇰 Denmark International Talent Initiatives")
    st.write("Based on Copenhagen Capacity's 2025 Expat Survey Recommendations")
    
    # Load data
    df = load_data()
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Filter by recommendation
    st.sidebar.write("**Filter by Copenhagen Capacity Recommendations:**")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Select All Recs", key="select_all_recs"):
            st.session_state.selected_recs = list(RECOMMENDATIONS.keys())
    with col2:
        if st.button("Clear All Recs", key="clear_all_recs"):
            st.session_state.selected_recs = []
    
    selected_recs = st.sidebar.multiselect(
        "Choose recommendations:",
        options=list(RECOMMENDATIONS.keys()),
        format_func=lambda x: f"{x}: {RECOMMENDATIONS[x][:50]}...",
        default=st.session_state.get('selected_recs', list(RECOMMENDATIONS.keys())),
        key="rec_multiselect"
    )
    st.session_state.selected_recs = selected_recs
    
    # Filter by location
    st.sidebar.write("**Filter by Location:**")
    all_locations = sorted(df['location'].unique())
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Select All Cities", key="select_all_cities"):
            st.session_state.selected_locations = all_locations
    with col2:
        if st.button("Clear All Cities", key="clear_all_cities"):
            st.session_state.selected_locations = []
    
    selected_locations = st.sidebar.multiselect(
        "Choose locations:",
        options=all_locations,
        default=st.session_state.get('selected_locations', all_locations),
        key="location_multiselect"
    )
    st.session_state.selected_locations = selected_locations
    
    # Apply filters
    df_filtered = df[
        (df['recommendation'].isin(selected_recs)) & 
        (df['location'].isin(selected_locations))
    ]
    
    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Initiative Map")
        
        # Map controls
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            show_schools = st.checkbox("Show International Schools", value=True)
        with col_b:
            gap_mode = st.checkbox("Gap Mode (show missing)", value=False)
        with col_c:
            if gap_mode:
                st.write("🔍 Showing cities missing selected recommendations")
        
        if not df_filtered.empty or gap_mode:
            map_obj = create_map(df_filtered, show_schools, gap_mode, selected_recs)
            st_folium(map_obj, width=700, height=500)
        else:
            st.write("No initiatives match your current filters.")
    
    with col2:
        st.subheader("Coverage Dashboard")
        
        # Copenhagen Capacity recommendation summary
        st.write("**Copenhagen Capacity's 4 Official Areas:**")
        st.write("1. **Job Market Accessibility** (1a-1b)")
        st.write("2. **International Students** (2a-2b)")  
        st.write("3. **Inclusion & Belonging** (3a-3c)")
        st.write("4. **Spouses/Partners & Family** (4a-4b)")
        
        # Region coverage summary
        all_cities = [city for city in CITY_COORDS.keys() if city != 'National']
        cities_with_data = df['location'].nunique() - (1 if 'National' in df['location'].values else 0)
                        
        # Recommendation coverage analysis
        st.write("**Coverage by Recommendation:**")
        for rec_id in RECOMMENDATIONS.keys():
            cities_with_rec = df[df['recommendation'] == rec_id]['location'].nunique()
            if 'National' in df[df['recommendation'] == rec_id]['location'].values:
                cities_with_rec -= 1  # Don't count National in city count
                national_symbol = " 🇩🇰"
            else:
                national_symbol = ""
            
            st.write(f"{rec_id}: **{cities_with_rec}** cities{national_symbol}")
        
        # Special insights
        st.write("**Key Insights:**")
        
        # Find cities with spouse support
        spouse_cities = df[df['recommendation'] == '4a']['location'].unique()
        spouse_count = len([c for c in spouse_cities if c != 'National'])
        st.write(f"• **{spouse_count}** cities have spouse support")
        
        # International schools
        school_data = df[df['recommendation'] == '4b']
        school_cities = len(school_data['location'].unique())
        st.write(f"• **{school_cities}** cities have international schools")
        
        # Find comprehensive cities (covering all 4 main areas)
        city_coverage = df[df['location'] != 'National'].groupby('location')['recommendation'].apply(
            lambda x: len(set([r[0] for r in x]))  # Count main categories (1,2,3,4)
        )
        comprehensive_cities = city_coverage[city_coverage == 4].index.tolist()
        st.write(f"• **{len(comprehensive_cities)}** cities address all 4 areas")
        
        if comprehensive_cities:
            st.write("   🏆 " + ", ".join(comprehensive_cities))
        
        
        st.subheader("Legend")
        st.write("**Copenhagen Capacity Categories:**")
        category_names = {
            '1': 'Job Market Access',
            '2': 'International Students',
            '3': 'Inclusion & Belonging',
            '4': 'Spouses & Family'
        }
        category_colors = {'1': 'blue', '2': 'green', '3': 'red', '4': 'purple'}
        for cat, color in category_colors.items():
            if any(rec.startswith(cat) for rec in selected_recs):
                cat_name = category_names[cat]
                st.write(f"🔵 **Category {cat}:** {cat_name}")

        if show_schools:
            st.write("🏫 **Blue markers:** International Schools")

        if gap_mode:
            st.write("⚠️ **Red markers:** Missing selected recommendations")

   

# Page configuration

# Danish city coordinates lookup


CITY_COORDS = {
    'Copenhagen': [55.6761, 12.5683],
    'Aarhus': [56.1629, 10.2039],
    'Odense': [55.4038, 10.4024],
    
    'Kalundborg': [55.6794, 11.0888],
    'Kolding': [55.4904, 9.4719],
    'Aalborg': [57.0488, 9.9217],
    'Esbjerg': [55.4700, 8.4520],
    'Horsens': [55.8607, 9.8500],
    'Hellerup': [55.7267, 12.5700],
    'Frederiksberg': [55.6867, 12.5339],
    'Roskilde': [55.6415, 12.0803],
    'Hørsholm': [55.8817, 12.4983],
    'Næstved': [55.2297, 11.7603],
    'Sønderborg': [54.9089, 9.7927],
    'Billund': [55.7308, 9.1153],
    'Ikast': [56.1386, 9.1575],
    'Holbæk': [55.7167, 11.7167],
    'Viborg': [56.4533, 9.4017],
    'Maribo': [54.7719, 11.5008],
    'Nordhavn': [55.7061, 12.5914],
    'Vejle': [55.7058, 9.5378],
    'National': [56.2639, 9.5018]
}

# Copenhagen Capacity recommendation mapping (EXACTLY as they wrote it)
RECOMMENDATIONS = {
    '1a': "Job market accessibility - Targeted programs",
    '1b': "Job market accessibility - Job portals with relevant jobs", 
    '2a': "International students - Career services",
    '2b': "International students - Integration resources",
    '3a': "Inclusion and belonging - Onboarding programs",
    '3b': "Inclusion and belonging - More social events",
    '3c': "Inclusion and belonging - Encourage cultural engagement",
    '4a': "Spouses/partners & family - Job opportunities",
    '4b': "Spouses/partners & family - Inclusive education for children"
}

# Color mapping for Copenhagen Capacity's 4 main categories
REC_COLORS = {
    '1a': 'blue', '1b': 'lightblue',                       # Job market - blues
    '2a': 'green', '2b': 'lightgreen',                     # Students - greens  
    '3a': 'red', '3b': 'lightred', '3c': 'darkred',        # Inclusion - reds
    '4a': 'purple', '4b': 'pink'                           # Family - purples
}

@st.cache_data
def load_data():
    # Restructured data following Copenhagen Capacity's official 4 recommendations
    data = [
        
        {'location': 'National', 'recommendation': '1a', 'program': 'Workindenmark/EURES', 'organization': 'Government/EU partnership', 'status': 'Active'},
        {'location': 'National', 'recommendation': '3b', 'program': 'Welcome September', 'organization': 'Life in Denmark', 'status': 'Active'},
        {'location': 'National', 'recommendation': '2a', 'program': 'Young Professionals in Denmark', 'organization': 'Confederation of Danish Industry', 'status': 'Active'},
        {'location': 'National', 'recommendation': '2a', 'program': 'Student Job Portals', 'organization': 'Workindenmark', 'status': 'Active'},
        {'location': 'National', 'recommendation': '4a', 'program': 'SIRI Family Member Support', 'organization': 'Danish Agency for International Recruitment', 'status': 'Active'},
        {'location': 'National', 'recommendation': '4a', 'program': 'Relocare Spouse Job Search', 'organization': 'Private Relocation Services', 'status': 'Active'},
        
        
        {'location': 'Copenhagen', 'recommendation': '2a', 'program': 'Career Kick Start', 'organization': 'University of Copenhagen', 'status': 'Active'},
        {'location': 'Copenhagen', 'recommendation': '2a', 'program': 'Greater Copenhagen Career Program', 'organization': 'Copenhagen Capacity', 'status': 'Active'},
        {'location': 'Copenhagen', 'recommendation': '2a', 'program': 'Young Professionals in Denmark', 'organization': 'Confederation of Danish Industry', 'status': 'Active'},
        {'location': 'Copenhagen', 'recommendation': '2b', 'program': 'University Career Services', 'organization': 'Danish Universities', 'status': 'Active'},
        {'location': 'Copenhagen', 'recommendation': '2b', 'program': 'Company Thesis Collaboration', 'organization': 'Universities & Employers', 'status': 'Active'},
        {'location': 'Copenhagen', 'recommendation': '4b', 'program': 'European School Copenhagen', 'organization': 'Public School', 'status': 'Active'},
        {'location': 'Copenhagen', 'recommendation': '4b', 'program': 'International Montessori School', 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Copenhagen', 'recommendation': '4b', 'program': 'Sankt Petri Skole', 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Copenhagen', 'recommendation': '4b', 'program': 'Viking International School', 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Copenhagen', 'recommendation': '4b', 'program': 'Waldorf International School', 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Copenhagen', 'recommendation': '4a', 'program': 'Copenhagen Career Program for Spouses', 'organization': 'Municipality', 'status': 'Active'},
        
        
        {'location': 'Aarhus', 'recommendation': '1a', 'program': 'International Community Aarhus', 'organization': 'Erhverv Aarhus', 'status': 'Active'},
        {'location': 'Aarhus', 'recommendation': '1a', 'program': 'International Employment Unit', 'organization': 'Jobcenter Aarhus', 'status': 'Active'},
        {'location': 'Aarhus', 'recommendation': '1a', 'program': 'Work & Study Programme (Computer Science)', 'organization': 'Aarhus University', 'status': 'Pilot (2025-2027)'},
        {'location': 'Aarhus', 'recommendation': '1a', 'program': 'Employer Outreach & Awareness Campaigns', 'organization': 'Erhverv Aarhus', 'status': 'Active'},
        {'location': 'Aarhus', 'recommendation': '2a', 'program': 'Talent to a Green Denmark', 'organization': 'Studenterhus Aarhus', 'status': 'Active (2023-2025)'},
        {'location': 'Aarhus', 'recommendation': '2b', 'program': 'University-Business Talent Partnerships', 'organization': 'Aarhus University', 'status': 'Active'},
        {'location': 'Aarhus', 'recommendation': '2a', 'program': 'AU Student Job Fair', 'organization': 'Aarhus University', 'status': 'Active'},
        {'location': 'Aarhus', 'recommendation': '3a', 'program': 'Aarhus City Welcome', 'organization': 'Municipality', 'status': 'Active'},
        {'location': 'Aarhus', 'recommendation': '3a', 'program': 'International Employment Unit Onboarding', 'organization': 'Jobcenter Aarhus', 'status': 'Active'},
        {'location': 'Aarhus', 'recommendation': '4a', 'program': 'AU Expat Partner Programme', 'organization': 'Aarhus University', 'status': 'Active'},
        {'location': 'Aarhus', 'recommendation': '4a', 'program': 'International Employment Unit Partner Support', 'organization': 'Jobcenter Aarhus', 'status': 'Active'},
        {'location': 'Aarhus', 'recommendation': '4b', 'program': 'Aarhus International School', 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Aarhus', 'recommendation': '3b', 'program': 'Aarhus City Welcome Events', 'organization': 'Municipality', 'status': 'Active'},
        {'location': 'Aarhus', 'recommendation': '3b', 'program': 'International Community Events', 'organization': 'Erhverv Aarhus', 'status': 'Active'},
        {'location': 'Aarhus', 'recommendation': '3b', 'program': 'Studenterhus Aarhus Social Programs', 'organization': 'Studenterhus Aarhus', 'status': 'Active'},
        {'location': 'Aarhus', 'recommendation': '3c', 'program': 'Sports Integration Initiatives', 'organization': 'Municipality & Sports Clubs', 'status': 'Active'},
        {'location': 'Aarhus', 'recommendation': '3c', 'program': 'Cultural Clubs Integration', 'organization': 'Municipality & NGOs', 'status': 'Active'},
        
        
        {'location': 'Odense', 'recommendation': '3a', 'program': 'International Community Odense', 'organization': 'City of Odense', 'status': 'Active'},
        {'location': 'Odense', 'recommendation': '1b', 'program': 'IT and Academic Job Fair', 'organization': 'Jobcenter Odense', 'status': 'Active'},
        {'location': 'Odense', 'recommendation': '2a', 'program': 'SDU Career Services', 'organization': 'University of Southern Denmark', 'status': 'Active'},
        {'location': 'Odense', 'recommendation': '4b', 'program': 'Henriette Hørlücks Skole', 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Odense', 'recommendation': '4a', 'program': 'Host Programme', 'organization': 'Odense Kommune', 'status': 'Active'},
        
        
        {'location': 'Aalborg', 'recommendation': '1a', 'program': 'International House North Denmark', 'organization': 'IHND (Municipal/Regional)', 'status': 'Active'},
        {'location': 'Aalborg', 'recommendation': '3a', 'program': 'IHND Onboarding Services', 'organization': 'IHND', 'status': 'Active'},
        {'location': 'Aalborg', 'recommendation': '4a', 'program': 'IHND Spouse Support', 'organization': 'IHND', 'status': 'Active'},
        {'location': 'Aalborg', 'recommendation': '2b', 'program': 'University/Business Network Collaboration', 'organization': 'Invest in Aalborg', 'status': 'Active'},
        {'location': 'Aalborg', 'recommendation': '3b', 'program': 'Welcome September', 'organization': 'Local Municipality', 'status': 'Active'},
        {'location': 'Aalborg', 'recommendation': '2a', 'program': 'University Career Centre', 'organization': 'Aalborg University', 'status': 'Active'},
        {'location': 'Aalborg', 'recommendation': '2b', 'program': 'Internship Programmes', 'organization': 'Aalborg University', 'status': 'Active'},
        {'location': 'Aalborg', 'recommendation': '4b', 'program': 'Skipper Clement Skolen', 'organization': 'Private School', 'status': 'Active'},
        
        
        {'location': 'Esbjerg', 'recommendation': '1a', 'program': 'Jobcenter & EURES Collaboration', 'organization': 'Local Jobcenter', 'status': 'Active'},
        {'location': 'Esbjerg', 'recommendation': '2b', 'program': 'University-Company Integration', 'organization': 'University of Southern Denmark', 'status': 'Active'},
        {'location': 'Esbjerg', 'recommendation': '3b', 'program': 'Welcome September', 'organization': 'Local Municipality', 'status': 'Active'},
        {'location': 'Esbjerg', 'recommendation': '4b', 'program': 'Esbjerg International School', 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Esbjerg', 'recommendation': '4a', 'program': 'Settling-in Coordinator', 'organization': 'Municipality', 'status': 'Active'},
        
        
        {'location': 'Maribo', 'recommendation': '3b', 'program': 'International Welcome Fund', 'organization': 'Lolland Kommune', 'status': 'Active'},
        {'location': 'Maribo', 'recommendation': '3a', 'program': 'Healthcare Professionals Program', 'organization': 'Lolland Kommune', 'status': 'Active'},
        {'location': 'Maribo', 'recommendation': '4b', 'program': 'Lolland International School', 'organization': 'Public School', 'status': 'Active'},
        {'location': 'Kalundborg', 'recommendation': '1a', 'program': 'Virksomhedsforum', 'organization': 'Kalundborg Jobcenter', 'status': 'Active'},
        {'location': 'Kalundborg', 'recommendation': '3b', 'program': 'Liv i Kalundborg', 'organization': 'Business Council', 'status': 'Active'},
        {'location': 'Kolding', 'recommendation': '1a', 'program': 'International Policy Framework', 'organization': 'Kolding Kommune', 'status': 'Active'},
        {'location': 'Kolding', 'recommendation': '3a', 'program': 'International Policy Framework', 'organization': 'Kolding Kommune', 'status': 'Active'},
        
        
        {'location': 'Hellerup', 'recommendation': '4b', 'program': 'Bernadotteskolen', 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Hellerup', 'recommendation': '4b', 'program': 'International School of Hellerup', 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Hellerup', 'recommendation': '4b', 'program': 'Rygaards Skole', 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Frederiksberg', 'recommendation': '4b', 'program': 'Prins Henriks skole', 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Frederiksberg', 'recommendation': '1a', 'program': 'Inclusive Municipal Hiring', 'organization': 'Municipality', 'status': 'Active'},
        {'location': 'Frederiksberg', 'recommendation': '3b', 'program': 'CPH STAGE Festival', 'organization': 'Event Organizations', 'status': 'Active'},
        {'location': 'Frederiksberg', 'recommendation': '2a', 'program': 'Career Kick Start (coverage)', 'organization': 'University of Copenhagen', 'status': 'Active'},
        {'location': 'Roskilde', 'recommendation': '4b', 'program': "Skt. Josef's International School", 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Roskilde', 'recommendation': '2a', 'program': 'Roskilde University Career Services', 'organization': 'Roskilde University', 'status': 'Active'},
        {'location': 'Sønderborg', 'recommendation': '4b', 'program': 'Sønderborg International School', 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Sønderborg', 'recommendation': '4a', 'program': 'SDU Spouse Support', 'organization': 'University of Southern Denmark', 'status': 'Active'},
        {'location': 'Billund', 'recommendation': '4b', 'program': 'International School of Billund', 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Billund', 'recommendation': '4a', 'program': 'LEGO Family Programme', 'organization': 'LEGO Group', 'status': 'Active'},
        {'location': 'Billund', 'recommendation': '3a', 'program': 'LEGO Family Onboarding', 'organization': 'LEGO Group', 'status': 'Active'},
        {'location': 'Ikast', 'recommendation': '4b', 'program': 'International School Ikast-Brande', 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Viborg', 'recommendation': '4b', 'program': 'Viborg private Realskole', 'organization': 'Private School', 'status': 'Active'},
        {'location': 'Viborg', 'recommendation': '2a', 'program': 'VIA University Partnerships', 'organization': 'VIA University', 'status': 'Active'},
        {'location': 'Horsens', 'recommendation': '4a', 'program': 'International House Horsens Spouse Support', 'organization': 'International House Horsens', 'status': 'Active'},
        {'location': 'Horsens', 'recommendation': '2a', 'program': 'VIA University College Career Services', 'organization': 'VIA University College', 'status': 'Active'},
        {'location': 'Kolding', 'recommendation': '2a', 'program': 'SDU Career Services', 'organization': 'University of Southern Denmark', 'status': 'Active'},
        {'location': 'Vejle', 'recommendation': '4a', 'program': 'Spousehouse Vejle', 'organization': 'Facebook Community Group', 'status': 'Active'},
    ]
    return pd.DataFrame(data)

def create_map(df_filtered, show_schools=True, gap_mode=False, selected_recs=None):
    """Create folium map with filtered data"""
    m = folium.Map(location=[56.0, 10.0], zoom_start=7)
    
    if gap_mode and selected_recs:
        # Gap mode: show cities that DON'T have selected recommendations
        all_cities = set(CITY_COORDS.keys()) - {'National'}  # Exclude National
        
        # Find cities that have ANY of the selected recommendations
        df_full = load_data()  # Use full dataset, not filtered
        cities_with_any_selected_rec = set()
        for rec in selected_recs:
            cities_with_rec = set(df_full[df_full['recommendation'] == rec]['location'].unique())
            cities_with_any_selected_rec.update(cities_with_rec)
        
        # Remove 'National' if it somehow got in there
        cities_with_any_selected_rec.discard('National')
        
        # Cities missing ALL selected recommendations
        missing_cities = all_cities - cities_with_any_selected_rec
        
        # Add red markers for cities missing the selected recommendations
        for city in missing_cities:
            if city in CITY_COORDS:
                lat, lon = CITY_COORDS[city]
                missing_recs = [RECOMMENDATIONS[r] for r in selected_recs]
                popup_text = f"<b>{city}</b><br><br>⚠️ <b>Missing:</b><br>"
                for rec in missing_recs:
                    popup_text += f"• {rec}<br>"
                
                folium.Marker(
                    [lat, lon],
                    popup=folium.Popup(html=f"<div style='max-height:200px; overflow-y:auto;'>{popup_text}</div>", max_width=300),
                    tooltip=f"{city} (Missing {len(selected_recs)} recommendations)",
                    icon=folium.Icon(color='red', icon='exclamation-sign')
                ).add_to(m)
    
    # Regular markers for cities with initiatives
    if not gap_mode:
        # Group by location to avoid duplicate markers
        location_groups = df_filtered.groupby('location')
        
        for location, group in location_groups:
            if location in CITY_COORDS:
                lat, lon = CITY_COORDS[location]
                
                # Separate schools from other initiatives
                schools = group[group['program'].str.contains('School|skole', case=False, na=False)]
                other_initiatives = group[~group['program'].str.contains('School|skole', case=False, na=False)]
                
                # Main marker for non-school initiatives
                if not other_initiatives.empty:
                    popup_text = f"<b>{location}</b><br><br>"
                    for _, row in other_initiatives.iterrows():
                        rec_text = RECOMMENDATIONS[row['recommendation']]
                        popup_text += f"• <b>{row['program']}</b><br>"
                        popup_text += f"  {rec_text}<br>"
                        popup_text += f"  <i>{row['organization']}</i><br><br>"
                    
                    # Use color of first recommendation for the marker
                    color = REC_COLORS[other_initiatives.iloc[0]['recommendation']]
                    
                    folium.Marker(
                        [lat, lon],
                        popup=folium.Popup(html=f"<div style='max-height:200px; overflow-y:auto;'>{popup_text}</div>", max_width=300),
                        tooltip=f"{location} ({len(other_initiatives)} initiatives)",
                        icon=folium.Icon(color=color, icon='info-sign')
                    ).add_to(m)
                
                # School markers (if enabled)
                if show_schools and not schools.empty:
                    school_popup = f"<b>{location} - International Schools</b><br><br>"
                    for _, row in schools.iterrows():
                        school_popup += f"🏫 <b>{row['program']}</b><br>"
                        school_popup += f"   {row['organization']}<br><br>"
                    
                    folium.Marker(
                        [lat + 0.02, lon + 0.02],  # Slight offset to avoid overlap
                        popup=folium.Popup(html=f"<div style='max-height:200px; overflow-y:auto;'>{school_popup}</div>", max_width=300),
                        tooltip=f"{location} ({len(schools)} schools)",
                        icon=folium.Icon(color='blue', icon='home')
                    ).add_to(m)
    
    return m

def main():
    st.title("🇩🇰 Denmark International Talent Initiatives")
    st.write("Based on Copenhagen Capacity's 2025 Expat Survey Recommendations")
    
    # Load data
    df = load_data()
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Filter by recommendation
    st.sidebar.write("**Filter by Copenhagen Capacity Recommendations:**")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Select All Recs", key="select_all_recs"):
            st.session_state.selected_recs = list(RECOMMENDATIONS.keys())
    with col2:
        if st.button("Clear All Recs", key="clear_all_recs"):
            st.session_state.selected_recs = []
    
    selected_recs = st.sidebar.multiselect(
        "Choose recommendations:",
        options=list(RECOMMENDATIONS.keys()),
        format_func=lambda x: f"{x}: {RECOMMENDATIONS[x][:50]}...",
        default=st.session_state.get('selected_recs', list(RECOMMENDATIONS.keys())),
        key="rec_multiselect"
    )
    st.session_state.selected_recs = selected_recs
    
    # Filter by location
    st.sidebar.write("**Filter by Location:**")
    all_locations = sorted(df['location'].unique())
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Select All Cities", key="select_all_cities"):
            st.session_state.selected_locations = all_locations
    with col2:
        if st.button("Clear All Cities", key="clear_all_cities"):
            st.session_state.selected_locations = []
    
    selected_locations = st.sidebar.multiselect(
        "Choose locations:",
        options=all_locations,
        default=st.session_state.get('selected_locations', all_locations),
        key="location_multiselect"
    )
    st.session_state.selected_locations = selected_locations
    
    # Apply filters
    df_filtered = df[
        (df['recommendation'].isin(selected_recs)) & 
        (df['location'].isin(selected_locations))
    ]
    
    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Initiative Map")
        
        # Map controls
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            show_schools = st.checkbox("Show International Schools", value=True)
        with col_b:
            gap_mode = st.checkbox("Gap Mode (show missing)", value=False)
        with col_c:
            if gap_mode:
                st.write("🔍 Showing cities missing selected recommendations")
        
        if not df_filtered.empty or gap_mode:
            map_obj = create_map(df_filtered, show_schools, gap_mode, selected_recs)
            st_folium(map_obj, width=700, height=500)
        else:
            st.write("No initiatives match your current filters.")
    
    with col2:
        st.subheader("Coverage Dashboard")
        
        # Copenhagen Capacity recommendation summary
        st.write("**Copenhagen Capacity's 4 Official Areas:**")
        st.write("1. **Job Market Accessibility** (1a-1b)")
        st.write("2. **International Students** (2a-2b)")  
        st.write("3. **Inclusion & Belonging** (3a-3c)")
        st.write("4. **Spouses/Partners & Family** (4a-4b)")
        
        # Region coverage summary
        all_cities = [city for city in CITY_COORDS.keys() if city != 'National']
        cities_with_data = df['location'].nunique() - (1 if 'National' in df['location'].values else 0)
                        
        # Recommendation coverage analysis
        st.write("**Coverage by Recommendation:**")
        for rec_id in RECOMMENDATIONS.keys():
            cities_with_rec = df[df['recommendation'] == rec_id]['location'].nunique()
            if 'National' in df[df['recommendation'] == rec_id]['location'].values:
                cities_with_rec -= 1  # Don't count National in city count
                national_symbol = " 🇩🇰"
            else:
                national_symbol = ""
            
            st.write(f"{rec_id}: **{cities_with_rec}** cities{national_symbol}")
        
        # Special insights
        st.write("**Key Insights:**")
        
        # Find cities with spouse support
        spouse_cities = df[df['recommendation'] == '4a']['location'].unique()
        spouse_count = len([c for c in spouse_cities if c != 'National'])
        st.write(f"• **{spouse_count}** cities have spouse support")
        
        # International schools
        school_data = df[df['recommendation'] == '4b']
        school_cities = len(school_data['location'].unique())
        st.write(f"• **{school_cities}** cities have international schools")
        
        # Find comprehensive cities (covering all 4 main areas)
        city_coverage = df[df['location'] != 'National'].groupby('location')['recommendation'].apply(
            lambda x: len(set([r[0] for r in x]))  # Count main categories (1,2,3,4)
        )
        comprehensive_cities = city_coverage[city_coverage == 4].index.tolist()
        st.write(f"• **{len(comprehensive_cities)}** cities address all 4 areas")
        
        if comprehensive_cities:
            st.write("   🏆 " + ", ".join(comprehensive_cities))
        
        
        st.subheader("Legend")
        st.write("**Copenhagen Capacity Categories:**")
        category_names = {
            '1': 'Job Market Access',
            '2': 'International Students',
            '3': 'Inclusion & Belonging',
            '4': 'Spouses & Family'
        }
        category_colors = {'1': 'blue', '2': 'green', '3': 'red', '4': 'purple'}
        for cat, color in category_colors.items():
            if any(rec.startswith(cat) for rec in selected_recs):
                cat_name = category_names[cat]
                st.write(f"🔵 **Category {cat}:** {cat_name}")

        if show_schools:
            st.write("🏫 **Blue markers:** International Schools")

        if gap_mode:
            st.write("⚠️ **Red markers:** Missing selected recommendations")

   



    



    st.subheader("Initiative Details")

    if not df_filtered.empty:
        df_display = df_filtered.copy()
        df_display['Recommendation Text'] = df_display['recommendation'].map(RECOMMENDATIONS)

        def generate_html_table(df, hyperlinks):
            rows = []
            header = "<tr><th>Location</th><th>Rec ID</th><th>Recommendation</th><th>Program</th><th>Organization</th><th>Status</th></tr>"
            rows.append(header)

            for _, row in df.iterrows():
                program = row['program']
                link = hyperlink_data.get(program)
                program_display = f'<a href="{link}" target="_blank">{program}</a>' if link else program

                html_row = (
                    f"<tr>"
                    f"<td>{row['location']}</td>"
                    f"<td>{row['recommendation']}</td>"
                    f"<td>{RECOMMENDATIONS[row['recommendation']]}</td>"
                    f"<td>{program_display}</td>"
                    f"<td>{row['organization']}</td>"
                    f"<td>{row['status']}</td>"
                    f"</tr>"
                )
                rows.append(html_row)

            html_table = "<table style='width:100%; border-collapse: collapse;' border='1'>" + "".join(rows) + "</table>"
            return html_table

        html_table = generate_html_table(df_display, hyperlink_data)
        st.markdown(html_table, unsafe_allow_html=True)

    else:
        st.write("No data to display with current filters.")

    # Quick stats
    st.subheader("Quick Stats")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Initiatives", len(df_filtered))
    with col2:
        st.metric("Cities Covered", df_filtered['location'].nunique())
    with col3:
        st.metric("Recommendation Types", df_filtered['recommendation'].nunique())
    with col4:
        international_schools = len(df_filtered[df_filtered['recommendation'] == '4b'])
        st.metric("International Schools", international_schools)

if __name__ == "__main__":
    main()
