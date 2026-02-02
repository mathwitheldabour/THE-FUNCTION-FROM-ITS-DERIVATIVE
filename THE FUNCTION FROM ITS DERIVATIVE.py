import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import random

# ---------------------------------------------------------
# 1. إعداد الصفحة والتنسيقات (CSS)
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="Bilingual Calculus Quiz")

st.markdown("""
<style>
    .stApp { text-align: center; }
    
    /* تنسيق صندوق السؤال */
    .question-container {
        background-color: #f0f8ff;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #007bff;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .q-text-en { font-size: 18px; font-weight: bold; color: #0056b3; direction: ltr; margin-bottom: 8px;}
    .q-text-ar { font-size: 20px; font-weight: bold; color: #0056b3; direction: rtl; font-family: 'Segoe UI', sans-serif;}

    /* تنسيق بطاقات الاختيارات */
    .option-card {
        background-color: white;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        transition: 0.3s;
    }
    .option-card:hover {
        border-color: #007bff;
        box-shadow: 0 0 10px rgba(0,123,255,0.2);
    }
    .opt-label {
        font-weight: bold;
        font-size: 20px;
        color: #d63384; /* لون الحرف A, B, C */
        margin-bottom: 5px;
        display: block;
    }
    .opt-en {
        display: block;
        direction: ltr;
        font-size: 18px;
        color: #333;
        font-weight: 500;
        margin-bottom: 5px;
    }
    .opt-ar {
        display: block;
        direction: rtl;
        font-size: 18px;
        color: #555;
        font-family: 'Segoe UI', sans-serif;
        border-top: 1px dashed #eee; /* فاصل خفيف */
        padding-top: 5px;
    }
    
    /* تحسين شكل الراديو وزر التحقق */
    .stRadio > div {
        flex-direction: row;
        justify-content: center;
        gap: 20px;
    }
    .stButton button {
        width: 60%;
        margin: 0 auto;
        display: block;
        font-size: 20px;
        background-color: #28a745;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. إدارة الحالة
# ---------------------------------------------------------
if 'q_index' not in st.session_state:
    st.session_state.q_index = 0

def next_question():
    if st.session_state.q_index < len(questions) - 1:
        st.session_state.q_index += 1

def prev_question():
    if st.session_state.q_index > 0:
        st.session_state.q_index -= 1

# ---------------------------------------------------------
# 3. الرسم البياني
# ---------------------------------------------------------
def plot_derivative(func_prime, x_range=(-4, 5), y_range=(-4, 5)):
    x = np.linspace(x_range[0], x_range[1], 1000)
    y = func_prime(x)
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.grid(True, which='both', linestyle=':', alpha=0.6)
    ax.plot(x, y, color='#d32f2f', linewidth=2.5)
    ax.text(x_range[1]*0.8, y_range[1]*0.8, "y = f'(x)", fontsize=12, color='#d32f2f', fontweight='bold')
    ax.set_ylim(y_range)
    ax.set_xlim(x_range)
    plt.tight_layout()
    return fig

# ---------------------------------------------------------
# 4. البيانات
# ---------------------------------------------------------
# تعريف المشتقات
def q1_deriv(x): return -x + 1 
def q2_deriv(x): return 0.5*(x-1)*(x-3) 
def q3_deriv(x): return 0.2*(x+1)**2 * (x-2)
def q4_deriv(x): return x 

# قائمة الأسئلة - لاحظ فصلنا النصوص الإنجليزية والعربية
questions = [
    {
        "id": 1,
        "func": q1_deriv,
        "q_en": "From the graph of f'(x), determine the local extrema.",
        "q_ar": "من رسم المشتقة f'(x)، حدد القيم القصوى المحلية.",
        "options": [
            {"code": "A", "en": r"Local Max at $x=1$", "ar": "قيمة عظمى محلية عند $x=1$", "is_correct": True},
            {"code": "B", "en": r"Local Min at $x=1$", "ar": "قيمة صغرى محلية عند $x=1$", "is_correct": False},
            {"code": "C", "en": r"Local Max at $x=0$", "ar": "قيمة عظمى محلية عند $x=0$", "is_correct": False},
            {"code": "D", "en": r"No local extrema", "ar": "لا توجد قيم قصوى محلية", "is_correct": False},
        ]
    },
    {
        "id": 2,
        "func": q2_deriv,
        "q_en": "Identify the intervals of decrease for f(x).",
        "q_ar": "حدد فترات التناقص للدالة f(x).",
        "options": [
            {"code": "A", "en": r"Decrease on $(1, 3)$", "ar": "متناقصة في الفترة $(1, 3)$", "is_correct": True},
            {"code": "B", "en": r"Decrease on $(-\infty, 1)$", "ar": "متناقصة في الفترة $(-\infty, 1)$", "is_correct": False},
            {"code": "C", "en": r"Decrease on $(-\infty, 1) \cup (3, \infty)$", "ar": "متناقصة في $(-\infty, 1)$ و $(3, \infty)$", "is_correct": False},
            {"code": "D", "en": r"Increase on $(1, 3)$", "ar": "متزايدة في الفترة $(1, 3)$", "is_correct": False},
        ]
    },
    {
        "id": 3,
        "func": q3_deriv,
        "q_en": "Analyze the critical point at $x=-1$.",
        "q_ar": "حلل النقطة الحرجة عند $x=-1$.",
        "options": [
            {"code": "A", "en": r"Neither Max nor Min (Saddle)", "ar": "ليست عظمى ولا صغرى (نقطة سرج)", "is_correct": True},
            {"code": "B", "en": r"Local Maximum", "ar": "قيمة عظمى محلية", "is_correct": False},
            {"code": "C", "en": r"Local Minimum", "ar": "قيمة صغرى محلية", "is_correct": False},
            {"code": "D", "en": r"Vertical Asymptote", "ar": "خط تقارب رأسي", "is_correct": False},
        ]
    },
    {
        "id": 4,
        "func": q4_deriv,
        "q_en": "Determine the behavior at $x=0$.",
        "q_ar": "حدد سلوك الدالة عند $x=0$.",
        "options": [
            {"code": "A", "en": r"Local Minimum", "ar": "قيمة صغرى محلية", "is_correct": True},
            {"code": "B", "en": r"Local Maximum", "ar": "قيمة عظمى محلية", "is_correct": False},
            {"code": "C", "en": r"Point of Inflection", "ar": "نقطة انقلاب", "is_correct": False},
            {"code": "D", "en": r"Discontinuity", "ar": "نقطة انفصال", "is_correct": False},
        ]
    }
]

# ---------------------------------------------------------
# 5. العرض
# ---------------------------------------------------------

q_idx = st.session_state.q_index
q = questions[q_idx]
progress = (q_idx + 1) / len(questions)

st.progress(progress)

# 1. عنوان السؤال
st.markdown(f"""
<div class="question-container">
    <div class="q-text-en">Q{q_idx+1}: {q['q_en']}</div>
    <div class="q-text-ar">س{q_idx+1}: {q['q_ar']}</div>
</div>
""", unsafe_allow_html=True)

# 2. الرسم البياني
col1, col_graph, col2 = st.columns([1, 2, 1])
with col_graph:
    st.pyplot(plot_derivative(q['func']))

st.write("---")

# 3. عرض الخيارات (الحيلة هنا: عرضنا HTML واستخدمنا الراديو للاختيار فقط)
# خلط الخيارات مرة واحدة وتثبيتها باستخدام الـ Seed
random.seed(q_idx + 3000)
current_options = q['options'].copy()
random.shuffle(current_options)

# عرض البطاقات المنسقة
cols = st.columns(len(current_options))
for idx, opt in enumerate(current_options):
    # نعيد تسمية الكود ليكون A, B, C, D بناءً على الترتيب الجديد
    display_code = chr(65 + idx) 
    opt['display_code'] = display_code # حفظ الحرف المعروض للاستخدام لاحقاً
    
    with cols[idx]:
        st.markdown(f"""
        <div class="option-card">
            <span class="opt-label">{display_code}</span>
            <span class="opt-en">{opt['en']}</span>
            <span class="opt-ar">{opt['ar']}</span>
        </div>
        """, unsafe_allow_html=True)

# 4. زر الاختيار (بسيط جداً الآن)
selection = st.radio(
    "Select the correct option / اختر الرمز الصحيح:",
    [opt['display_code'] for opt in current_options],
    horizontal=True,
    label_visibility="collapsed"
)

st.write("")
check = st.button("Check Answer / تحقق من الإجابة")

if check:
    # البحث عن الخيار المختار
    chosen_opt = next(item for item in current_options if item["display_code"] == selection)
    
    if chosen_opt['is_correct']:
        st.success("✅ Correct! إجابة صحيحة")
        st.balloons()
    else:
        st.error("❌ Incorrect. إجابة خاطئة")
        # البحث عن الإجابة الصحيحة لعرضها
        correct_opt = next(item for item in current_options if item["is_correct"])
        st.markdown(f"""
        <div style="background-color:#d4edda; color:#155724; padding:10px; border-radius:5px; direction:rtl; text-align:center;">
            الإجابة الصحيحة هي: <b>{correct_opt['display_code']}</b><br>
            {correct_opt['ar']} <br> {correct_opt['en']}
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
c1, c2 = st.columns(2)
with c1:
    if st.session_state.q_index > 0:
        if st.button("⬅️ Previous / السابق"):
            prev_question()
            st.rerun()
with c2:
    if st.session_state.q_index < len(questions) - 1:
        if st.button("Next / التالي ➡️"):
            next_question()
            st.rerun()
