import os
import streamlit as st
import time
from src.dfs_engine import run_exact_dfs
from src.euler_engine import run_fast_eulerian

# 1. Translation Dictionary (Localization)
LANGUAGES = {
    "en": {
        "title": "🧩 Digital Chain Puzzle Solver",
        "subtitle": "Test assignment for **PortaOne**. Intelligent hybrid engine.",
        "lang_label": "🌐 Language / Мова",
        "data_source_label": "Choose Data Source",
        "source_demo": "📂 Use Demo File (142 fragments)",
        "source_upload": "📤 Upload Custom File (.txt)",
        "uploader_label": "Upload a .txt file with fragments",
        "success_load": "Successfully loaded fragments: **{}**",
        "btn_run": "Run Computations",
        "spinner": "Calculating, please wait...",
        "engine_dfs": "🤖 Exact DFS selected (calculating global maximum)",
        "engine_euler": "⚡ Fast Eulerian hybrid selected (Look-ahead heuristic)",
        "success_calc": "Calculation finished!",
        "metric_fragments": "Fragments Used",
        "metric_digits": "Chain Length (digits)",
        "metric_time": "Execution Time",
        "sec": "sec",
        "pcs": "pcs",
        "digits": "digits",
        "result_header": "Resulting Number Puzzle:",
        "error_empty": "⚠️ Failed to assemble any continuous chain from these data.",
        "error_no_demo": "⚠️ Demo file not found at data/source.txt. Please upload your own.",
    },
    "uk": {
        "title": "🧩 Пазл-конструктор цифрових ланцюжків",
        "subtitle": "Тестове завдання для **PortaOne**. Інтелектуальний гібридний двіжок.",
        "lang_label": "🌐 Мова / Language",
        "data_source_label": "Оберіть джерело даних",
        "source_demo": "📂 Використати демо-файл (142 фрагменти)",
        "source_upload": "📤 Завантажити власний файл (.txt)",
        "uploader_label": "Завантажте .txt файл із фрагментами",
        "success_load": "Успішно завантажено фрагментів: **{}**",
        "btn_run": "Запустити обчислення",
        "spinner": "Йде розрахунок, будь ласка, зачекайте...",
        "engine_dfs": "🤖 Обрано точний DFS (розрахунок глобального максимуму)",
        "engine_euler": "⚡ Обрано швидкий Ейлерів гібрид (Look-ahead евристика)",
        "success_calc": "Розрахунок завершено!",
        "metric_fragments": "Використано фрагментів",
        "metric_digits": "Довжина числа (знаків)",
        "metric_time": "Час розрахунку",
        "sec": "сек",
        "pcs": "шт.",
        "digits": "знаків",
        "result_header": "Зібране число-пазл:",
        "error_empty": "⚠️ Не вдалося зібрати жодного безперервного ланцюжка з цих даних.",
        "error_no_demo": "⚠️ Демо-файл не знайдено за шляхом data/source.txt. Будь ласка, завантажте свій.",
    }
}

st.set_page_config(page_title="Puzzle Solver", page_icon="🧩", layout="centered")

# 2. Language selection in the sidebar
st.sidebar.title("Settings / Налаштування")
lang_choice = st.sidebar.selectbox(
    "🌐 Select Language", 
    options=["English", "Українська"],
    index=0
)

lang = "en" if lang_choice == "English" else "uk"
t = LANGUAGES[lang]

# 3. Main interface
st.title(t["title"])
st.write(t["subtitle"])

# Switch: Demo or Custom File
data_source = st.radio(
    t["data_source_label"],
    options=["demo", "upload"],
    format_func=lambda x: t["source_demo"] if x == "demo" else t["source_upload"]
)

fragments = []
file_ready = False

if data_source == "demo":
    demo_path = os.path.join("data", "source.txt")
    if os.path.exists(demo_path):
        with open(demo_path, "r", encoding="utf-8") as f:
            fragments = [line.strip() for line in f if line.strip()]
        st.info(t["success_load"].format(len(fragments)))
        file_ready = True
    else:
        st.error(t["error_no_demo"])

else:
    uploaded_file = st.file_uploader(t["uploader_label"], type=["txt"])
    if uploaded_file is not None:
        bytes_data = uploaded_file.read()
        fragments = [line.strip() for line in bytes_data.decode("utf-8", errors="ignore").split("\n") if line.strip()]
        st.info(t["success_load"].format(len(fragments)))
        file_ready = True

# 4. Calculation start button
if file_ready:
    if st.button(t["btn_run"], type="primary", use_container_width=True):
        with st.spinner(t["spinner"]):
            start_time = time.time()
            total_count = len(fragments)
            
            # Smart engine switching
            if total_count <= 170:
                st.caption(t["engine_dfs"])
                result_puzzle, chain_len = run_exact_dfs(fragments)
            else:
                st.caption(t["engine_euler"])
                result_puzzle, chain_len = run_fast_eulerian(fragments, depth=4)
                
            end_time = time.time()
            
        # Output of results
        if result_puzzle:
            st.success(t["success_calc"])
            
            col1, col2, col3 = st.columns(3)
            col1.metric(t["metric_fragments"], f"{chain_len} {t['pcs']}")
            col2.metric(t["metric_digits"], f"{len(result_puzzle)} {t['digits']}")
            col3.metric(t["metric_time"], f"{end_time - start_time:.4f} {t['sec']}")
            
            st.subheader(t["result_header"])
            st.code(result_puzzle, wrap_lines=True)
        else:
            st.error(t["error_empty"])