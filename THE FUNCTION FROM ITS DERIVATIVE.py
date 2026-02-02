import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import random

# ---------------------------------------------------------
# 1. إعداد الصفحة والتنسيقات (CSS)
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="Calculus Infinite Quiz")

st.markdown("""
<style>
    .stApp { text-align: center; }
    
    /* تنسيق صندوق السؤال */
    .question-box {
        background-color: #f8f9fa;
        padding: 25px;
        border-radius: 15px;
        border-top: 6px solid #007bff;
        margin-bottom: 25px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    
    /* تنسيق النصوص داخل السؤال */
    .q-en {
        text-align: left;
        direction: ltr;
        font-size: 18px;
        color: #0056b3;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .q-ar {
        text-align: right;
        direction: rtl;
        font-size: 20px;
        color: #0056b3;
        font-weight: 700;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* تنسيق المعادلات داخل النصوص العربية */
    .math-text {
        direction: ltr;
        display: inline-block;
        font-weight: bold;
        color: #d63384;
    }

    /* تنسيق البطاقات (الخيارات) */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
        gap: 1rem;
    }
    
    /* النصوص داخل بطاقة الاختيار */
    .opt-en {
        text-align: left;
        direction: ltr;
        font-size: 16px;
        color: #333;
        margin-bottom: 8px;
    }
    .opt-ar {
        text-align: right;
        direction: rtl;
        font-size: 18px;
        color: #444;
        border-top: 1px solid #eee;
        padding-top: 8px;
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* حرف الاختيار */
    .opt-letter {
        font-size: 22px;
        font-weight: 900;
        color: #007bff;
        margin-bottom: 5px;
        display: block;
        text-align: center;
    }

    /* أزرار الإجابة */
    .stButton button {
        width: 100%;
        border-radius: 8px;
        transition: 0.3s;
    }
    div[data-testid="column"] .stButton button:hover {
        background-color: #007bff;
        color: white;
        border-color: #007bff;
        transform: scale(1.02);
    }
    
    /* زر محاولة جديدة */
    .new-quiz-btn button {
        background-color: #28a745 !important;
        color: white !important;
        font-size: 20px !important;
        padding: 15px !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. مولد الأسئلة الذكي (Logic Generator)
# ---------------------------------------------------------

def generate_linear_question():
    """توليد سؤال لدالة مشتقة خطية: f'(x) = a(x-r)"""
    r = random.randint(-3, 3) # الجذر
    slope = random.choice([-1, 1]) # الميل
    
    # تعريف دالة المشتقة للرسم
    def func_prime(x): return slope * (x - r)
    
    # تحديد الإجابة الصحيحة
    if slope > 0: # المشتقة كانت سالبة ثم موجبة (صغرى)
        correct_en = rf"Dec on $(-\infty, {r})$, Inc on $({r}, \infty)$; Min at $x={r}$"
        correct_ar = rf"تناقص $(-\infty, {r})$، تزايد $({r}, \infty)$؛ صغرى عند $x={r}$"
        # مشتتات
        d1_en = rf"Inc on $(-\infty, {r})$, Dec on $({r}, \infty)$; Max at $x={r}$"
        d1_ar = rf"تزايد $(-\infty, {r})$، تناقص $({r}, \infty)$؛ عظمى عند $x={r}$"
    else: # المشتقة كانت موجبة ثم سالبة (عظمى)
        correct_en = rf"Inc on $(-\infty, {r})$, Dec on $({r}, \infty)$; Max at $x={r}$"
        correct_ar = rf"تزايد $(-\infty, {r})$، تناقص $({r}, \infty)$؛ عظمى عند $x={r}$"
        # مشتتات
        d1_en = rf"Dec on $(-\infty, {r})$, Inc on $({r}, \infty)$; Min at $x={r}$"
        d1_ar = rf"تناقص $(-\infty, {r})$، تزايد $({r}, \infty)$؛ صغرى عند $x={r}$"
        
    return {
        "func": func_prime,
        "q_en": r"Determine the local extrema from the graph of $f'(x)$.",
        "q_ar": r"حدد القيم القصوى المحلية من رسم المشتقة $f'(x)$.",
        "correct": {"en": correct_en, "ar": correct_ar},
        "distractors": [
            {"en": d1_en, "ar": d1_ar},
            {"en": rf"No local extrema; Inflection at $x={r}$", "ar": rf"لا توجد قيم قصوى؛ نقطة انقلاب عند $x={r}$"},
            {"en": rf"Local Max at $x=0$", "ar": rf"قيمة عظمى محلية عند $x=0$"}
        ]
    }

def generate_quadratic_question():
    """توليد سؤال لدالة تربيعية: f'(x) = a(x-r1)(x-r2)"""
    roots = sorted(random.sample(range(-3, 4), 2))
    r1, r2 = roots[0], roots[1]
    a = random.choice([-0.5, 0.5]) # التقعر
    
    def func_prime(x): return a * (x - r1) * (x - r2)
    
    if a > 0: # + (Inc) -> r1 -> - (Dec) -> r2 -> + (Inc)
        correct_en = rf"Max at $x={r1}$, Min at $x={r2}$"
        correct_ar = rf"عظمى عند $x={r1}$، صغرى عند $x={r2}$"
        d1_en = rf"Min at $x={r1}$, Max at $x={r2}$"
        d1_ar = rf"صغرى عند $x={r1}$، عظمى عند $x={r2}$"
    else: # - (Dec) -> r1 -> + (Inc) -> r2 -> - (Dec)
        correct_en = rf"Min at $x={r1}$, Max at $x={r2}$"
        correct_ar = rf"صغرى عند $x={r1}$، عظمى عند $x={r2}$"
        d1_en = rf"Max at $x={r1}$, Min at $x={r2}$"
        d1_ar = rf"عظمى عند $x={r1}$، صغرى عند $x={r2}$"

    return {
        "func": func_prime,
        "q_en": r"Identify the local extrema for $f(x)$.",
        "q_ar": r"حدد القيم القصوى المحلية للدالة $f(x)$.",
        "correct": {"en": correct_en, "ar": correct_ar},
        "distractors": [
            {"en": d1_en, "ar": d1_ar},
            {"en": rf"Max at $x={(r1+r2)/2}$ (Vertex)", "ar": rf"عظمى عند رأس القطع $x={(r1+r2)/2}$"},
            {"en": rf"Decreasing everywhere", "ar": rf"متناقصة على مجالها"}
        ]
    }

def generate_touching_question():
    """توليد سؤال لجذر مكرر (يمس المحور): f'(x) = a(x-r)^2"""
    r = random.randint(-2, 2)
    a = random.choice([-0.3, 0.3])
    
    def func_prime(x): return a * (x - r)**2
    
    # الإشارة لا تتغير حول الجذر (موجب-موجب أو سالب-سالب)
    correct_en = rf"No extrema (Inflection Point at $x={r}$)"
    correct_ar = rf"لا توجد قيم قصوى (نقطة انقلاب عند $x={r}$)"
    
    return {
        "func": func_prime,
        "q_en": r"Analyze the critical point at the root.",
        "q_ar": r"حلل النقطة الحرجة عند الجذر.",
        "correct": {"en": correct_en, "ar": correct_ar},
        "distractors": [
            {"en": rf"Local Maximum at $x={r}$", "ar": rf"قيمة عظمى محلية عند $x={r}$"},
            {"en": rf"Local Minimum at $x={r}$", "ar": rf"قيمة صغرى محلية عند $x={r}$"},
            {"en": rf"Vertical Asymptote at $x={r}$", "ar": rf"خط تقارب رأسي عند $x={r}$"}
        ]
    }

def generate_quiz():
    """توليد اختبار جديد مكون من 4 أسئلة عشوائية"""
    q1 = generate_linear_question()
    q2 = generate_quadratic_question()
    q3 = generate_touching_question()
    # يمكن إضافة نوع رابع أو تكرار نوع بمعاملات مختلفة
    q4 = generate_linear_question() 
    
    # خلط ترتيب أنواع الأسئلة
    quiz = [q1, q2, q3, q4]
    random.shuffle(quiz)
    return quiz

# ---------------------------------------------------------
# 3. إدارة الحالة (Session State)
# ---------------------------------------------------------
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = generate_quiz()
if 'q_index' not in st.session_state:
    st.session_state.q_index = 0
if 'answered' not in st.session_state:
    st.session_state.answered = False
if 'selected_opt' not in st.session_state:
    st.session_state.selected_opt = None

def reset_quiz():
    st.session_state.quiz_data = generate_quiz()
    st.session_state.q_index = 0
    st.session_state.answered = False
    st.session_state.selected_opt = None

def check_answer(code):
    st.session_state.selected_opt = code
    st.session_state.answered = True

def next_question():
    if st.session_state.q_index < len(st.session_state.quiz_data) - 1:
        st.session_state.q_index += 1
        st.session_state.answered = False
        st.session_state.selected_opt = None

def prev_question():
    if st.session_state.q_index > 0:
        st.session_state.q_index -= 1
        st.session_state.answered = False
        st.session_state.selected_opt = None

# ---------------------------------------------------------
# 4. دالة الرسم البياني
# ---------------------------------------------------------
def plot_derivative(func_prime, x_range=(-5, 5), y_range=(-5, 5)):
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
# 5. العرض (UI Rendering)
# ---------------------------------------------------------

# جلب بيانات السؤال الحالي
current_quiz = st.session_state.quiz_data
q_idx = st.session_state.q_index
q_data = current_quiz[q_idx]

# شريط التقدم
st.progress((q_idx + 1) / len(current_quiz))

# 1. صندوق السؤال
st.markdown(f"""
<div class="question-box">
    <div class="q-en">Q{q_idx+1}: {q_data['q_en']}</div>
    <div class="q-ar">س{q_idx+1}: {q_data['q_ar']}</div>
</div>
""", unsafe_allow_html=True)

# 2. الرسم البياني
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.pyplot(plot_derivative(q_data['func']))

st.write("---")

# 3. تجهيز الخيارات (خلط عشوائي)
# نستخدم random.seed مرتبط برقم السؤال والبيانات لضمان ثبات الخيارات أثناء التفاعل
seed_val = q_idx + int(q_data['func'](0)*100) # seed فريد لكل سؤال مولد
random.seed(seed_val)

options_list = []
# إضافة الصحيح
options_list.append({**q_data['correct'], "is_correct": True})
# إضافة المشتتات
for dist in q_data['distractors']:
    options_list.append({**dist, "is_correct": False})

random.shuffle(options_list)

# عرض الخيارات
cols = st.columns(4)
letters = ['A', 'B', 'C', 'D']
option_map = {}

for idx, col in enumerate(cols):
    opt = options_list[idx]
    letter = letters[idx]
    option_map[letter] = opt
    
    with col:
        # حاوية البطاقة
        with st.container(border=True):
            st.markdown(f"<span class='opt-letter'>{letter}</span>", unsafe_allow_html=True)
            
            # النص الإنجليزي (يسار)
            st.markdown(f"<div class='opt-en'>{opt['en']}</div>", unsafe_allow_html=True)
            
            # النص العربي (يمين) - لاحظ وضع dir="rtl"
            st.markdown(f"""
            <div class='opt-ar'>
                {opt['ar']}
            </div>
            """, unsafe_allow_html=True)
            
            # زر الاختيار داخل البطاقة
            if st.button(f"Choose {letter}", key=f"btn_{q_idx}_{letter}"):
                check_answer(letter)

# 4. عرض النتيجة
if st.session_state.answered:
    selected = st.session_state.selected_opt
    chosen_data = option_map[selected]
    
    st.write("")
    if chosen_data['is_correct']:
        st.success(f"✅ Correct! الإجابة ({selected}) صحيحة.", icon="✅")
        st.balloons()
    else:
        st.error(f"❌ Incorrect. لقد اخترت ({selected}).", icon="❌")
        # عرض الصحيح
        correct_letter = [k for k, v in option_map.items() if v['is_correct']][0]
        correct_text = option_map[correct_letter]
        st.markdown(f"""
        <div style="background-color:#d4edda; color:#155724; padding:15px; border-radius:10px; direction:rtl; text-align:center;">
            <b>الإجابة الصحيحة هي: {correct_letter}</b><br>
            <span dir="ltr">{correct_text['en']}</span><br>
            {correct_text['ar']}
        </div>
        """, unsafe_allow_html=True)

st.write("---")

# 5. أزرار التنقل والتحكم
c_prev, c_new, c_next = st.columns([1, 2, 1])

with c_prev:
    if q_idx > 0:
        if st.button("⬅️ Previous / السابق"):
            prev_question()
            st.rerun()

with c_next:
    if q_idx < len(current_quiz) - 1:
        if st.button("Next / التالي ➡️"):
            next_question()
            st.rerun()

# زر محاولة جديدة (يظهر في النهاية أو دائماً، حسب التفضيل)
# سنجعله يظهر دائماً في الوسط كخيار لإعادة التوليد
with c_new:
    st.markdown('<div class="new-quiz-btn">', unsafe_allow_html=True)
    if st.button("🔄 New Quiz / محاولة جديدة (أسئلة مختلفة)"):
        reset_quiz()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
