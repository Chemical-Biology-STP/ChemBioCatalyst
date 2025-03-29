import json
import os
import streamlit as st

# Load the menu configuration from the JSON file
with open('menu_config.json', 'r') as f:
    menu_config = json.load(f)

# Dynamically create st.Page definitions
pages = {}
for menu in menu_config:
    if 'pages' in menu:
        for page in menu['pages']:
            var_name = page['display'].lower().replace(' ', '_')
            if page.get('icon'):
                pages[var_name] = st.Page(page['file_path'], title=page['display'], icon=page['icon'])
            else:
                pages[var_name] = st.Page(page['file_path'], title=page['display'])
    else:
        var_name = menu['folder']
        page = menu['page']
        if page.get('icon'):
            pages[var_name] = st.Page(page['file_path'], title=menu['display'], icon=page['icon'])
        else:
            pages[var_name] = st.Page(page['file_path'], title=menu['display'])

# Build navigation sidebar
with st.sidebar:
    st.header('Navigation')
    category = st.selectbox('Select a category', [m['display'] for m in menu_config])
    current_menu = next((m for m in menu_config if m['display'] == category), None)
    if current_menu:
        if 'pages' in current_menu:
            option = st.selectbox('Select an option', [p['display'] for p in current_menu['pages']])
            var_name = option.lower().replace(' ', '_')
            current_page = pages[var_name]
        else:
            var_name = current_menu['folder']
            current_page = pages[var_name]

pg = st.navigation([current_page])
pg.run()