import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import random

# ---------------------------------------------------------
# 1. Page Config & CSS Styling
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="Derivative Analysis Quiz")

st.markdown("""
<style>
    /* Default: RTL for Arabic instructions */
    .stApp { direction: rtl; }
    
    h1, h2, h3, p, div { text-align: right; }
    
    /* Box for the question graph */
    .question-box {
        background-color: #e3f2fd;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-right: 5px solid #1565c0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    /* Force LTR for Radio Options (The Answers) */
    .stRadio > div {
        direction: ltr !important;
        text-align: left !important;
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
    }
    
    /* Style for the radio labels to ensure Math looks good */
    div[data-testid="stMarkdownContainer"] > p {
        font-size: 16px;
        font-family: 'Times New Roman', Times, serif;
    }
    
    .stButton button { width: 100%; font-weight: bold; font-size: 18px; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. Session State
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
# 3. Plotting Function (For the Derivative Stimulus)
# ---------------------------------------------------------
def plot_derivative(func_prime, x_range=(-4, 5), y_range=(-4, 5), title=""):
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
    
    # Plot f'(x) in Red
    ax.plot(x, y, color='#d32f2f', linewidth=2.5, label="f'(x)")
    ax.text(x_range[1]*0.8, y_range[1]*0.8, "y = f'(x)", fontsize=12, color='#d32f2f', fontweight='bold')
    
    ax.set_ylim(y_range)
    ax.set_xlim(x_range)
    plt.tight_layout()
    return fig

# ---------------------------------------------------------
# 4. Question Data
# ---------------------------------------------------------

# Q1: Linear Derivative (Line crossing at x=1)
# f'(x) = -x + 1. Zero at 1. Pos for x<1, Neg for x>1.
# f(x): Inc (-inf, 1), Dec (1, inf). Local Max at x=1.
def q1_deriv(x): return -x + 1

# Q2: Parabola Derivative (Roots at 1 and 3)
# f'(x) = -(x-1)(x-3). Zero at 1, 3.
# Signs: Neg (x<1), Pos (1<x<3), Neg (x>3).
# f(x): Dec (-inf, 1), Inc (1, 3), Dec (3, inf). Min at 1, Max at 3.
def q2_deriv(x): return -0.8*(x-1)*(x-3)

# Q3: Cubic-like Derivative (Touch at -1, Cross at 2)
# f'(x) = 0.5(x+1)^2(x-2). Roots -1, 2.
# Signs: (-) * (-) = (-) for x<-1. (+) * (-) = (-) for -1<x<2. (+) * (+) = (+) for x>2.
# f(x): Dec (-inf, 2), Inc (2, inf). Saddle at -1. Min at 2.
def q3_deriv(x): return 0.2*(x+1)**2 * (x-2)

# Q4: Line crossing origin positively
# f'(x) = x. Zero at 0. Neg x<0, Pos x>0.
# f(x): Dec (-inf, 0), Inc (0, inf). Min at 0.
def q4_deriv(x): return x

questions = [
    {
        "id": 1,
        "func": q1_deriv,
        "question_text": "Based on the graph of f'(x) shown above, determine the behavior of f(x).",
        "correct_option": r"Increasing on $(-\infty, 1)$, Decreasing on $(1, \infty)$, Local Max at $x=1$",
        "distractors": [
            r"Decreasing on $(-\infty, 1)$, Increasing on $(1, \infty)$, Local Min at $x=1$", # Reversed
            r"Increasing on $(-\infty, 0)$, Decreasing on $(0, \infty)$, Local Max at $x=0$", # Wrong intercept
            r"Increasing everywhere, Point of Inflection at $x=1$" # Confusing f' slope
        ]
    },
    {
        "id": 2,
        "func": q2_deriv,
        "question_text": "Identify the extrema and intervals of monotonicity for f(x).",
        "correct_option": r"Dec $(-\infty, 1)$, Inc $(1, 3)$, Dec $(3, \infty)$; Min at $x=1$, Max at $x=3$",
        "distractors": [
            r"Inc $(-\infty, 1)$, Dec $(1, 3)$, Inc $(3, \infty)$; Max at $x=1$, Min at $x=3$", # Reversed Signs
            r"Inc $(-\infty, 2)$, Dec $(2, \infty)$; Max at $x=2$", # Confusing vertex of parabola
            r"Dec $(-\infty, 1)$, Dec $(1, 3)$, Dec $(3, \infty)$; No Extrema" # Ignoring crossing
        ]
    },
    {
        "id": 3,
        "func": q3_deriv,
        "question_text": "Analyze the critical points of f(x) given the graph of f'(x).",
        "correct_option": r"Decreasing on $(-\infty, 2)$, Increasing on $(2, \infty)$; Local Min at $x=2$",
        "distractors": [
            r"Local Max at $x=-1$, Local Min at $x=2$", # Treating touch as max
            r"Increasing on $(-\infty, -1)$, Decreasing on $(-1, 2)$; Max at $x=-1$", # Wrong intervals
            r"Increasing everywhere; Points of Inflection at $x=-1$ and $x=2$" # Confusing with f''
        ]
    },
    {
        "id": 4,
        "func": q4_deriv,
        "question_text": "Determine the properties of f(x) from the graph of f'(x).",
        "correct_option": r"Decreasing on $(-\infty, 0)$, Increasing on $(0, \infty)$; Local Min at $x=0$",
        "distractors": [
            r"Increasing on $(-\infty, 0)$, Decreasing on $(0, \infty)$; Local Max at $x=0$",
            r"Increasing on $(-\infty, \infty)$; No local extrema",
            r"Constant on $(-\infty, \infty)$"
        ]
    }
]

# ---------------------------------------------------------
# 5. Rendering
# ---------------------------------------------------------

q_idx = st.session_state.q_index
q = questions[q_idx]

progress = (q_idx + 1) / len(questions)
st.progress(progress)

# Question Area
st.markdown(f"""
<div class="question-box">
    <div style="font-size:20px; font-weight:bold; color:#1565c0; text-align:right; direction:rtl;">
    تمرين {q_idx + 1}: تحليل رسم المشتقة
    </div>
    <p style="text-align:right; direction:rtl;">
    الشكل التالي يمثل منحنى المشتقة الأولى $y = f'(x)$. اختر الوصف الصحيح للدالة الأصلية $f(x)$.
    </p>
</div>
""", unsafe_allow_html=True)

# Plot f'(x)
col_graph_l, col_graph_c, col_graph_r = st.columns([1, 2, 1])
with col_graph_c:
    st.pyplot(plot_derivative(q['func']))

st.markdown("---")

# Options Area (Text Based, LTR)
options = [q['correct_option']] + q['distractors']
random.seed(q_idx + 42)
random.shuffle(options)

# Helper to find which one is correct after shuffle
correct_idx = options.index(q['correct_option'])

# Radio button for choices
selected_option = st.radio(
    "Choose the correct statement / اختر العبارة الصحيحة:",
    options,
    key=f"q_radio_{q_idx}"
)

# Check Answer Button
col_check_l, col_check_r = st.columns([3, 1])
with col_check_r:
    st.write("")
    if st.button("Check Answer / تحقق"):
        if selected_option == q['correct_option']:
            st.success("Correct! ✅")
            st.balloons()
        else:
            st.error("Incorrect ❌")
            st.markdown(f"**Correct Answer:** {q['correct_option']}")

# Navigation
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
