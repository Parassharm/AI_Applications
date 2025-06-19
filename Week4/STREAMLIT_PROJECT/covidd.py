# 📦 आवश्यक लाइब्रेरीहरू
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from PIL import Image
import base64

# 🎨 पृष्ठभूमि र शैली सेटअप
def set_background():
    # एस्थेटिक ब्याकग्राउन्ड इमेज
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(255,255,255,0.8), rgba(255,255,255,0.8)), 
                        url("data:image/png;base64,{base64.b64encode(open('health_bg.jpg', 'rb').read()).decode()}");
            background-size: cover;
            background-attachment: fixed;
            font-family: 'Arial Unicode MS', 'Preeti', sans-serif;
        }}
        
        /* साइडबार डिजाइन */
        .sidebar .sidebar-content {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white;
            border-right: 2px solid #4b6cb7;
        }}
        
        /* कार्ड डिजाइन */
        .custom-card {{
            background-color: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 6px 12px rgba(0,0,0,0.1);
            margin-bottom: 25px;
            border-left: 5px solid #4b6cb7;
        }}
        
        /* हेडर डिजाइन */
        .main-header {{
            background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }}
        
        /* अलर्ट बक्सहरू */
        .alert-high-risk {{
            background: linear-gradient(135deg, #ff758c 0%, #ff7eb3 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            border-left: 6px solid #e53e3e;
        }}
        
        .alert-low-risk {{
            background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            border-left: 6px solid #38a169;
        }}
        
        /* बटन डिजाइन */
        .stButton>button {{
            background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: bold;
        }}
        
        /* मेट्रिक बक्स */
        .metric-box {{
            background: rgba(255,255,255,0.9);
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border-left: 4px solid #4b6cb7;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# 👉 डाटा लोड गर्ने
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Covid Data.csv")
        
        # डाटा सफा गर्ने
        df = df.drop_duplicates()
        df['IS_DEAD'] = df['DATE_DIED'].apply(lambda x: 0 if x == '9999-99-99' else 1)
        
        cols_to_clean = ['ICU', 'PNEUMONIA', 'DIABETES', 'COPD', 'ASTHMA', 'INMSUPR', 
                         'CARDIOVASCULAR', 'OBESITY', 'RENAL_CHRONIC', 'TOBACCO']
        df[cols_to_clean] = df[cols_to_clean].replace([97, 98, 99], np.nan)
        df = df.dropna(subset=cols_to_clean)
        
        return df
    
    except Exception as e:
        st.markdown(f"""
        <div class="custom-card" style="border-left-color: #e53e3e;">
        <h3 style="color:#e53e3e;">❌ त्रुटि</h3>
        <p>डाटा लोड गर्दा समस्या आयो: <strong>{str(e)}</strong></p>
        <p>कृपया 'Covid Data.csv' फाइल जाँच गर्नुहोस्</p>
        </div>
        """, unsafe_allow_html=True)
        return None

# 📊 डाटा विश्लेषण चार्टहरू
def show_analysis(df):
    st.markdown("""
    <div class="custom-card">
    <h3 style="color:#2a4365; text-align:center;">📈 डाटा विश्लेषण</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # उमेर वितरण
        fig, ax = plt.subplots(figsize=(10,5))
        df['AGE'].hist(bins=20, ax=ax, color='#4b6cb7', edgecolor='white')
        ax.set_title('Age distribution', fontsize=14, pad=20)
        ax.set_xlabel('Age', fontsize=12)
        ax.set_ylabel('Calculation', fontsize=12)
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)
    
    with col2:
        # मृत्यु दर
        death_rate = df['IS_DEAD'].value_counts(normalize=True) * 100
        fig, ax = plt.subplots(figsize=(10,5))
        death_rate.plot(kind='bar', color=['#38a169', '#e53e3e'], edgecolor='white', ax=ax)
        ax.set_title('Death rate', fontsize=14, pad=20)
        ax.set_xticklabels(['Alive', 'Dead'], rotation=0, fontsize=12)
        ax.set_ylabel('Percentage', fontsize=12)
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)

    # डाटा सारांश
    st.markdown("""
    <div class="custom-card">
    <h4 style="color:#2a4365; text-align:center;">📋 डाटा सारांश</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-box">
        <h4 style="color:#4b6cb7;">कुल डाटा</h4>
        <h2 style="color:#2a4365;">{df.shape[0]:,}</h2>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-box">
        <h4 style="color:#4b6cb7;">मृत्यु भएका</h4>
        <h2 style="color:#e53e3e;">{df['IS_DEAD'].sum():,}</h2>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-box">
        <h4 style="color:#4b6cb7;">बाँचेका</h4>
        <h2 style="color:#38a169;">{len(df) - df['IS_DEAD'].sum():,}</h2>
        </div>
        """, unsafe_allow_html=True)

# मुख्य एप्लिकेसन
def main():
    # पृष्ठभूमि सेटअप
    set_background()
    
    # हेडर सेक्सन
    st.markdown("""
    <div class="main-header">
    <h1 style="color:white; margin-bottom:10px;">COVID-19 मृत्यु जोखिम मूल्यांकन</h1>
    <p style="font-size:18px; color:rgba(255,255,255,0.9);">यो एप्लिकेसनले Logistic Regression प्रयोग गरेर COVID-19 रोगीको मृत्युको सम्भावना अनुमान गर्छ</p>
    </div>
    """, unsafe_allow_html=True)
    
    # डाटा लोड गर्ने
    df = load_data()
    
    if df is not None:
        # मोडेल तयार गर्ने
        features = ['AGE', 'SEX', 'DIABETES', 'OBESITY', 'PNEUMONIA', 'TOBACCO']
        X = df[features]
        y = df['IS_DEAD']
        model = LogisticRegression(max_iter=1000)
        model.fit(X, y)
        
        # -------------------------------
        # साइडबार इनपुट
        # -------------------------------
        with st.sidebar:
            st.markdown("""
            <div style="background-color:rgba(255,255,255,0.2); padding:15px; border-radius:12px; margin-bottom:25px;">
            <h3 style="color:green; text-align:center;">🧾 रोगीको जानकारी</h3>
            </div>
            """, unsafe_allow_html=True)
            
            AGE = st.slider("उमेर", 0, 120, 40, help="रोगीको उमेर")
            SEX = st.selectbox("लिङ्ग", ("पुरुष", "महिला"), index=0)
            SEX = 1 if SEX == "पुरुष" else 2
            
            DIABETES = st.selectbox("मधुमेह", ("छैन", "छ"), index=0)
            DIABETES = 1 if DIABETES == "छ" else 2
            
            OBESITY = st.selectbox("मोटोपन", ("छैन", "छ"), index=0)
            OBESITY = 1 if OBESITY == "छ" else 2
            
            PNEUMONIA = st.selectbox("निमोनिया", ("छैन", "छ"), index=0)
            PNEUMONIA = 1 if PNEUMONIA == "छ" else 2
            
            TOBACCO = st.selectbox("धूम्रपान", ("छैन", "छ"), index=0)
            TOBACCO = 1 if TOBACCO == "छ" else 2
            
            if st.button("🔍 जोखिम मूल्यांकन गर्नुहोस्", use_container_width=True):
              st.success("मूल्यांकन सफल भयो!")


        
        # इनपुट डाटा तयार गर्ने
        input_data = {
            'AGE': AGE,
            'SEX': SEX,
            'DIABETES': DIABETES,
            'OBESITY': OBESITY,
            'PNEUMONIA': PNEUMONIA,
            'TOBACCO': TOBACCO
        }
        input_df = pd.DataFrame([input_data])
        
        # 🔍 इनपुट जानकारी देखाउने
        st.markdown("""
        <div class="custom-card">
        <h3 style="color:#2a4365; text-align:center;">🔍 तपाईंले दिनुभएको जानकारी</h3>
        </div>
        """, unsafe_allow_html=True)
        
        cols = st.columns(3)
        with cols[0]:
            st.markdown(f"""
            <div class="metric-box">
            <h4>उमेर</h4>
            <h2 style="color:#4b6cb7;">{AGE} वर्ष</h2>
            </div>
            """, unsafe_allow_html=True)
        with cols[1]:
            gender = "पुरुष" if SEX == 1 else "महिला"
            st.markdown(f"""
            <div class="metric-box">
            <h4>लिङ्ग</h4>
            <h2 style="color:#4b6cb7;">{gender}</h2>
            </div>
            """, unsafe_allow_html=True)
        with cols[2]:
            diabetes = "छ" if DIABETES == 1 else "छैन"
            st.markdown(f"""
            <div class="metric-box">
            <h4>मधुमेह</h4>
            <h2 style="color:#4b6cb7;">{diabetes}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        cols = st.columns(3)
        with cols[0]:
            obesity = "छ" if OBESITY == 1 else "छैन"
            st.markdown(f"""
            <div class="metric-box">
            <h4>मोटोपन</h4>
            <h2 style="color:#4b6cb7;">{obesity}</h2>
            </div>
            """, unsafe_allow_html=True)
        with cols[1]:
            pneumonia = "छ" if PNEUMONIA == 1 else "छैन"
            st.markdown(f"""
            <div class="metric-box">
            <h4>निमोनिया</h4>
            <h2 style="color:#4b6cb7;">{pneumonia}</h2>
            </div>
            """, unsafe_allow_html=True)
        with cols[2]:
            tobacco = "छ" if TOBACCO == 1 else "छैन"
            st.markdown(f"""
            <div class="metric-box">
            <h4>धूम्रपान</h4>
            <h2 style="color:#4b6cb7;">{tobacco}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # 📊 अनुमान गर्ने
        prediction = model.predict(input_df)[0]
        prediction_proba = model.predict_proba(input_df)[0][1]
        
        # 🧾 नतिजा देखाउने
        st.markdown("""
        <div class="custom-card">
        <h3 style="color:#2a4365; text-align:center;">🧮 मृत्युको सम्भावना</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if prediction == 1:
            st.markdown(f"""
            <div class="alert-high-risk">
            <h2 style="color:white; text-align:center; margin-top:0;">⚠️ उच्च जोखिम!</h2>
            <h1 style="color:white; text-align:center; font-size:42px;">{prediction_proba*100:.2f}%</h1>
            <p style="text-align:center; color:rgba(255,255,255,0.9);">मृत्यु हुने सम्भावना</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="custom-card" style="border-left-color:#e53e3e;">
            <h4 style="color:#e53e3e;">🚨 सुझावहरू:</h4>
            <ul style="font-size:16px;">
            <li>डाक्टरसँग तुरुन्तै सम्पर्क गर्नुहोस्</li>
            <li>आइसोलेशनमा रहनुहोस्</li>
            <li>अक्सिजन लेभल मोनिटर गर्नुहोस्</li>
            <li>नियमित स्वास्थ्य जाँच गर्नुहोस्</li>
            <li>आपतकालीन सेवासँग सम्पर्क राख्नुहोस्</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="alert-low-risk">
            <h2 style="color:white; text-align:center; margin-top:0;">सुरक्षित देखिन्छ!</h2>
            <h1 style="color:white; text-align:center; font-size:42px;">{prediction_proba*100:.2f}%</h1>
            <p style="text-align:center; color:rgba(255,255,255,0.9);">मृत्यु हुने सम्भावना</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="custom-card" style="border-left-color:#38a169;">
            <h4 style="color:#38a169;">🛡️ सुझावहरू:</h4>
            <ul style="font-size:16px;">
            <li>स्वच्छताको पालना गर्नुहोस्</li>
            <li>सामाजिक दूरी कायम राख्नुहोस्</li>
            <li>नियमित रूपमा हात धुनुहोस्</li>
            <li>मास्क लगाउनुहोस्</li>
            <li>रोग प्रतिरोधक क्षमता बढाउने खाना खानुहोस्</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # डाटा विश्लेषण देखाउने
        show_analysis(df)
        
        # फुटर
        st.markdown("---")
        st.markdown("""
        <div style="text-align:center; color:#4a5568; padding:20px;">
        <p style="font-size:14px;">यो एप्लिकेसन Logistic Regression मोडेलमा आधारित छ</p>
        <p style="font-size:12px;">© 2082 KMC SEEP MELA AI AND IT'S APPLICATION TRAINING | नेपाली संस्करण</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()