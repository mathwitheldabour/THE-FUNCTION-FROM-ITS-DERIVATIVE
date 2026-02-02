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
    /* 1. توسيط عام للتطبيق */
    .stApp {
        text-align: center;
    }
    
    /* 2. تنسيق صندوق السؤال */
    .question-container {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #e9ecef;
        margin-bottom: 20px;
        text-align: center;
    }
    .q-text-en {
        font-size: 18px;
        font-weight: bold;
        color: #0d6efd;
        margin-bottom: 5px;
        direction: ltr; /* انجليزي يسار ليمين */
    }
    .q-text-ar {
        font-size: 20px;
        font-weight: bold;
        color: #0d6efd;
        margin-top: 5px;
        direction: rtl; /* عربي يمين ليسار */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* 3. تنسيق خيارات الراديو (الأهم) */
    
    /* جعل الحاوية للكلام في المنتصف */
    div[role="radiogroup"] {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
    }
    
    /* تنسيق كل خيار على حدة */
    div[data-testid="stMarkdownContainer"] p {
        text-align: center; /* توسيط النص */
        font-size: 18px;
        line-height: 1.6;
    }
    
    /* تنسيق خاص لفصل اللغتين داخل الخيار الواحد */
    .opt-en {
        display: block;
        direction: ltr;
        color: #333;
        font-weight: 500;
    }
    .opt-ar {
        display: block;
        direction: rtl;
        color: #555;
        margin-top: 4px;
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* تنسيق الزر */
    .stButton button {
        width: 50%;
        margin: 0 auto;
        display: block;
        font-size: 20px;
        background-color: #0d6efd;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. إدارة حالة الجلسة
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
# 3. دالة الرسم البياني للمشتقة
# ---------------------------------------------------------
def plot_derivative(func_prime, x_range=(-4, 5), y_range=(-4, 5)):
    x = np.linspace(x_range[0], x_range[1], 1000)
    y = func_prime(x)
    
    fig, ax = plt.subplots(figsize=(6, 3))
    
    # محاور في المنتصف
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.grid(True, which='both', linestyle=':', alpha=0.6)
    
    # الرسم
    ax.plot(x, y, color='#d32f2f', linewidth=2.5, label="f'(x)")
    ax.text(x_range[1]*0.8, y_range[1]*0.8, "y = f'(x)", fontsize=12, color='#d32f2f', fontweight='bold')
    
    ax.set_ylim(y_range)
    ax.set_xlim(x_range)
    plt.tight_layout()
    return fig

# ---------------------------------------------------------
# 4. البيانات (تنسيق النصوص HTML داخل Markdown)
# ---------------------------------------------------------

# دالة مساعدة لتنسيق النص (انجليزي فوق - عربي تحت)
def format_option(en_text, ar_text):
    # نستخدم HTML span مع كلاسات CSS التي عرفناها بالأعلى
    return f"""<span class="opt-en">{en_text}</span><span class="opt-ar">{ar_text}</span>"""

# تعريف المشتقات
def q1_deriv(x): return -x + 1 
def q2_deriv(x): return 0.5*(x-1)*(x-3) 
def q3_deriv(x): return 0.2*(x+1)**2 * (x-2)
def q4_deriv(x): return x 

questions = [
    {
        "id": 1,
        "func": q1_deriv,
        "q_en": "From the graph of f'(x), determine the local extrema.",
        "q_ar": "من رسم المشتقة f'(x)، حدد القيم القصوى المحلية.",
        "correct": format_option(r"Local Max at $x=1$", "قيمة عظمى محلية عند $x=1$"),
        "distractors": [
            format_option(r"Local Min at $x=1$", "قيمة صغرى محلية عند $x=1$"),
            format_option(r"Local Max at $x=0$", "قيمة عظمى محلية عند $x=0$"),
            format_option(r"No local extrema", "لا توجد قيم قصوى محلية")
        ]
    },
    {
        "id": 2,
        "func": q2_deriv,
        "q_en": "Identify the intervals of decrease for f(x).",
        "q_ar": "حدد فترات التناقص للدالة f(x).",
        "correct": format_option(r"Decrease on $(1, 3)$", "متناقصة في الفترة $(1, 3)$"),
        "distractors": [
            format_option(r"Decrease on $(-\infty, 1)$ and $(3, \infty)$", "متناقصة في $(-\infty, 1)$ و $(3, \infty)$"),
            format_option(r"Decrease on $(-\infty, 2)$", "متناقصة في الفترة $(-\infty, 2)$"),
            format_option(r"Increase on $(1, 3)$", "متزايدة في الفترة $(1, 3)$")
        ]
    },
    {
        "id": 3,
        "func": q3_deriv,
        "q_en": "Analyze the critical point at $x=-1$.",
        "q_ar": "حلل النقطة الحرجة عند $x=-1$.",
        "correct": format_option(r"Neither Max nor Min (Saddle)", "ليست عظمى ولا صغرى (نقطة سرج)"),
        "distractors": [
            format_option(r"Local Maximum", "قيمة عظمى محلية"),
            format_option(r"Local Minimum", "قيمة صغرى محلية"),
            format_option(r"Inflection Point only", "نقطة انقلاب فقط")
        ]
    },
    {
        "id": 4,
        "func": q4_deriv,
        "q_en": "Determine the behavior at $x=0$.",
        "q_ar": "حدد سلوك الدالة عند $x=0$.",
        "correct": format_option(r"Local Minimum", "قيمة صغرى محلية"),
        "distractors": [
            format_option(r"Local Maximum", "قيمة عظمى محلية"),
            format_option(r"Discontinuity", "نقطة انفصال"),
            format_option(r"Vertical Asymptote", "خط تقارب رأسي")
        ]
    }
]

# ---------------------------------------------------------
# 5. العرض
# ---------------------------------------------------------

q_idx = st.session_state.q_index
q = questions[q_idx]
progress = (q_idx + 1) / len(questions)

# شريط التقدم
st.progress(progress)

# 1. عنوان السؤال (في المنتصف)
st.markdown(f"""
<div class="question-container">
    <div class="q-text-en">Q{q_idx+1}: {q['q_en']}</div>
    <div class="q-text-ar">س{q_idx+1}: {q['q_ar']}</div>
</div>
""", unsafe_allow_html=True)

# 2. الرسم البياني (في المنتصف)
col_spacer1, col_graph, col_spacer2 = st.columns([1, 2, 1])
with col_graph:
    st.pyplot(plot_derivative(q['func']))

st.write("---")

# 3. الاختيارات (في المنتصف، انجليزي فوق عربي)
options = [q['correct']] + q['distractors']
random.seed(q_idx + 2024)
random.shuffle(options)

# نستخدم allow_unsafe_html لعرض الـ span والـ css داخل الراديو
# ملاحظة: streamlit لا يدعم html داخل الراديو بشكل مباشر إلا عبر markdown wrapper،
# ولكن هنا سنستخدم الحيلة عبر تمرير النصوص وسيتكفل الـ CSS بالأعلى بالتنسيق.
# بما أن st.radio يقرأ النص كنص عادي، سنستخدم التنسيق عبر class CSS على الحاوية.

# الحل الأفضل لضمان التنسيق هو استخدام captions مخصصة، ولكن للراديو سنعتمد على Markdown rendering
user_choice = st.radio(
    "Select Answer / اختر الإجابة:",
    options,
    key=f"radio_{q_idx}",
    label_visibility="collapsed" # إخفاء عنوان الراديو لأنه مكرر
)

st.write("---")

# 4. زر التحقق والتنقل (في المنتصف)
check = st.button("Check Answer / تحقق من الإجابة")

if check:
    # بما أن النصوص تحتوي HTML للمقارنة يجب أن تكون دقيقة
    if user_choice == q['correct']:
        st.success("✅ Correct! إجابة صحيحة")
        st.balloons()
    else:
        st.error("❌ Incorrect. إجابة خاطئة")

# مساحة فاصلة
st.write("")

# أزرار التنقل
col_prev, col_next = st.columns(2)
with col_prev:
    if st.session_state.q_index > 0:
        if st.button("⬅️ Previous / السابق"):
            prev_question()
            st.rerun()
with col_next:
    if st.session_state.q_index < len(questions) - 1:
        if st.button("Next / التالي ➡️"):
            next_question()
            st.rerun()
