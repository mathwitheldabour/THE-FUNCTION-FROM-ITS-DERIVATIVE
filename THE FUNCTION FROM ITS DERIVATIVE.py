import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import random

# ---------------------------------------------------------
# 1. إعداد الصفحة والتنسيقات (CSS المحسّن)
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="Calculus Quiz")

st.markdown("""
<style>
    .stApp { text-align: center; }
    
    /* تنسيق صندوق السؤال */
    .question-box {
        background-color: #f1f3f6;
        padding: 20px;
        border-radius: 15px;
        border-top: 5px solid #007bff;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* تنسيق الحرف A, B, C */
    .option-letter {
        color: #d63384;
        font-size: 26px;
        font-weight: 800;
        margin-bottom: 5px;
        display: block;
    }

    /* تحسين شكل الأزرار */
    .stButton button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        font-size: 16px;
        padding: 10px;
        transition: all 0.3s ease;
    }
    
    /* أزرار الإجابات (تلقائي) */
    div[data-testid="column"] .stButton button {
        background-color: #ffffff;
        color: #333;
        border: 2px solid #007bff;
    }
    div[data-testid="column"] .stButton button:hover {
        background-color: #007bff;
        color: white;
        border-color: #007bff;
        transform: translateY(-2px);
    }

    /* أزرار التنقل (السابق/التالي) */
    .nav-btn .stButton button {
        background-color: #6c757d; 
        color: white;
        border: none;
    }
    .nav-btn .stButton button:hover {
        background-color: #5a6268;
    }
    
    /* رسالة النتيجة */
    .result-box {
        padding: 15px;
        border-radius: 10px;
        margin-top: 20px;
        font-size: 18px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. إدارة الحالة
# ---------------------------------------------------------
if 'q_index' not in st.session_state:
    st.session_state.q_index = 0
if 'answered' not in st.session_state:
    st.session_state.answered = False
if 'selected_opt' not in st.session_state:
    st.session_state.selected_opt = None

# دوال التنقل مع تصفير الحالة للإجابة الجديدة
def next_question():
    if st.session_state.q_index < len(questions) - 1:
        st.session_state.q_index += 1
        st.session_state.answered = False
        st.session_state.selected_opt = None

def prev_question():
    if st.session_state.q_index > 0:
        st.session_state.q_index -= 1
        st.session_state.answered = False
        st.session_state.selected_opt = None

def check_answer(option):
    st.session_state.selected_opt = option
    st.session_state.answered = True

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
    ax.plot(x, y, color='#007bff', linewidth=2.5)
    ax.text(x_range[1]*0.8, y_range[1]*0.8, "y = f'(x)", fontsize=12, color='#007bff', fontweight='bold')
    ax.set_ylim(y_range)
    ax.set_xlim(x_range)
    plt.tight_layout()
    return fig

# ---------------------------------------------------------
# 4. البيانات
# ---------------------------------------------------------
def q1_deriv(x): return -x + 1 
def q2_deriv(x): return 0.5*(x-1)*(3-x) 
def q3_deriv(x): return 0.2*(x+1)*(x-2)**2 
def q4_deriv(x): return 0.5*(x+1)*(x-2)*(x-4) 

questions = [
    {
        "id": 1,
        "func": q1_deriv,
        "q_en": "From the graph of $f'(x)$, determine the local extrema.",
        "q_ar": "من رسم المشتقة $f'(x)$، حدد القيم القصوى المحلية.",
        "options": [
            {"code": "A", "en": r"Local Max at $x=1$", "ar": r"قيمة عظمى محلية عند $x=1$", "correct": True},
            {"code": "B", "en": r"Local Min at $x=1$", "ar": r"قيمة صغرى محلية عند $x=1$", "correct": False},
            {"code": "C", "en": r"Local Max at $x=0$", "ar": r"قيمة عظمى محلية عند $x=0$", "correct": False},
            {"code": "D", "en": r"No local extrema", "ar": r"لا توجد قيم قصوى محلية", "correct": False},
        ]
    },
    {
        "id": 2,
        "func": q2_deriv,
        "q_en": "Identify the intervals of decrease for $f(x)$.",
        "q_ar": "حدد فترات التناقص للدالة $f(x)$.",
        "options": [
            {"code": "A", "en": r"Decrease on $(-\infty, 1) \cup (3, \infty)$", "ar": r"متناقصة في $(-\infty, 1) \cup (3, \infty)$", "correct": True},
            {"code": "B", "en": r"Decrease on $(1, 3)$", "ar": r"متناقصة في الفترة $(1, 3)$", "correct": False},
            {"code": "C", "en": r"Increase on $(-\infty, 1)$", "ar": r"متزايدة في الفترة $(-\infty, 1)$", "correct": False},
            {"code": "D", "en": r"Decrease on $(3, \infty)$ only", "ar": r"متناقصة في $(3, \infty)$ فقط", "correct": False},
        ]
    },
    {
        "id": 3,
        "func": q3_deriv,
        "q_en": "Analyze the critical point at $x=2$.",
        "q_ar": "حلل النقطة الحرجة عند $x=2$.",
        "options": [
            {"code": "A", "en": r"Saddle Point (Inflection)", "ar": r"نقطة سرج (انقلاب)", "correct": True},
            {"code": "B", "en": r"Local Maximum", "ar": r"قيمة عظمى محلية", "correct": False},
            {"code": "C", "en": r"Local Minimum", "ar": r"قيمة صغرى محلية", "correct": False},
            {"code": "D", "en": r"Cusp (Sharp corner)", "ar": r"رأس حاد (Cusp)", "correct": False},
        ]
    }
]

# ---------------------------------------------------------
# 5. العرض
# ---------------------------------------------------------

q_idx = st.session_state.q_index
q = questions[q_idx]

st.progress((q_idx + 1) / len(questions))

# 1. السؤال
st.markdown(f"""
<div class="question-box">
    <div style="text-align: left; direction: ltr; font-weight: bold; color: #0056b3; font-size: 18px;">Q{q_idx+1}: {q['q_en']}</div>
    <div style="text-align: right; direction: rtl; font-weight: bold; color: #0056b3; font-size: 20px; margin-top: 10px;">س{q_idx+1}: {q['q_ar']}</div>
</div>
""", unsafe_allow_html=True)

# 2. الرسم البياني
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.pyplot(plot_derivative(q['func']))

st.write("---")
st.markdown("##### اختر الإجابة الصحيحة / Select your answer:")

# 3. عرض الخيارات (كل خيار يحتوي زر اختيار بداخله)
random.seed(q_idx + 42)
current_opts = q['options'].copy()
random.shuffle(current_opts)
letters = ['A', 'B', 'C', 'D']
option_map = {}

cols = st.columns(4)

for idx, col in enumerate(cols):
    opt = current_opts[idx]
    display_letter = letters[idx]
    option_map[display_letter] = opt
    
    with col:
        # حاوية البطاقة
        with st.container(border=True):
            st.markdown(f"<span class='option-letter'>{display_letter}</span>", unsafe_allow_html=True)
            st.markdown(opt['en'])
            st.markdown("---")
            st.markdown(f"{opt['ar']}")
            
            # --- التغيير الجوهري هنا ---
            # وضعنا الزر داخل البطاقة مباشرة
            if st.button(f"Select {display_letter}", key=f"btn_{q_idx}_{display_letter}"):
                check_answer(display_letter)

# 4. عرض النتيجة (بدون الحاجة لزر تحقق منفصل)
if st.session_state.answered:
    selected_letter = st.session_state.selected_opt
    chosen_opt = option_map[selected_letter]
    
    st.write("")
    if chosen_opt['correct']:
        st.success(f"✅ Correct! الإجابة ({selected_letter}) صحيحة.", icon="✅")
        st.balloons()
    else:
        st.error(f"❌ Incorrect. لقد اخترت ({selected_letter}) وهي إجابة خاطئة.", icon="❌")
        # عرض الإجابة الصحيحة
        correct_letter = [k for k, v in option_map.items() if v['correct']][0]
        st.info(f"الإجابة الصحيحة هي: **{correct_letter}**")

st.markdown("---")

# 5. أزرار التنقل (بتصميم مختلف)
col_prev, col_sp, col_next = st.columns([1, 2, 1])

# كلاس CSS مخصص لأزرار التنقل
with col_prev:
    st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
    if st.session_state.q_index > 0:
        if st.button("⬅️ Previous / السابق"):
            prev_question()
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col_next:
    st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
    if st.session_state.q_index < len(questions) - 1:
        if st.button("Next / التالي ➡️"):
            next_question()
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
