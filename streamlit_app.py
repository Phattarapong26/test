
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
    
    # Enhanced Custom CSS
    st.markdown("""
    <style>
    /* Modal Styling */
    .modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
        animation: fadeIn 0.3s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .modal-content {
        background-color: white;
        border-radius: 10px;
        padding: 30px;
        width: 90%;
        max-width: 500px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        position: relative;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from { transform: translateY(-50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .modal-close {
        position: absolute;
        top: 15px;
        right: 15px;
        cursor: pointer;
        font-size: 24px;
        color: #888;
        transition: color 0.2s;
    }
    
    .modal-close:hover {
        color: #ff4136;
    }
    
    /* Content Card Styling */
    .content-card {
        border: 1px solid #e1e1e1;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        transition: box-shadow 0.3s ease;
    }
    
    .content-card:hover {
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stButton>button {
        width: 100%;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'data' not in st.session_state:
        st.session_state.data = pd.DataFrame(sample_data)
    
    # Modal state initialization
    modal_states = [
        'show_add_modal', 'show_edit_modal', 'show_delete_modal', 
        'edit_index', 'delete_index'
    ]
    for state in modal_states:
        if state not in st.session_state:
            st.session_state[state] = None if 'index' in state else False
    
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
            st.session_state.show_add_modal = True
    
    # Menu
    if st.session_state.get('show_menu', False):
        st.sidebar.title("Menu")
        st.sidebar.button("Option 1")
        st.sidebar.button("Option 2")
        st.sidebar.button("Option 3")
    
    # Add Content Modal
    if st.session_state.show_add_modal:
        st.markdown('<div class="modal">', unsafe_allow_html=True)
        st.markdown('<div class="modal-content">', unsafe_allow_html=True)
        st.markdown('<div class="modal-close" onclick="this.closest(\'.modal\').style.display=\'none\'">×</div>', unsafe_allow_html=True)
        
        with st.form("add_content_form", clear_on_submit=True):
            st.subheader("Add New Content")
            new_image = st.text_input("Image URL")
            new_description = st.text_area("Description")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Add"):
                    if new_image and new_description:
                        new_data = pd.DataFrame({
                            'image': [new_image],
                            'description': [new_description],
                            'views': [0]
                        })
                        st.session_state.data = pd.concat([st.session_state.data, new_data], ignore_index=True)
                        st.session_state.show_add_modal = False
            with col2:
                if st.form_submit_button("Cancel"):
                    st.session_state.show_add_modal = False
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display content grid
    cols = st.columns(3)
    for index, row in st.session_state.data.iterrows():
        with cols[index % 3]:
            with st.container():
                st.markdown(f"<div class='content-card'>", unsafe_allow_html=True)
                st.image(row['image'], use_column_width=True)
                st.markdown(f"<p>{row['description']}</p>", unsafe_allow_html=True)
                st.markdown(f"view {row['views']:,}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("DELETE", key=f"delete_{index}"):
                        st.session_state.show_delete_modal = True
                        st.session_state.delete_index = index
                with col2:
                    if st.button("EDIT", key=f"edit_{index}"):
                        st.session_state.show_edit_modal = True
                        st.session_state.edit_index = index
                
                st.markdown("</div>", unsafe_allow_html=True)
    
    # Edit Modal
    if st.session_state.show_edit_modal and st.session_state.edit_index is not None:
        st.markdown('<div class="modal">', unsafe_allow_html=True)
        st.markdown('<div class="modal-content">', unsafe_allow_html=True)
        st.markdown('<div class="modal-close" onclick="this.closest(\'.modal\').style.display=\'none\'">×</div>', unsafe_allow_html=True)
        
        with st.form(f"edit_form", clear_on_submit=True):
            st.subheader("Edit Content")
            index = st.session_state.edit_index
            
            edited_image = st.text_input("Image URL", value=st.session_state.data.loc[index, 'image'])
            edited_description = st.text_area("Description", value=st.session_state.data.loc[index, 'description'])
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Save"):
                    st.session_state.data.loc[index, 'image'] = edited_image
                    st.session_state.data.loc[index, 'description'] = edited_description
                    st.session_state.show_edit_modal = False
                    st.session_state.edit_index = None
            with col2:
                if st.form_submit_button("Cancel"):
                    st.session_state.show_edit_modal = False
                    st.session_state.edit_index = None
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Delete Modal
    if st.session_state.show_delete_modal and st.session_state.delete_index is not None:
        st.markdown('<div class="modal">', unsafe_allow_html=True)
        st.markdown('<div class="modal-content">', unsafe_allow_html=True)
        st.markdown('<div class="modal-close" onclick="this.closest(\'.modal\').style.display=\'none\'">×</div>', unsafe_allow_html=True)
        
        with st.form(f"delete_form"):
            st.subheader("Delete Content")
            st.write("Are you sure you want to delete this content?")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Delete"):
                    st.session_state.data = st.session_state.data.drop(st.session_state.delete_index)
                    st.session_state.show_delete_modal = False
                    st.session_state.delete_index = None
            with col2:
                if st.form_submit_button("Cancel"):
                    st.session_state.show_delete_modal = False
                    st.session_state.delete_index = None
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
