import streamlit as st
import re
import random
from collections import Counter
import plotly.express as px
import plotly.graph_objects as go

# =============== CONFIGURATION ===============
st.set_page_config(
    page_title="Cognify AI",
    page_icon="🧠",
    layout="wide"
)

# SESSION STATE

# =============== SESSION STATE ===============
if "text" not in st.session_state:
    st.session_state.text = ""

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = None

if "history" not in st.session_state:
    st.session_state.history = []

if "flash_index" not in st.session_state:
    st.session_state.flash_index = 0

# =============== PREMIUM CSS ===============
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background:
        radial-gradient(at 10% 10%, #29205b 0%, transparent 40%),
        radial-gradient(at 90% 90%, #172c60 0%, transparent 40%),
        #090d20;
    color: #f5f3ff;
    font-family: 'Inter', sans-serif;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#11152f,#211443);
    border-right: 1px solid #6545a8;
}

h1,h2,h3 {
    color: #ffffff !important;
}

p, label, .stMarkdown {
    color: #d9d5f2;
}

.hero {
    background: linear-gradient(120deg,#32216d,#192c59,#172044);
    padding: 32px;
    border-radius: 22px;
    border: 1px solid #7654d8;
    box-shadow: 0 8px 35px #542bb533;
    margin-bottom: 24px;
}

.hero h1 {
    font-size: 36px;
    font-weight: 800;
}

.hero p {
    color: #d6d0ff;
}

.card {
    background: linear-gradient(145deg,#1b2142,#21183d);
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #51417e;
    min-height: 125px;
    transition: 0.3s;
}

.card:hover {
    border-color: #a78bfa;
    transform: translateY(-3px);
}

.card h2 {
    color: #bba5ff !important;
}

.stButton button,
.stFormSubmitButton button {
    background: linear-gradient(90deg,#873cff,#397bff);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 20px;
    font-weight: 700;
}

.stButton button:hover,
.stFormSubmitButton button:hover {
    background: linear-gradient(90deg,#a45bff,#26c6ff);
    color: white;
}

.stTextArea textarea {
    background: #151b37 !important;
    color: white !important;
    border: 1px solid #7255b7 !important;
    border-radius: 14px !important;
}

.stRadio label {
    background: #202344;
    border: 1px solid #51417e;
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 7px;
}

div[data-testid="stMetric"] {
    background: #1b2142;
    border: 1px solid #51417e;
    border-radius: 14px;
    padding: 16px;
}

hr {
    border-color: #51417e;
}
/* GLOBAL AI VISUAL EFFECTS */

.stApp {
    color: #F5F3FF;
    background: radial-gradient(
        circle at top right,
        #201447,
        #080D20 65%
    );
}

/* Clear headings */
h1, h2, h3 {
    color: #FFFFFF !important;
    font-weight: 800 !important;
    letter-spacing: 0.4px;
}

/* Readable body text */
p, label, li, .stMarkdown {
    color: #E2DDF5;
}

/* Animated gradient headings */
h1 {
    background: linear-gradient(
        90deg, #FFFFFF, #B69CFF, #67E8F9
    );
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: auroraText 5s ease infinite;
}

@keyframes auroraText {
    0% { background-position: 0% center; }
    100% { background-position: 200% center; }
}

/* Glowing cards */
div[data-testid="stMetric"],
div[data-testid="stExpander"] {
    background: rgba(83, 55, 150, 0.18);
    border: 1px solid rgba(174, 145, 255, 0.35);
    border-radius: 16px;
    transition: all 0.3s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    box-shadow: 0 0 22px rgba(139, 92, 246, 0.35);
}

/* Smooth buttons */
.stButton > button {
    border: 1px solid #9575FF;
    border-radius: 12px;
    background: linear-gradient(110deg, #7041FF, #087EA4);
    color: white !important;
    font-weight: 700;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    box-shadow: 0 0 22px #7041FF;
    transform: translateY(-2px);
}

/* Sidebar readability */
section[data-testid="stSidebar"] {
    background: #10152D;
}

section[data-testid="stSidebar"] * {
    color: #F0EBFF;
}

/* AI ambient glow */
.stMain {
    background-image:
        radial-gradient(circle at 85% 15%,
        rgba(112, 65, 255, 0.10), transparent 28%);
}/* Animated AI neural network glow */

@keyframes aiPulse {
    0%, 100% {
        opacity: 0.35;
        transform: scale(1);
    }
    50% {
        opacity: 0.8;
        transform: scale(1.08);
    }
}

[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    top: 15%;
    right: -100px;
    width: 280px;
    height: 280px;
    border-radius: 50%;
    background: radial-gradient(
        circle,
        rgba(112, 65, 255, 0.22),
        transparent 70%
    );
    filter: blur(25px);
    pointer-events: none;
    animation: aiPulse 6s ease-in-out infinite;
    z-index: 0;
}

[data-testid="stAppViewContainer"]::after {
    content: "";
    position: fixed;
    bottom: 5%;
    left: -100px;
    width: 240px;
    height: 240px;
    border-radius: 50%;
    background: radial-gradient(
        circle,
        rgba(0, 198, 255, 0.16),
        transparent 70%
    );
    filter: blur(25px);
    pointer-events: none;
    animation: aiPulse 8s ease-in-out infinite;
    z-index: 0;
}
/* AI BRAIN VISUAL */

.ai-visual {
    position: relative;
    width: 220px;
    height: 220px;
    margin: 25px auto;
    display: flex;
    align-items: center;
    justify-content: center;
}

.ai-core {
    width: 95px;
    height: 95px;
    border-radius: 50%;
    background: linear-gradient(135deg, #7041FF, #00C6FF);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 25px;
    font-weight: 800;
    box-shadow: 0 0 35px #7041FF;
    animation: brainPulse 3s ease-in-out infinite;
}

.ai-orbit {
    position: absolute;
    width: 170px;
    height: 170px;
    border: 2px solid rgba(166, 130, 255, 0.6);
    border-radius: 50%;
    animation: brainRotate 8s linear infinite;
}

.orbit-two {
    width: 210px;
    height: 120px;
    transform: rotate(60deg);
    border-color: rgba(0, 198, 255, 0.6);
}

.ai-node {
    position: absolute;
    color: #67E8F9;
    font-size: 24px;
    animation: brainPulse 2s infinite;
}

.node-one { top: 5px; left: 95px; }
.node-two { bottom: 10px; left: 25px; }
.node-three { bottom: 10px; right: 25px; }

@keyframes brainPulse {
    0%, 100% { transform: scale(1); opacity: 0.7; }
    50% { transform: scale(1.2); opacity: 1; }
}

@keyframes brainRotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
</style>
""", unsafe_allow_html=True)

# =============== NLP FUNCTIONS ===============
STOPWORDS = {
    "the", "is", "are", "was", "were", "a", "an", "and",
    "or", "of", "to", "in", "on", "for", "with", "as",
    "by", "at", "it", "this", "that", "from", "be", "has",
    "have", "had", "which", "what", "who", "when", "where",
    "how", "can", "will", "their", "they", "we", "you",
    "he", "she", "i", "not", "but", "about", "into"
}

def get_words(text):
    return re.findall(r"\b[a-zA-Z]+\b", text.lower())

def get_sentences(text):
    return [
        s.strip() for s in re.split(r'(?<=[.!?])\s+', text.strip())
        if s.strip()
    ]

def extract_keywords(text, limit=10):
    words = [
        w for w in get_words(text)
        if w not in STOPWORDS and len(w) > 2
    ]
    return Counter(words).most_common(limit)

def summarize_text(text, count=3):
    sentences = get_sentences(text)
    if not sentences:
        return ""

    frequencies = Counter(
        w for w in get_words(text)
        if w not in STOPWORDS and len(w) > 2
    )

    scores = {}
    for sentence in sentences:
        words = get_words(sentence)
        scores[sentence] = sum(
            frequencies[w] for w in words
        ) / max(len(words), 1)

    selected = sorted(
        sentences,
        key=lambda s: scores[s],
        reverse=True
    )[:min(count, len(sentences))]

    return " ".join(
        s for s in sentences if s in selected
    )

# =============== SIDEBAR ===============
with st.sidebar:
    st.markdown("# 🧠 Cognify AI")
    st.caption("LEARN • ANALYZE • GROW")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "🏠 Overview",
            "✨ Smart Summarizer",
            "🔑 Key Concepts",
            "🎯 Quiz Generator",
            "📚 Flashcards",
            "📊 Analytics",
            "⚙️ AI Architecture"
        ]
    )

    st.divider()
    st.markdown("### ✨ Learning Assistant")
    st.caption("Your intelligent learning companion.")
    st.caption("Version 2.0")

# =============== OVERVIEW ===============
if page == "🏠 Overview":
    #ai_visual()

    st.markdown("""
    <div class="hero">
        <h1>Welcome to Cognify AI 🧠</h1>
        <p>Your Intelligent Text Analysis and Personalized Learning Assistant</p>
        <p>Transform information into understanding.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Your Learning Workspace")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            '<div class="card"><h2>📝 NLP</h2>'
            '<h3>Text Intelligence</h3>'
            '<p>Analyze and understand text.</p></div>',
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            '<div class="card"><h2>🎯 QUIZ</h2>'
            '<h3>Knowledge Testing</h3>'
            '<p>Test your understanding.</p></div>',
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            '<div class="card"><h2>📚 LEARN</h2>'
            '<h3>Smart Revision</h3>'
            '<p>Review concepts with flashcards.</p></div>',
            unsafe_allow_html=True
        )

    st.divider()
    st.subheader("🧬 How Cognify AI Works")

    steps = st.columns(5)
    workflow = [
        ("01", "Input Text"),
        ("02", "Preprocessing"),
        ("03", "NLP Analysis"),
        ("04", "Knowledge"),
        ("05", "Learning")
    ]

    for col, (number, name) in zip(steps, workflow):
        with col:
            st.markdown(
                f'<div class="card"><h2>{number}</h2>'
                f'<b>{name}</b></div>',
                unsafe_allow_html=True
            )

    st.info(
        "Start by opening Smart Summarizer and entering your study material."
    )

# =============== SUMMARIZER ===============
elif page == "✨ Smart Summarizer":

    st.title("✨ Smart Text Summarizer")
    st.write("Convert lengthy text into a concise summary.")

    text = st.text_area(
        "Paste your study material here",
        height=220,
        placeholder="Enter your paragraph or notes..."
    )

    summary_length = st.slider(
        "Number of summary sentences",
        1, 8, 3
    )

    if st.button("✨ Analyze and Summarize", use_container_width=True):
        if len(text.split()) < 10:
            st.warning("Please enter at least 10 words.")
        else:
            result = summarize_text(text, summary_length)
            st.session_state.text = text
            st.session_state.history.append(len(text.split()))

            st.success("Text analysis completed!")

            st.subheader("📄 Generated Summary")
            st.markdown(
                f'<div class="card">{result}</div>',
                unsafe_allow_html=True
            )

            st.metric(
                "Original Word Count",
                len(text.split())
            )

            st.metric(
                "Summary Word Count",
                len(result.split())
            )

# =============== KEY CONCEPTS ===============
elif page == "🔑 Key Concepts":

    st.title("🔑 Key Concept Extraction")
    st.write("Identify important terms in your study material.")

    text = st.text_area(
        "Enter text for concept extraction",
        height=200
    )

    if st.button("Extract Key Concepts"):
        if not text.strip():
            st.warning("Please enter some text.")
        else:
            keywords = extract_keywords(text)

            st.success("Concepts extracted!")

            for word, frequency in keywords:
                st.markdown(
                    f'<div class="card">'
                    f'<h3>🔹 {word.title()}</h3>'
                    f'<p>Frequency: {frequency}</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )

            if keywords:
                chart = px.bar(
                    x=[x[0] for x in keywords],
                    y=[x[1] for x in keywords],
                    labels={"x": "Concept", "y": "Frequency"},
                    title="Concept Frequency Analysis"
                )
                chart.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)"
                )
                st.plotly_chart(chart, use_container_width=True)

# =============== QUIZ GENERATOR ===============
elif page == "🎯 Quiz Generator":

    st.title("🎯 Knowledge Assessment")
    st.write("Test your understanding of Artificial Intelligence.")

    questions = [
        {
            "q": "What does AI stand for?",
            "options": [
                "Artificial Intelligence",
                "Automatic Internet",
                "Advanced Information",
                "Applied Interface"
            ],
            "answer": "Artificial Intelligence"
        },
        {
            "q": "Which language is widely used in AI?",
            "options": ["Python", "HTML", "CSS", "XML"],
            "answer": "Python"
        },
        {
            "q": "Machine Learning is a subset of which field?",
            "options": [
                "Web Design",
                "Artificial Intelligence",
                "Networking",
                "Operating Systems"
            ],
            "answer": "Artificial Intelligence"
        },
        {
            "q": "What is NLP?",
            "options": [
                "Natural Language Processing",
                "Network Learning Program",
                "New Logic Process",
                "Neural Link Protocol"
            ],
            "answer": "Natural Language Processing"
        },
        {
            "q": "Which is an example of supervised learning?",
            "options": [
                "Learning with labelled data",
                "Learning without data",
                "Random guessing",
                "Data deletion"
            ],
            "answer": "Learning with labelled data"
        }
    ]

    with st.form("cognify_quiz"):
        answers = []

        for i, q in enumerate(questions):
            st.markdown(f"### Question {i + 1}")
            st.write(q["q"])

            answer = st.radio(
                "Select your answer",
                q["options"],
                key=f"quiz_{i}"
            )
            answers.append(answer)

            st.divider()

        submitted = st.form_submit_button(
            "Submit Assessment",
            use_container_width=True
        )

    if submitted:
        score = sum(
            answers[i] == questions[i]["answer"]
            for i in range(len(questions))
        )

        st.session_state.quiz_score = score
        st.session_state.history.append(score)

        st.success(f"Your score: {score}/{len(questions)}")

        st.progress(score / len(questions))

        if score == len(questions):
            st.balloons()
            st.success("Excellent! All answers are correct.")
        else:
            st.info("Keep practising and review the concepts!")

        with st.expander("Review correct answers"):
            for i, q in enumerate(questions):
                st.write(
                    f"**Q{i+1}. {q['q']}**"
                )
                st.write(
                    f"Correct answer: {q['answer']}"
                )

# =============== FLASHCARDS ===============
elif page == "📚 Flashcards":

    st.title("📚 Smart Revision Flashcards")
    st.write("Review important Artificial Intelligence concepts.")

    flashcards = [
        ("Artificial Intelligence",
         "The field of creating systems that perform tasks requiring human-like intelligence."),

        ("Machine Learning",
         "A subset of AI that enables systems to learn patterns from data."),

        ("Natural Language Processing",
         "A field of AI that enables computers to process human language."),

        ("Deep Learning",
         "A machine learning approach based on multi-layered neural networks."),

        ("Neural Network",
         "A computational model inspired by interconnected biological neurons.")
    ]

    if st.session_state.flash_index >= len(flashcards):
        st.session_state.flash_index = 0

    question, answer = flashcards[st.session_state.flash_index]

    st.markdown(
        f'<div class="hero"><h2>🧠 {question}</h2>'
        f'<p>Flashcard {st.session_state.flash_index + 1} '
        f'of {len(flashcards)}</p></div>',
        unsafe_allow_html=True
    )

    if st.button("Reveal Answer"):
        st.info(answer)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅ Previous"):
            st.session_state.flash_index = (
                st.session_state.flash_index - 1
            ) % len(flashcards)
            st.rerun()

    with col2:
        if st.button("Next ➡"):
            st.session_state.flash_index = (
                st.session_state.flash_index + 1
            ) % len(flashcards)
            st.rerun()

# =============== ANALYTICS ===============
elif page == "📊 Analytics":

    st.title("📊 Learning Analytics")
    st.write("Explore your learning activity and performance.")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Text Analyses", len(st.session_state.history))

    with c2:
        st.metric(
            "Latest Quiz Score",
            str(st.session_state.quiz_score)
            + "/5" if st.session_state.quiz_score is not None else "Not attempted"
        )

    with c3:
        st.metric("Learning Platform", "Active")

    scores = [
        value for value in st.session_state.history
        if isinstance(value, int) and value <= 5
    ]

    if scores:
        chart = px.line(
            x=list(range(1, len(scores) + 1)),
            y=scores,
            markers=True,
            title="Quiz Performance"
        )
        chart.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Attempt",
            yaxis_title="Score"
        )
        st.plotly_chart(chart, use_container_width=True)
    else:
        st.info("Complete a quiz to see your performance chart.")

    st.caption(
        "Analytics are stored for this active session only."
    )

# =============== AI ARCHITECTURE ===============
elif page == "⚙️ AI Architecture":

    st.title("⚙️ Cognify AI System Architecture")

    st.write(
        "Explore the processing workflow behind the learning assistant."
    )

    stages = [
        "User Input",
        "Text Preprocessing",
        "NLP Analysis",
        "Concept Extraction",
        "Summary Generation",
        "Learning Assessment",
        "Feedback"
    ]

    fig = go.Figure()

    for i, stage in enumerate(stages):
        fig.add_trace(go.Scatter(
            x=[i],
            y=[0],
            mode="markers+text",
            marker=dict(
                size=48,
                color="#8b5cf6",
                line=dict(color="#c4b5fd", width=2)
            ),
            text=[stage],
            textposition="bottom center",
            textfont=dict(color="white", size=11),
            showlegend=False,
            hovertemplate=stage + "<extra></extra>"
        ))

        if i < len(stages) - 1:
            fig.add_annotation(
                x=i + 0.5,
                y=0,
                ax=i,
                ay=0,
                xref="x",
                yref="y",
                axref="x",
                ayref="y",
                text="",
                showarrow=True,
                arrowhead=3,
                arrowcolor="#22d3ee"
            )

    fig.update_layout(
        template="plotly_dark",
        height=350,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=30, r=30, t=40, b=100)
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🧠 Core Technologies")

    st.markdown("""
    - **Python:** Application logic
    - **Natural Language Processing:** Text analysis
    - **Scikit-learn:** Available for future ML extensions
    - **Plotly:** Interactive data visualization
    - **Streamlit:** Interactive application interface
    """)

    st.info(
        "Current implementation uses lightweight, extractive NLP "
        "and rule-based quiz content. It does not use a trained "
        "generative AI model."
    )

# =============== FOOTER ===============
st.divider()
st.markdown(
    "<center>🧠 Cognify AI | Intelligent Learning Experience</center>",
    unsafe_allow_html=True
)