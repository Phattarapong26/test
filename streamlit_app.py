
import streamlit as st
import pandas as pd

# Sample data for demonstration
sample_data = {
    'image': [
        'https://example.com/image1.jpg',
        'https://example.com/image2.jpg',
        'https://example.com/image3.jpg',
        'https://example.com/image4.jpg',
        'https://example.com/image5.jpg',
        'https://example.com/image6.jpg'
    ],
    'description': [
        'เลนส์ทรงกลมที่มีสไตล์ดูเป็นทางการ เหมาะสำหรับผู้ที่ชอบความคลาสสิก',
        'สายตาสั้น และ สายตายาวในเลนส์เดียวกัน สามารถมองได้',
        'Case Study 04 : The perfection result of compound simple adaptation',
        'เลนส์ทรงกลมที่มีสไตล์ดูเป็นทางการ เหมาะสำหรับผู้ที่ชอบความคลาสสิก',
        'สายตาสั้น และ สายตายาวในเลนส์เดียวกัน สามารถมองได้',
        'Case Study 04 : The perfection result of compound simple adaptation'
    ],
    'views': [15000, 16000, 19000, 15000, 16000, 18000]
}

def main():
    st.set_page_config(layout="wide", page_title="Contents Management")
    
    # Custom CSS
    st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
    }
    .stTextInput>div>div>input {
        background-color: #f0f2f6;
    }
    .content-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .content-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
    }
    .content-description {
        height: 60px;
        overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.title("CONTENTS MANAGEMENT")
    
    # Top bar
    col1, col2, col3 = st.columns([1,2,1])
    with col1:
        if st.button("MENU"):
            st.session_state.show_menu = not st.session_state.get('show_menu', False)
    with col2:
        st.text_input("Search", placeholder="Search content")
    with col3:
        if st.button("+ CONTENT"):
            st.session_state.show_add_content = True
    
    # Menu
    if st.session_state.get('show_menu', False):
        st.sidebar.title("Menu")
        st.sidebar.button("Option 1")
        st.sidebar.button("Option 2")
        st.sidebar.button("Option 3")
    
    # Add Content Form
    if st.session_state.get('show_add_content', False):
        with st.form("add_content_form"):
            st.subheader("Add New Content")
            new_image = st.text_input("Image URL")
            new_description = st.text_area("Description")
            submitted = st.form_submit_button("Add Content")
            if submitted:
                new_data = pd.DataFrame({
                    'image': [new_image],
                    'description': [new_description],
                    'views': [0]
                })
                st.session_state.data = pd.concat([st.session_state.data, new_data], ignore_index=True)
                st.session_state.show_add_content = False
                st.experimental_rerun()
    
    # Initialize session state for data
    if 'data' not in st.session_state:
        st.session_state.data = pd.DataFrame(sample_data)
    
    # Display content grid
    cols = st.columns(3)
    for index, row in st.session_state.data.iterrows():
        with cols[index % 3]:
            with st.container():
                st.markdown(f"<div class='content-card'>", unsafe_allow_html=True)
                st.image(row['image'], use_column_width=True, output_format="JPEG")
                st.markdown(f"<p class='content-description'>{row['description']}</p>", unsafe_allow_html=True)
                st.markdown(f"view {row['views']:,}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("DELETE", key=f"delete_{index}"):
                        st.session_state.data = st.session_state.data.drop(index)
                        st.experimental_rerun()
                with col2:
                    if st.button("EDIT", key=f"edit_{index}"):
                        st.session_state.edit_index = index
                st.markdown("</div>", unsafe_allow_html=True)
    
    # Edit form
    if 'edit_index' in st.session_state:
        index = st.session_state.edit_index
        with st.form(f"edit_form_{index}"):
            st.subheader("Edit Content")
            edited_image = st.text_input("Image URL", value=st.session_state.data.loc[index, 'image'])
            edited_description = st.text_area("Description", value=st.session_state.data.loc[index, 'description'])
            submitted = st.form_submit_button("Save Changes")
            if submitted:
                st.session_state.data.loc[index, 'image'] = edited_image
                st.session_state.data.loc[index, 'description'] = edited_description
                del st.session_state.edit_index
                st.experimental_rerun()

if __name__ == "__main__":
    main()
