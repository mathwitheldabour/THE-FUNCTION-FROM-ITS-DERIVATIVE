import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import random

# ---------------------------------------------------------
# 1. إعداد الصفحة والتنسيقات
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="Calculus Quiz")

st.markdown("""
<style>
    /* توسيط النصوص */
    .stApp { text-align: center; }
    
    /* تنسيق صندوق السؤال الرئيسي */
    .question-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
        border-top: 5px solid #007bff;
        margin-bottom: 30px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* تنسيق الحرف A, B, C */
    .option-letter {
        color: #e83e8c;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    /* ضبط حجم الأزرار */
    .stButton button {
        width: 40%;
        margin: 0 auto;
        display: block;
        font-size: 18px;
        background-color: #28a745;
        color: white;
    }
    
    /* تحسين مظهر الراديو */
    div[role="radiogroup"] {
        justify-content: center;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. إدارة الحالة (Session State)
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
    
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.grid(True, which='both', linestyle=':', alpha=0.6)
    
    # رسم الدالة
    ax.plot(x, y, color='#007bff', linewidth=2.5) # لون أزرق مثل الصورة
    ax.text(x_range[1]*0.8, y_range[1]*0.8, "y = f'(x)", fontsize=12, color='#007bff', fontweight='bold')
    
    ax.set_ylim(y_range)
    ax.set_xlim(x_range)
    plt.tight_layout()
    return fig

# ---------------------------------------------------------
# 4. بيانات الأسئلة (استخدام r"..." للمعادلات)
# ---------------------------------------------------------

# الدوال
def q1_deriv(x): return -x + 1  # خطي
def q2_deriv(x): return 0.5*(x-1)*(3-x) # قطع مكافئ مقلوب (موجب بين 1 و 3)
def q3_deriv(x): return 0.2*(x+1)*(x-2)**2 # يقطع عند -1 ويمس عند 2
def q4_deriv(x): return 0.5*(x+1)*(x-2)*(x-4) # تكعيبي 

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
        # الرسم 22: قطع مكافئ مقلوب، موجب بين 1 و 3
        # دالة f تتزايد في (1,3) وتتناقص خارجها
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
        # الرسم 24 تقريباً: يقطع عند -1، يمس عند 2
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
# 5. العرض والتصميم
# ---------------------------------------------------------

q_idx = st.session_state.q_index
q = questions[q_idx]

# شريط التقدم
st.progress((q_idx + 1) / len(questions))

# 1. صندوق السؤال
st.markdown(f"""
<div class="question-box">
    <div style="text-align: left; direction: ltr; font-weight: bold; color: #0056b3; font-size: 18px;">Q{q_idx+1}: {q['q_en']}</div>
    <div style="text-align: right; direction: rtl; font-weight: bold; color: #0056b3; font-size: 20px; margin-top: 10px;">س{q_idx+1}: {q['q_ar']}</div>
</div>
""", unsafe_allow_html=True)

# 2. الرسم البياني (في المنتصف)
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.pyplot(plot_derivative(q['func']))

st.write("---")

# 3. عرض الخيارات (باستخدام الحاويات Native Containers)
# هذه الطريقة تضمن ظهور المعادلات بشكل صحيح لأننا لا نستخدم HTML للنصوص

random.seed(q_idx + 42)
current_opts = q['options'].copy()
random.shuffle(current_opts)
letters = ['A', 'B', 'C', 'D']

# إنشاء 4 أعمدة للخيارات
cols = st.columns(4)

# حفظ ترتيب الإجابات لزر الراديو
option_map = {} 

for idx, col in enumerate(cols):
    opt = current_opts[idx]
    display_letter = letters[idx]
    
    # حفظ الرابط بين الحرف والخيار
    option_map[display_letter] = opt
    
    with col:
        # إنشاء بطاقة بحدود (Native Streamlit Container)
        with st.container(border=True):
            # 1. الحرف A, B, C...
            st.markdown(f":pink[**{display_letter}**]")
            
            # 2. النص الإنجليزي (يسار)
            # Streamlit ينسق المعادلات تلقائياً هنا
            st.markdown(opt['en'])
            
            # 3. فاصل
            st.markdown("---")
            
            # 4. النص العربي (يمين)
            # نستخدم Markdown عادي لضمان ظهور المعادلات، ونتركه محاذاة لليسار للحفاظ على تنسيق المعادلة
            # أو يمكننا كتابة النص العربي ببساطة
            st.markdown(f"{opt['ar']}")

# 4. زر الاختيار
selection = st.radio(
    "Choose your answer / اختر إجابتك:",
    letters,
    horizontal=True,
    label_visibility="collapsed"
)

# 5. التحقق
st.write("")
check = st.button("Check Answer / تحقق من الإجابة")

if check:
    chosen_opt = option_map[selection]
    
    if chosen_opt['correct']:
        st.success(f"✅ Correct! الإجابة ({selection}) صحيحة.")
        st.balloons()
    else:
        st.error(f"❌ Incorrect. إجابة خاطئة.")
        
        # البحث عن الإجابة الصحيحة
        correct_letter = [k for k, v in option_map.items() if v['correct']][0]
        correct_content = option_map[correct_letter]
        
        st.info(f"The correct answer is **{correct_letter}**:\n\n"
                f"{correct_content['en']}\n\n"
                f"{correct_content['ar']}")

st.markdown("---")

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
