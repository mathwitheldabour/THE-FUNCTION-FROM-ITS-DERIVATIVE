import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import random

# ---------------------------------------------------------
# 1. إعداد الصفحة والتنسيقات
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="Bilingual Calculus Quiz")

st.markdown("""
<style>
    /* جعل التطبيق يدعم الكتابة المختلطة */
    .stApp { direction: ltr; }
    
    /* تنسيق صندوق السؤال */
    .question-box {
        background-color: #f0f7ff;
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 25px;
        border-left: 6px solid #0056b3;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .q-header-en {
        font-size: 18px;
        font-weight: bold;
        color: #0056b3;
        margin-bottom: 5px;
        text-align: left;
        font-family: sans-serif;
    }
    
    .q-header-ar {
        font-size: 20px;
        font-weight: bold;
        color: #0056b3;
        margin-bottom: 15px;
        text-align: right;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        direction: rtl;
    }
    
    /* تنسيق الخيارات (Radio Buttons) */
    .stRadio > div {
        direction: ltr !important; /* إجبار الاتجاه من اليسار لليمين */
        text-align: left !important;
        background-color: #ffffff;
        padding: 10px;
        border-radius: 8px;
    }
    
    /* تكبير خط الخيارات ليكون واضحاً */
    .stRadio label {
        font-size: 16px !important;
        padding-bottom: 10px;
    }

    .stButton button { width: 100%; font-size: 18px; font-weight: bold; }
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
    
    fig, ax = plt.subplots(figsize=(8, 3.5)) # عرض أوسع قليلاً
    
    # محاور في المنتصف
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.grid(True, which='both', linestyle=':', alpha=0.6)
    
    # رسم المشتقة
    ax.plot(x, y, color='#d32f2f', linewidth=2.5, label="f'(x)")
    
    # عنوان الرسم داخل الإطار
    ax.text(x_range[1]*0.85, y_range[1]*0.8, "y = f'(x)", fontsize=12, color='#d32f2f', fontweight='bold')
    
    ax.set_ylim(y_range)
    ax.set_xlim(x_range)
    plt.tight_layout()
    return fig

# ---------------------------------------------------------
# 4. بيانات الأسئلة (ثنائية اللغة)
# ---------------------------------------------------------

# الدوال الرياضية (المشتقات)
def q1_deriv(x): return -x + 1 # خطي يقطع عند 1
def q2_deriv(x): return (x-1)*(x-3) * 0.5 # قطع مكافئ يقطع عند 1 و 3 (مقعر لأعلى)
def q3_deriv(x): return -0.5*(x+1)**2 * (x-2) # يمس عند -1 ويقطع عند 2
def q4_deriv(x): return x # يقطع عند 0

# قائمة الأسئلة
questions = [
    {
        "id": 1,
        "func": q1_deriv,
        "q_en": "Based on the graph of $f'(x)$, determine the intervals of increase/decrease and extrema.",
        "q_ar": "بناءً على رسم المشتقة $f'(x)$، حدد فترات التزايد والتناقص والقيم القصوى.",
        "correct": r"Inc on $(-\infty, 1)$, Dec on $(1, \infty)$; Max at $x=1$  ||  تزايد $(-\infty, 1)$، تناقص $(1, \infty)$؛ عظمى عند $1$",
        "distractors": [
            r"Dec on $(-\infty, 1)$, Inc on $(1, \infty)$; Min at $x=1$  ||  تناقص $(-\infty, 1)$، تزايد $(1, \infty)$؛ صغرى عند $1$",
            r"Inc on $(-\infty, 0)$, Dec on $(0, \infty)$; Max at $x=0$  ||  تزايد $(-\infty, 0)$، تناقص $(0, \infty)$؛ عظمى عند $0$",
            r"Increasing everywhere; Inflection at $x=1$  ||  تزايد على مجالها؛ نقطة انقلاب عند $1$"
        ]
    },
    {
        "id": 2,
        "func": q2_deriv, # + (inc) -> 1 -> - (dec) -> 3 -> + (inc)
        "q_en": "Identify the local extrema and monotonicity from the graph of $f'(x)$.",
        "q_ar": "حدد القيم القصوى المحلية وفترات الاطراد من رسم المشتقة $f'(x)$.",
        "correct": r"Max at $x=1$, Min at $x=3$  ||  عظمى عند $x=1$، صغرى عند $x=3$",
        "distractors": [
            r"Min at $x=1$, Max at $x=3$  ||  صغرى عند $x=1$، عظمى عند $x=3$",
            r"Max at $x=2$ (Vertex)  ||  عظمى عند رأس المنحنى $x=2$",
            r"Decreasing on $(1, 3)$ only  ||  متناقصة فقط في الفترة $(1, 3)$"
        ]
    },
    {
        "id": 3,
        "func": q3_deriv, # + -> -1 (touch) -> + -> 2 -> -
        "q_en": "Analyze the critical points of $f(x)$ given the graph of $f'(x)$.",
        "q_ar": "حلل النقاط الحرجة للدالة $f(x)$ بناءً على رسم المشتقة.",
        "correct": r"Inc $(-\infty, 2)$, Dec $(2, \infty)$; Max at $x=2$  ||  تزايد $(-\infty, 2)$، تناقص $(2, \infty)$؛ عظمى عند $2$",
        "distractors": [
            r"Max at $x=-1$, Min at $x=2$  ||  عظمى عند $-1$، صغرى عند $2$",
            r"Min at $x=-1$, Max at $x=2$  ||  صغرى عند $-1$، عظمى عند $2$",
            r"Dec $(-\infty, 2)$, Inc $(2, \infty)$; Min at $x=2$  ||  تناقص $(-\infty, 2)$، تزايد $(2, \infty)$؛ صغرى عند $2$"
        ]
    },
    {
        "id": 4,
        "func": q4_deriv, # - -> 0 -> +
        "q_en": "Find the local extrema of $f(x)$ from the graph of $f'(x)$.",
        "q_ar": "أوجد القيم القصوى المحلية للدالة $f(x)$ من رسم المشتقة.",
        "correct": r"Local Min at $x=0$  ||  قيمة صغرى محلية عند $x=0$",
        "distractors": [
            r"Local Max at $x=0$  ||  قيمة عظمى محلية عند $x=0$",
            r"No local extrema  ||  لا توجد قيم قصوى محلية",
            r"Inflection point at $x=0$  ||  نقطة انقلاب عند $x=0$"
        ]
    }
]

# ---------------------------------------------------------
# 5. العرض (Rendering)
# ---------------------------------------------------------

q_idx = st.session_state.q_index
q = questions[q_idx]

progress = (q_idx + 1) / len(questions)
st.progress(progress)

# --- صندوق السؤال (ثنائي اللغة) ---
st.markdown(f"""
<div class="question-box">
    <div class="q-header-en">Q{q_idx+1}: {q['q_en']}</div>
    <div class="q-header-ar">س{q_idx+1}: {q['q_ar']}</div>
</div>
""", unsafe_allow_html=True)

# --- رسم المشتقة ---
col_l, col_c, col_r = st.columns([1, 6, 1])
with col_c:
    st.pyplot(plot_derivative(q['func']))

st.markdown("---")

# --- الاختيارات (Bilingual & LTR) ---
options = [q['correct']] + q['distractors']
random.seed(q_idx + 100)
random.shuffle(options)

# عرض الاختيارات
selected_option = st.radio(
    "Choose the correct answer / اختر الإجابة الصحيحة:",
    options,
    key=f"radio_{q_idx}"
)

# زر التحقق
col_btn_l, col_btn_r = st.columns([3, 1])
with col_btn_r:
    st.write("")
    check = st.button("Check / تحقق")

# نتيجة التحقق
if check:
    if selected_option == q['correct']:
        st.success("Correct Answer! ✅ إجابة صحيحة")
        st.balloons()
    else:
        st.error("Incorrect ❌ إجابة خاطئة")
        st.info(f"The Correct Answer is: \n\n {q['correct']}")

# أزرار التنقل
st.markdown("---")
c1, c2, c3 = st.columns([1, 2, 1])
with c1:
    if st.session_state.q_index > 0:
        if st.button("⬅️ Previous / السابق"):
            prev_question()
            st.rerun()
with c3:
    if st.session_state.q_index < len(questions) - 1:
        if st.button("Next / التالي ➡️"):
            next_question()
            st.rerun()
