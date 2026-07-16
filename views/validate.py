import streamlit as st
import db
import validators
import auth
from styling import apply_custom_css

def show_validate():
    apply_custom_css()
    
    st.markdown('<h2 style="margin-top:0;">🔍 Verify KYC Documents</h2>', unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b;'>Instantly validate format, structure, and integrity checks for PAN and Aadhaar.</p>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["💳 PAN Card Verification", "🆔 Aadhaar Card Verification"])
    
    with tab1:
        st.markdown('<div class="kyc-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='margin-top: 0;'>Validate PAN (Permanent Account Number)</h4>", unsafe_allow_html=True)
        
        pan_input = st.text_input("Enter PAN Number", placeholder="e.g. ABCDE1234F", key="pan_input_field")
        validate_pan_btn = st.button("Verify PAN", key="pan_submit_btn")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if validate_pan_btn:
            result = validators.validate_pan(pan_input)
            
            # Save validation to database history
            status_str = "Valid" if result.valid else "Invalid"
            user_id = st.session_state.get('user_id')
            
            save_query = """
                INSERT INTO validation_history (user_id, document_type, document_number, status, reason)
                VALUES (%s, 'PAN', %s, %s, %s)
            """
            try:
                db.execute_query(save_query, (user_id, result.normalized_input or pan_input, status_str, result.reason), commit=True)
                # Audit log
                auth.log_audit(user_id, "VALIDATE_PAN", "Validation", f"Validated PAN: {result.normalized_input or pan_input} - Result: {status_str}")
            except Exception as e:
                st.error(f"Failed to save record to database: {e}")
                
            # Display Result
            if result.valid:
                st.success(f"✅ **PAN is Valid!**\n\n{result.reason}")
                # Parse category details from PAN
                categories = {
                    'P': 'Individual',
                    'C': 'Company',
                    'H': 'Hindu Undivided Family (HUF)',
                    'F': 'Firm / Partnership',
                    'A': 'Association of Persons (AOP)',
                    'T': 'Trust',
                    'B': 'Body of Individuals (BOI)',
                    'L': 'Local Authority',
                    'J': 'Artificial Juridical Person',
                    'G': 'Government Agency'
                }
                cat_char = result.normalized_input[3]
                cat_name = categories.get(cat_char, "Unknown")
                
                st.markdown(f"""
                <div class="kyc-card" style="border-left: 5px solid #10b981 !important;">
                    <h5 style="margin-top: 0; color: #10b981;">PAN Details Extraction</h5>
                    <p style="margin-bottom: 5px;"><b>Normalized Input:</b> <code style="font-size: 1.1rem; color: #3b82f6;">{result.normalized_input}</code></p>
                    <p style="margin-bottom: 5px;"><b>Category Code:</b> <code>{cat_char}</code></p>
                    <p style="margin-bottom: 0;"><b>Holder Category:</b> <span style="font-weight: 600;">{cat_name}</span></p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"❌ **Validation Failed**\n\n{result.reason}")
                
    with tab2:
        st.markdown('<div class="kyc-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='margin-top: 0;'>Validate Aadhaar Card (12-Digit UID)</h4>", unsafe_allow_html=True)
        
        aadhaar_input = st.text_input("Enter Aadhaar Number", placeholder="e.g. 999912341234", key="aadhaar_input_field")
        validate_aadhaar_btn = st.button("Verify Aadhaar", key="aadhaar_submit_btn")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if validate_aadhaar_btn:
            result = validators.validate_aadhaar(aadhaar_input)
            
            # Save validation to database history
            status_str = "Valid" if result.valid else "Invalid"
            user_id = st.session_state.get('user_id')
            
            save_query = """
                INSERT INTO validation_history (user_id, document_type, document_number, status, reason)
                VALUES (%s, 'Aadhaar', %s, %s, %s)
            """
            try:
                db.execute_query(save_query, (user_id, result.normalized_input or aadhaar_input, status_str, result.reason), commit=True)
                # Audit log
                auth.log_audit(user_id, "VALIDATE_AADHAAR", "Validation", f"Validated Aadhaar: {result.normalized_input or aadhaar_input} - Result: {status_str}")
            except Exception as e:
                st.error(f"Failed to save record to database: {e}")
                
            # Display Result
            if result.valid:
                st.success(f"✅ **Aadhaar Checksum Valid!**\n\n{result.reason}")
                st.markdown(f"""
                <div class="kyc-card" style="border-left: 5px solid #10b981 !important;">
                    <h5 style="margin-top: 0; color: #10b981;">Aadhaar Verification</h5>
                    <p style="margin-bottom: 5px;"><b>Normalized Input:</b> <code style="font-size: 1.1rem; color: #3b82f6;">{result.normalized_input}</code></p>
                    <p style="margin-bottom: 0;"><b>Structure Test:</b> Verhoeff checksum matches. Safe for production processing.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"❌ **Validation Failed**\n\n{result.reason}")

if __name__ == "__main__":
    show_validate()
