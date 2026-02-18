import streamlit as st
import pandas as pd
import numpy as np
import openpyxl
import hashlib

# dataset profiling
from analysis.dataset_profile import generate_dataset_profile

from reasoning.context_builder import build_reasoning_context
from reasoning.reason_engine import run_reasoning
from rag.retriever import index_reasoning
from rag.bot import run_chatbot



st.set_page_config(
  page_title="AI Dataset Inspector",
  page_icon="🤖",
  layout="wide",
  initial_sidebar_state="expanded",
)

st.title("🤖 AI Dataset Inspector")
st.divider()

# global variable css
st.markdown("""
  <style>
    body {
      background-color: #f0f2f6;
    }

    .section-title {
      font-size: 20px;
      font-weight: 600;
      margin-bottom: 10px;
    }

    .card {
        background-color: #161b22;
        padding: 20px;
        border-radius: 12px;
    }

  </style>
""", unsafe_allow_html=True)


# sidebar
with st.sidebar:

  # logo
  st.image("image/LYZERAI.png", width=150)

#   st.header("Navigation Menu")

#   st.divider()

#   with st.container():
#     st.button ("Home", icon="🏠", width='stretch')
#     st.button("AI chatbot", icon="💬", width='stretch')

  st.divider()

  with st.container():
    analysis_mode = st.sidebar.selectbox(
      "Select Analysis Mode",
      ("AI Insights", "Standard Analysis")
    )

  with st.container():
    st.header("Upload Dataset")
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "json"])

    if uploaded_file:
        # Create a unique and valid collection name for the uploaded file
        file_identifier = f"{uploaded_file.name}_{uploaded_file.size}"
        collection_name = hashlib.md5(file_identifier.encode()).hexdigest()

        if "collection_name" not in st.session_state or st.session_state.collection_name != collection_name:
            st.session_state.collection_name = collection_name
            if "reasoning_result" in st.session_state:
                del st.session_state["reasoning_result"]
            if "messages" in st.session_state:
                st.session_state.messages = []

# dataset load
dataFrame_ = None


# fungsi untuk mengecek apakah suatu file excel memiliki header
def auto_excel_index(df_preview, threshold=0.5):

    for i, row in df_preview.iterrows():
        non_empty = row.notna().sum() / len(row)
        if non_empty >= threshold:
            return i

    return 0

def load_dataset(uploaded_file):
    # opened_file = uploaded_file.name.lower()
    opened_file = uploaded_file

    if opened_file.name.endswith(".csv"):
        return pd.read_csv(uploaded_file)

    if uploaded_file.name.endswith(".json"):
        return pd.read_json(uploaded_file)

    if uploaded_file.name.endswith(".xlsx"):
        # percobaan apabila suatu file excel memiliki suatu header
        try:
            excel_file = pd.ExcelFile(uploaded_file, engine='openpyxl')
            all_sheet = excel_file.sheet_names

            # untuk memilih sheet mana yang akan digunakan untuk analisis
            if len(all_sheet) > 1:
                sheet_name = st.selectbox(
                    "Select sheet to load",
                    all_sheet
                )
            else:
                sheet_name = all_sheet[0]

            header_preview = pd.read_excel(uploaded_file, sheet_name=sheet_name, header=None, engine="openpyxl")
            header_of_row = auto_excel_index(header_preview)

            st.info(f"Terdeteksi baris awal ada pada index: {header_of_row}")

            return pd.read_excel(
                uploaded_file,
                sheet_name=sheet_name,
                header=header_of_row,
                engine='openpyxl'
            )

            # dataFrame_ = pd.read_excel(
            #     uploaded_file,
            #     sheet_name=sheet_name,
            #     header=header_of_row,
            #     engine='openpyxl'
            # )

        except Exception as exc:
            st.warning(f"Mohon cek kembali apakah file excel anda sesuai: {exc}")

if uploaded_file:
    try:
        dataFrame_ = load_dataset(uploaded_file)
            # try:
            #     # deteksi apakah ada multiple sheet
            #     multiple_sheets = pd.ExcelFile(uploaded_file, engine='openpyxl').sheet_names
            #     if len(multiple_sheets) > 1:
            #         sheet_name = st.selectbox(
            #             "Select sheet to load",
            #             multiple_sheets
            #         )
            #         dataFrame_ = pd.read_excel(uploaded_file, sheet_name=sheet_name, engine='openpyxl')

            #     # deteksi apakah col atau row digunakan sebagai header
            #     use_first_row_as_header = st.checkbox("Use first row as header", value=True)

            #     if not use_first_row_as_header:
            #         dataFrame_ = pd.read_excel(uploaded_file, header=None, engine='openpyxl')
            #         dataFrame_.columns = [f"Column {i+1}" for i in range(dataFrame_.shape[1])]

            # except Exception as exc:
            #     st.warning(f"Maaf silahkan periksa apakah ada masalah dengan dataset anda {exc}")


    except Exception as e:
        st.error(f"Failed to load dataset, error: {e}")
        st.stop()

