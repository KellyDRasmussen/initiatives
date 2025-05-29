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

# Copenhagen Capacity recommendation mapping 
RECOMMENDATIONS = {
    '1a': "Job market accessibility - Targeted programs",
    '1b': "Job market accessibility - Job portals with relevant jobs", 
    '2a': "International students - Career services",
    '2b': "International students - Integration resources",
    '3': "Inclusion and belonging",
    #'3a': "Inclusion and belonging - Onboarding programs",
    #'3b': "Inclusion and belonging - More social events",
    #'3c': "Inclusion and belonging - Encourage cultural engagement",
    '4a': "Spouses/partners & family - Job opportunities",
    '4b': "Spouses/partners & family - Inclusive education for children"
}

# Color mapping for Copenhagen Capacity's 4 main categories
REC_COLORS = {
    '1a': 'blue', '1b': 'lightblue',
    '2a': 'darkgreen', '2b': 'lightgreen',
    '3': 'orange', 
    '4a': 'purple', '4b': 'pink'
}



@st.cache_data
def load_data():
    return pd.read_csv("initiatives.csv"), pd.read_csv("hyperlinks.csv")


df, hyperlinks_df = load_data()
hyperlink_data = dict(zip(hyperlinks_df["program"], hyperlinks_df["url"]))

    
def create_map(df_filtered, show_schools=True, gap_mode=False, selected_recs=None):
    """Create folium map with filtered data"""
    
    # Font Awesome icon mapping by recommendation
    ICON_MAP = {
        '1a': 'briefcase',
        '1b': 'search',
        '2a': 'graduation-cap',
        '2b': 'language',
        '3':  'heart',
        '4a': 'home',
        '4b': 'school'
    }

    m = folium.Map(location=[56.0, 10.0], zoom_start=7)
    
    if gap_mode and selected_recs:
        all_cities = set(CITY_COORDS.keys()) - {'National'}
        df_full, _ = load_data()

        cities_with_any_selected_rec = set()
        for rec in selected_recs:
            cities_with_rec = set(df_full[df_full['recommendation'] == rec]['location'].unique())
            cities_with_any_selected_rec.update(cities_with_rec)

        cities_with_any_selected_rec.discard('National')
        missing_cities = all_cities - cities_with_any_selected_rec

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

    if not gap_mode:
        location_groups = df_filtered.groupby('location')

        for location, group in location_groups:
            if location in CITY_COORDS:
                lat, lon = CITY_COORDS[location]

                schools = group[group['program'].str.contains('School|skole', case=False, na=False)]
                other_initiatives = group[~group['program'].str.contains('School|skole', case=False, na=False)]

                if not other_initiatives.empty:
                    popup_text = f"<b>{location}</b><br><br>"
                    for _, row in other_initiatives.iterrows():
                        rec_text = RECOMMENDATIONS[row['recommendation']]
                        popup_text += f"• <b>{row['program']}</b><br>"
                        popup_text += f"  {rec_text}<br>"
                        popup_text += f"  <i>{row['organization']}</i><br><br>"

                    rec_id = other_initiatives.iloc[0]['recommendation']
                    color = REC_COLORS.get(rec_id, 'gray')
                    icon_name = ICON_MAP.get(rec_id, 'info-sign')

                    folium.Marker(
                        [lat, lon],
                        popup=folium.Popup(html=f"<div style='max-height:200px; overflow-y:auto;'>{popup_text}</div>", max_width=300),
                        tooltip=f"{location} ({len(other_initiatives)} initiatives)",
                        icon=folium.Icon(color=color, icon=icon_name, prefix='fa')
                    ).add_to(m)

                if show_schools and not schools.empty:
                    school_popup = f"<b>{location} - International Schools</b><br><br>"
                    for _, row in schools.iterrows():
                        school_popup += f"🏫 <b>{row['program']}</b><br>"
                        school_popup += f"   {row['organization']}<br><br>"

                    folium.Marker(
                        [lat + 0.02, lon + 0.02],
                        popup=folium.Popup(html=f"<div style='max-height:200px; overflow-y:auto;'>{school_popup}</div>", max_width=300),
                        tooltip=f"{location} ({len(schools)} schools)",
                        icon=folium.Icon(color='blue', icon='home')
                    ).add_to(m)

    return m


def main():
    st.title("🇩🇰 Denmark International Talent Initiatives")
    st.write("Based on Copenhagen Capacity's 2025 Expat Survey Recommendations")
    
    # Load data
    df, hyperlinks_df = load_data()

    
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
        st.write("3. **Inclusion & Belonging**")
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
                st.write(f" **Category {cat}:** {cat_name}")

        if show_schools:
            st.write("🏫 International Schools")

        if gap_mode:
            st.write("⚠️  Missing selected recommendations")

   



    



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
