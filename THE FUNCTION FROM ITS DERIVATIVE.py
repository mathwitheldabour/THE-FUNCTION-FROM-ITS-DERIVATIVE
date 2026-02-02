import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import random

# ---------------------------------------------------------
# 1. إعداد الصفحة والتنسيقات
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="Calculus Quiz: Derivative to Function")

st.markdown("""
<style>
    .stApp { direction: rtl; }
    h1, h2, h3, p, div { text-align: right; }
    .katex-display, .katex { direction: ltr; text-align: center; }
    .stRadio > div { direction: rtl; text-align: right; }
    .question-box {
        background-color: #e3f2fd; /* لون أزرق فاتح للسؤال */
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-right: 5px solid #1565c0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center; /* توسيط الرسم في السؤال */
    }
    .question-text-ar { font-size: 22px; font-weight: bold; color: #1565c0; margin-bottom: 15px; text-align: right; }
    .question-text-en { font-size: 16px; color: #546e7a; font-family: sans-serif; direction: ltr; text-align: left; margin-bottom: 10px;}
    .stButton button { width: 100%; font-weight: bold; font-size: 18px; }
    
    /* تنسيق خاص لعنوان الرسم */
    .plot-title {
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
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
# 3. دوال الرسم البياني
# ---------------------------------------------------------

def plot_derivative_graph(func_prime, x_range=(-5, 5), y_range=(-5, 5)):
    """
    رسم دالة المشتقة (السؤال)
    """
    x = np.linspace(x_range[0], x_range[1], 1000)
    y = func_prime(x)
    
    fig, ax = plt.subplots(figsize=(6, 3)) # حجم مختلف قليلاً للسؤال
    
    # تنسيق المحاور
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.grid(True, which='both', linestyle=':', alpha=0.6)
    
    # رسم المشتقة بلون مميز (برتقالي مثلاً أو أحمر للدلالة على أنها f')
    ax.plot(x, y, color='#d32f2f', linewidth=2.5, label="f'(x)")
    
    # إضافة نص توضيحي على الرسم
    ax.text(x_range[1]*0.8, y_range[1]*0.8, "y = f'(x)", fontsize=12, color='#d32f2f', fontweight='bold')

    ax.set_ylim(y_range)
    ax.set_xlim(x_range)
    plt.tight_layout()
    return fig

def plot_original_graph(func, x_range=(-5, 5), y_range=(-5, 5), title=""):
    """
    رسم الدالة الأصلية (الخيارات)
    """
    x = np.linspace(x_range[0], x_range[1], 1000)
    y = func(x)
    
    fig, ax = plt.subplots(figsize=(4, 3))
    
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(2)) # تقليل زحمة الأرقام الصادية
    ax.grid(True, which='both', linestyle=':', alpha=0.5)
    
    # رسم الدالة الأصلية بلون أزرق
    ax.plot(x, y, color='#1976d2', linewidth=2)
    
    ax.set_ylim(y_range)
    ax.set_xlim(x_range)
    ax.set_title(title, fontsize=12, loc='right', color='black', fontweight='bold')
    plt.tight_layout()
    return fig

# ---------------------------------------------------------
# 4. بيانات الأسئلة (f' vs f)
# ---------------------------------------------------------
# ملاحظة: الدوال f يجب أن تكون تكامل f'

# --- Q1: Linear f'(x) ---
# f'(x) = 2 - x (Zero at 2, Pos < 2, Neg > 2)
# f(x) = 2x - 0.5x^2 (Parabola opening down, Vertex at 2)
def q1_deriv(x): return 2 - x
def q1_func(x): return 2*x - 0.5*x**2
# Trap: Parabola opening up (confusing inc/dec)
def q1_trap_up(x): return 0.5*x**2 - 2*x 
# Trap: Vertex shifted (ignoring the root location)
def q1_trap_shift(x): return 2*(x+2) - 0.5*(x+2)**2
# Trap: Using the derivative graph itself as the answer
def q1_trap_deriv(x): return 2 - x 

# --- Q2: Parabola f'(x) ---
# f'(x) = 1 - (x-1)^2 (Roots at 0 and 2). Pos in (0,2). Neg elsewhere.
# f(x) = x - (x-1)^3/3 (Cubic). Dec -> Min(0) -> Inc -> Max(2) -> Dec.
def q2_deriv(x): return 3 - 3*(x-1)**2  # Scaled for visibility
def q2_func(x): return 3*x - (x-1)**3 - 1 # Adjusted constant for visual
# Trap: Reversed Max/Min (Inc outside, Dec inside)
def q2_trap_reverse(x): return -(3*x - (x-1)**3) 
# Trap: f increasing where f' is increasing (Common misconception)
# f' increases (-inf, 1), decreases (1, inf). So student picks parabola-like shape for f.
def q2_trap_slope(x): return 3 - 3*(x-1)**2 
# Trap: Wrong roots/extremes (shifted)
def q2_trap_shift(x): return 3*(x-2) - (x-3)**3

# --- Q3: Touching Root f'(x) ---
# f'(x) = (x+1)(x-2)^2. Roots -1 (cross), 2 (touch).
# Signs: (-) * (+) = (-) for x<-1. (+) * (+) = (+) for -1<x<2. (+) * (+) = (+) for x>2.
# Behavior: Dec -> Min(-1) -> Inc -> Inflection(2) -> Inc.
def q3_deriv(x): return 0.5 * (x+1) * (x-2)**2
def q3_func(x): 
    # Integral approx: 0.5 * integral(x^3 - 3x^2 + 4) -> 0.125 x^4 - 0.5 x^3 + 2x
    return 0.125*x**4 - 0.5*x**3 + 2*x + 1
# Trap: Max at 2 (treating touch as cross) -> Dec-Inc-Dec
def q3_trap_max(x): return -0.125*x**4 + 0.5*x**3 - 2*x 
# Trap: Min at 2 (Standard W shape quartic)
def q3_trap_w(x): return 0.2*(x+1)**2 * (x-2)**2 
# Trap: Just increasing everywhere
def q3_trap_inc(x): return x + 1

# --- Q4: Cubic f'(x) (3 roots) ---
# f'(x) goes Neg -> Pos -> Neg. Roots -1, 3.
# Let's match Image 22 style: Parabola f'. 
# Let's try Image 23 style: Cubic f'. Roots approx -1.2, 1.5, 3.5?
# Let's simpler: Roots -2, 0, 2.
# f'(x) = -x(x-2)(x+2) = -x(x^2-4) = -x^3 + 4x.
# Signs: Pos (x<-2), Neg (-2,0), Pos (0,2), Neg (x>2).
# f(x): Inc -> Max(-2) -> Dec -> Min(0) -> Inc -> Max(2) -> Dec. (M shape).
def q4_deriv(x): return -0.5*x*(x-2)*(x+2)
def q4_func(x): return -0.125*x**4 + 0.5*x**2 # W or M shape.
# Wait, integral of -x^3 + 4x is -x^4/4 + 2x^2. 
# At x= large, -x^4 -> -inf. So Ends down. M shape.
# Trap: W shape (Reversed signs)
def q4_trap_w(x): return 0.125*x**4 - 0.5*x**2 
# Trap: f follows f' (Cubic shape)
def q4_trap_cubic(x): return -0.5*x*(x-2)*(x+2)
# Trap: One extrema only
def q4_trap_para(x): return -(x)**2 + 4

questions = [
    {
        "id": 1,
        "title_ar": "تحليل الدالة الخطية",
        "deriv_func": q1_deriv,
        "correct": q1_func,
        "distractors": [q1_trap_up, q1_trap_shift, q1_trap_deriv]
    },
    {
        "id": 2,
        "title_ar": "تحليل الدالة التربيعية",
        "deriv_func": q2_deriv,
        "correct": q2_func,
        "distractors": [q2_trap_reverse, q2_trap_slope, q2_trap_shift]
    },
    {
        "id": 3,
        "title_ar": "نقطة الانقلاب الأفقية",
        "deriv_func": q3_deriv,
        "correct": q3_func,
        "distractors": [q3_trap_max, q3_trap_w, q3_trap_inc]
    },
    {
        "id": 4,
        "title_ar": "تعدد النقاط الحرجة",
        "deriv_func": q4_deriv,
        "correct": q4_func,
        "distractors": [q4_trap_w, q4_trap_cubic, q4_trap_para]
    }
]

# ---------------------------------------------------------
# 5. عرض التطبيق
# ---------------------------------------------------------

q_idx = st.session_state.q_index
q = questions[q_idx]

progress = (q_idx + 1) / len(questions)
st.progress(progress)

# --- قسم السؤال (رسم المشتقة) ---
st.markdown(f"""
<div class="question-box">
    <div class="question-text-ar">بناءً على الرسم البياني لدالة المشتقة الأولى $f'(x)$ الموضح أدناه:</div>
    <div class="question-text-en">Given the graph of the derivative $f'(x)$ below:</div>
    <p style="direction:rtl; color:#333;">استنتج سلوك الدالة الأصلية $f(x)$ (فترات التزايد والتناقص، والقيم القصوى).</p>
</div>
""", unsafe_allow_html=True)

# عرض رسم المشتقة في المنتصف
col_q_left, col_q_center, col_q_right = st.columns([1, 2, 1])
with col_q_center:
    st.pyplot(plot_derivative_graph(q['deriv_func']))
    st.caption("رسم دالة المشتقة $y = f'(x)$")

st.markdown("---")
st.subheader("أي من الأشكال التالية يمثل الدالة الأصلية $y = f(x)$؟")

# --- تجهيز الخيارات (رسم الدالة الأصلية) ---
random.seed(q['id'] + 2024) 

options_data = []
options_data.append({"type": "correct", "fig": plot_original_graph(q["correct"], title="الإجابة الصحيحة")})
for dist in q["distractors"]:
    options_data.append({"type": "wrong", "fig": plot_original_graph(dist)})

random.shuffle(options_data)

# --- عرض الخيارات ---
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
cols_list = [col1, col2, col3, col4]
letters = ['A', 'B', 'C', 'D']
correct_letter = None

for idx, opt_data in enumerate(options_data):
    letter = letters[idx]
    with cols_list[idx]:
        opt_data["fig"].axes[0].set_title(f"({letter})", loc='left', fontsize=14)
        st.pyplot(opt_data["fig"])
        if opt_data["type"] == "correct":
            correct_letter = letter

# --- منطقة الإجابة ---
st.markdown("---")
col_input, col_action = st.columns([2, 1])

with col_input:
    user_answer = st.radio("اختر الرسم البياني المطابق للدالة الأصلية:", letters, key=f"radio_{q['id']}", horizontal=True)

with col_action:
    st.write("") 
    st.write("") 
    check_btn = st.button("تحقق من الإجابة", key=f"check_{q['id']}")

if check_btn:
    if user_answer == correct_letter:
        st.success(f"✅ أحسنت! الرسم ({correct_letter}) هو الصحيح.")
        st.balloons()
    else:
        st.error(f"❌ إجابة خاطئة. الإجابة الصحيحة هي ({correct_letter}).")
        with st.expander("تلميح للحل"):
            st.info("""
            **كيف تفكر في الحل؟**
            1. انظر إلى إشارة $f'(x)$:
               - إذا كانت $f'$ فوق المحور ($+$)، فالدالة $f$ **تتزايد** ↗️.
               - إذا كانت $f'$ تحت المحور ($-$)، فالدالة $f$ **تتناقص** ↘️.
            2. انظر إلى أصفار $f'$ (نقاط التقاطع مع محور السينات):
               - هذه هي النقاط الحرجة (عظمى أو صغرى) للدالة $f$.
               - (موجب $\\to$ سالب) تعني قمة عظمى.
               - (سالب $\\to$ موجب) تعني قاع أصغر.
            """)

# --- التنقل ---
st.markdown("---")
c1, c2, c3 = st.columns([1, 2, 1])
with c1:
    if st.session_state.q_index > 0:
        if st.button("⬅️ السابق"): prev_question(); st.rerun()
with c3:
    if st.session_state.q_index < len(questions) - 1:
        if st.button("التالي ➡️"): next_question(); st.rerun()