# dashboard
if dataFrame_ is not None:

    # dataset overview
    st.markdown("### Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.info("**rows**")
        st.metric("rows", dataFrame_.shape[0])
        # try:
        #     metric_array = np.array(list(dataFrame_.shape))
        #     st.metric("Rows", metric_array[0])
        # except:
        #     st.write(f"ada kesalahan pada sistem")

    with col2:
        # try:
        #     metric_array = np.array(list(dataFrame_.shape))
        #     st.metric("Rows", metric_array[0])
        # except:
        #     st.write(f"ada kesalahan pada sistem")
        st.info("**columns**")
        st.metric("Columns", dataFrame_.shape[1])

    with col3:
        st.info("**missing cells**")
        missing_pct = (dataFrame_.isna().sum().sum() / dataFrame_.size) * 100
        st.metric("Missing Cells (%)", f"{missing_pct:.2f}")

    with col4:
        st.info("**duplicate rows**")
        st.metric("Duplicate Rows", dataFrame_.duplicated().sum())

    st.divider()

    # analisa visual untuk missing value
    st.markdown("### Missing Value Analysis")

    left, right = st.columns([2, 1])

    with left:
        st.info("#### Missing Value Distribution")
        # st.markdown("### Missing Value Distribution")
        st.divider()

        missing_by_col = dataFrame_.isna().mean().sort_values(ascending=False)

        # memunculkan Bar chart for missing value distribution jika ada
        if missing_by_col.empty and missing_pct == 0.00:
            st.dataframe(pd.DataFrame({"No missing values": []}), width="stretch")
        else:
            st.bar_chart(missing_by_col, height=300)

    with right:
        st.info("#### High Risk Columns")
        # st.markdown("### High Risk Columns")
        st.divider()

        # resiko
        high_risk = missing_by_col[missing_by_col > 0.3]
        medium_risk = missing_by_col[(missing_by_col > 0.1) & (missing_by_col <= 0.3)]
        low_risk = missing_by_col[(missing_by_col <= 0.1) & (missing_by_col > 0)]

        # logika resiko
        if not high_risk.empty:
            st.error(
                f"Detected {len(high_risk)} high-risk columns with >30% missing values",
                icon="🚨"
            )
            st.dataframe(
                high_risk.rename("Missing Ratio"),
                width=300
            )

        if not medium_risk.empty:
            st.warning(
                f"Detected {len(medium_risk)} medium-risk columns with 10%-30% missing values",
                icon="⚠️"
            )
            st.dataframe(
                medium_risk.rename("Missing Ratio"),
                width=300
            )

        elif not low_risk.empty:
            st.info(
                f"Detected {len(low_risk)} low-risk columns with <=10% missing values",
                icon="⚠️"
            )
            st.dataframe(
                low_risk.rename("Missing Ratio"),
                width=300
            )

        else:
            st.success("No high-risk or medium-risk columns detected", icon="✅")

    st.divider()

    # profiling test
    # profiling = generate_dataset_profile(dataFrame_)
    # st.json(profiling)


    # AI insight panel
    st.markdown("### 🧠 AI Insight Panel")

    if analysis_mode == "AI Insights":
        dataset_profile = generate_dataset_profile(dataFrame_)

        # DEBUG: Tampilkan isi dataset_profile untuk melihat nama key yang benar
        # st.write("Isi dataset_profile:", dataset_profile)
        # st.info("AI recommendations powered by RAG will appear here.")

        # st.markdown("""
        # **Planned outputs:**
        # - Dataset risk summary
        # - Bias warnings
        # - Preprocessing checklist
        # """)

        if "reasoning_result" not in st.session_state:
            context = build_reasoning_context(
                dataset_profile=dataset_profile,
                # missing_by_column=missing_by_column,
                # duplicate_rows_count=duplicate_count
            )
            st.session_state.reasoning_result = run_reasoning(context)
            # Index the reasoning results once for the current file's collection
            with st.spinner("Creating AI context..."):
                index_reasoning(st.session_state.reasoning_result, st.session_state.collection_name)

        # st.write(dataset_profile)

        reasoning_result = st.session_state.reasoning_result


        st.subheader("Dataset Quality Insights")
        Risk_Level = reasoning_result.risk_levels

        # st.metric("Risk Level", reasoning_result.risk_levels)

        if Risk_Level == "HIGH":
            st.error(f"Overall Risk Level: {Risk_Level}", icon="🚨")
        elif Risk_Level == "MEDIUM":
            st.warning(f"Overall Risk Level: {Risk_Level}", icon="⚠️")
        elif Risk_Level == "LOW":
            st.success(f"Overall Risk Level: {Risk_Level}", icon="✅")

        # chatbot_response = run_chatbot(reasoning_result)

        st.markdown("#### 📊 Reasoning Insights & Recommendations")
        for index in reasoning_result.insights:
            st.markdown(f"**- {index}**")

        for recommendation in reasoning_result.recommendations:
            st.markdown(f"**• {recommendation}**")

        st.divider()

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_question = st.chat_input("Ask a question about your dataset:")

        if user_question:
            st.session_state.messages.append({
                "role": "user",
                "content": user_question
            })

            with st.chat_message("user"):
                st.markdown(user_question)

            chatbot_response = run_chatbot(
                reasoning_result=reasoning_result,
                collection_name=st.session_state.collection_name,
                user_questions=user_question
            )

            st.session_state.messages.append({
                "role": "assistant",
                "content": chatbot_response
            })

            with st.chat_message("assistant"):
                st.markdown(chatbot_response)

    else:
        # st.caption("Switch to **AI Insights** or **Standard Analysis** mode to view AI reasoning.")
        # st.caption("Switch to **AI Insights** mode to view AI reasoning.")
        st.info("anda sekarang berada di mode **Standard Analysis**")
        st.caption("Coba berganti ke mode **AI Insights** untuk melihat AI reasoning dan chatbot.")

else:
    st.info("Upload a dataset to start analysis.")
