import streamlit as st
import pickle
import pandas as pd
import numpy as np
from datetime import datetime

with open('models/ensemble_model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('models/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)
with open('models/label_encoders.pkl', 'rb') as f:
    label_encoders = pickle.load(f)

st.set_page_config(
    page_title="Risk Classification Tool",
    page_icon="🔍",
    layout="wide"
)

st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
            padding: 20px;
        }
        
        .header-container {
            background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            text-align: center;
        }
        
        .app-title {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: black;
        }
        
        .app-subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
            color: black;
        }
        
        .form-card {
            background-color: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
        }
        
        .section-title {
            font-size: 1.3rem;
            font-weight: 600;
            color: black;
            margin-bottom: 1rem;
            border-bottom: 2px solid #4b6cb7;
            padding-bottom: 0.5rem;
        }
        
        .results-card {
            text-align: center;
            padding: 2rem;
            border-radius: 10px;
        }
        
        .result-risk {
            background: linear-gradient(90deg, #FF416C 0%, #FF4B2B 100%);
        }
        
        .result-safe {
            background: linear-gradient(90deg, #56ab2f 0%, #a8e063 100%);
        }
        
        .prediction-text {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 1rem;
            color: black;
        }
        
        .prediction-description {
            font-size: 1.2rem;
            opacity: 0.9;
            color: black;
        }
        
        .stButton>button {
            background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
            color: black;
            border: none;
            border-radius: 5px;
            font-size: 1.1rem;
            font-weight: 600;
            padding: 0.75rem 2rem;
            width: 100%;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(75, 108, 183, 0.3);
        }
        
        .stSelectbox>div>div>div {
            background-color: #f8f9fa;
            border-radius: 5px;
            border: 1px solid #e0e0e0;
            color: black;
        }
        
        .stNumberInput>div>div>input {
            background-color: #f8f9fa;
            border-radius: 5px;
            border: 1px solid #e0e0e0;
            padding: 0.5rem;
            color: black;
        }
        
        body {
            color: black !important;
        }
        
        p, span, label, .stMarkdown, .stText, .stExpander, .stInfo, h1, h2, h3, h4, h5, h6 {
            color: black !important;
        }
        
        .stAlert > div {
            color: black !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header-container">
        <div class="app-title">Risk Classification Tool</div>
        <div class="app-subtitle">Advanced analysis for financial risk assessment</div>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">Personal Information</div>', unsafe_allow_html=True)
    pcol1, pcol2 = st.columns(2)
    
    with pcol1:
        age = st.number_input('Age', min_value=18, max_value=100, value=30, step=1)
        sex = st.selectbox('Gender', ['male', 'female'])
    
    with pcol2:
        job = st.selectbox('Job Level', ['0', '1', '2', '3'], 
                          help="0: Unskilled, 1: Skilled (non-resident), 2: Skilled (resident), 3: Highly skilled")
        housing = st.selectbox('Housing Situation', ['own', 'rent', 'free'])
    
    st.markdown('<div class="section-title">Financial Information</div>', unsafe_allow_html=True)
    fcol1, fcol2 = st.columns(2)
    
    with fcol1:
        saving_accounts = st.selectbox('Savings Account Status', 
                                      ['little', 'moderate', 'quite rich', 'rich'],
                                      help="Level of savings you currently maintain")
        
        checking_account = st.selectbox('Checking Account Status', 
                                       ['little', 'moderate', 'rich'],
                                       help="Level of funds in your checking account")
    
    with fcol2:
        credit_amount = st.number_input('Credit Amount ($)', 
                                       min_value=0, max_value=100000, value=5000, step=100,
                                       help="Amount of credit requested")
        
        duration = st.slider('Loan Duration (months)', 
                            min_value=1, max_value=60, value=12,
                            help="Period over which the loan will be repaid")
    
    st.markdown('<div class="section-title">Loan Purpose</div>', unsafe_allow_html=True)
    
    purpose = st.selectbox('Purpose of Loan', 
                          ['car', 'radio/TV', 'furniture/equipment', 'business', 'education'],
                          help="What the loan will be used for")
    
    if purpose == 'car':
        st.info("Financing for a vehicle purchase.")
    elif purpose == 'radio/TV':
        st.info("Purchase of electronic entertainment devices.")
    elif purpose == 'furniture/equipment':
        st.info("Purchase of household items or equipment.")
    elif purpose == 'business':
        st.info("Funding for business-related expenses.")
    elif purpose == 'education':
        st.info("Funding for formal education expenses.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    predict_btn = st.button('Analyze Risk Profile')

with col2:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Quick Tips</div>', unsafe_allow_html=True)
    
    st.markdown("""
    - **Higher savings** typically indicate lower risk
    - **Longer loan duration** may increase risk assessment
    - **Home ownership** is usually viewed favorably
    - **Employment status** affects risk evaluation
    """)
    
    st.info("This tool uses machine learning to predict risk categories based on your inputs. The prediction is based on historical data patterns.")
    
    st.markdown(f"<div style='text-align: center; margin-top: 20px; color: black;'>Today: {datetime.now().strftime('%B %d, %Y')}</div>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

if predict_btn:
    with st.spinner("Analyzing risk profile..."):
        input_data = pd.DataFrame({
            'Age': [age],
            'Sex': [sex],
            'Job': [int(job)],
            'Housing': [housing],
            'Saving accounts': [saving_accounts],
            'Checking account': [checking_account],
            'Credit amount': [credit_amount],
            'Duration': [duration],
            'Purpose': [purpose]
        })

        categorical_cols = ['Sex', 'Housing', 'Saving accounts', 'Checking account', 'Purpose']
        for col in categorical_cols:
            try:
                input_data[col] = label_encoders[col].transform(input_data[col])
            except ValueError:
                st.error(f"Invalid value for {col}. Please select a valid option.")
                st.stop()

        input_scaled = scaler.transform(input_data)

        prediction = model.predict(input_scaled)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if prediction[0] == 1:
        st.markdown("""
            <div class="results-card result-risk">
                <div class="prediction-text">⚠️ High Risk Profile</div>
                <div class="prediction-description">
                    Based on the provided information, this profile is classified as higher risk.
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.expander("Risk Assessment Details"):
            st.markdown("""
                ### Risk Factors That May Be Contributing:
                
                - **Credit amount** in relation to income
                - **Loan duration** and repayment timeline
                - **Account status** and financial history
                - **Housing situation** and stability
                
                *This assessment is based on statistical patterns and may not reflect individual circumstances.*
            """)
            
    else:
        st.markdown("""
            <div class="results-card result-safe">
                <div class="prediction-text">✅ Low Risk Profile</div>
                <div class="prediction-description">
                    Based on the provided information, this profile is classified as lower risk.
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.expander("Risk Assessment Details"):
            st.markdown("""
                ### Positive Factors Contributing:
                
                - **Financial stability** indicators
                - **Credit amount** appears appropriate
                - **Loan purpose** and duration alignment
                - **Account status** shows good management
                
                *This assessment is based on statistical patterns and does not guarantee loan approval.*
            """)