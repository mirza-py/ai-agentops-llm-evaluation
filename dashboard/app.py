import sqlite3

import pandas as pd

import streamlit as st


st.set_page_config(
    page_title="AI AgentOps",
    page_icon="🤖",
    layout="wide"
)


DB_PATH = "agentops.db"


@st.cache_data(ttl=5)
def load_data():

    conn = sqlite3.connect(
        DB_PATH
    )

    query = """
    SELECT
        id,
        prompt,
        response,
        model,
        prompt_version,
        latency_seconds,
        relevance,
        accuracy,
        completeness,
        clarity,
        quality_score,
        failure,
        failure_reason
    FROM evaluation_logs
    ORDER BY id DESC
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    return df


# --------------------------------
# Header
# --------------------------------

st.title(
    "🤖 AI AgentOps Dashboard"
)

st.caption(
    "LLM Evaluation • Observability • Prompt Monitoring"
)


# --------------------------------
# Load database
# --------------------------------

try:

    df = load_data()

except Exception as e:

    st.error(
        f"Database error: {e}"
    )

    st.stop()


if df.empty:

    st.info(
        "No evaluation data available. "
        "Send requests through /chat first."
    )

    st.stop()


# --------------------------------
# KPI Metrics
# --------------------------------

total_requests = len(df)

average_quality = round(
    df["quality_score"].mean(),
    2
)

average_latency = round(
    df["latency_seconds"].mean(),
    2
)

failure_rate = round(
    df["failure"].mean() * 100,
    2
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Requests",
        total_requests
    )


with col2:

    st.metric(
        "Average Quality",
        f"{average_quality}/10"
    )


with col3:

    st.metric(
        "Average Latency",
        f"{average_latency}s"
    )


with col4:

    st.metric(
        "Failure Rate",
        f"{failure_rate}%"
    )


st.divider()


# --------------------------------
# Quality Metrics
# --------------------------------

st.subheader(
    "Evaluation Performance"
)


metric_data = pd.DataFrame({

    "Metric": [
        "Relevance",
        "Accuracy",
        "Completeness",
        "Clarity"
    ],

    "Score": [

        df["relevance"].mean(),

        df["accuracy"].mean(),

        df["completeness"].mean(),

        df["clarity"].mean()
    ]
})


metric_data["Score"] = (
    metric_data["Score"]
    .round(2)
)


st.bar_chart(
    metric_data.set_index(
        "Metric"
    )
)


# --------------------------------
# Latency
# --------------------------------

st.subheader(
    "Request Latency"
)


latency_data = df[
    [
        "id",
        "latency_seconds"
    ]
].set_index("id")


st.line_chart(
    latency_data
)


# --------------------------------
# Prompt Versions
# --------------------------------

st.subheader(
    "Prompt Version Performance"
)


prompt_stats = (

    df.groupby(
        "prompt_version"
    )

    .agg(

        average_quality=(
            "quality_score",
            "mean"
        ),

        average_accuracy=(
            "accuracy",
            "mean"
        ),

        average_relevance=(
            "relevance",
            "mean"
        ),

        average_latency=(
            "latency_seconds",
            "mean"
        ),

        requests=(
            "id",
            "count"
        )
    )

    .reset_index()
)


prompt_stats[
    [
        "average_quality",
        "average_accuracy",
        "average_relevance",
        "average_latency"
    ]
] = prompt_stats[
    [
        "average_quality",
        "average_accuracy",
        "average_relevance",
        "average_latency"
    ]
].round(2)


st.dataframe(
    prompt_stats,
    use_container_width=True
)


# --------------------------------
# Recent Requests
# --------------------------------

st.subheader(
    "Recent LLM Requests"
)


display_df = df[
    [
        "id",
        "prompt",
        "model",
        "prompt_version",
        "latency_seconds",
        "relevance",
        "accuracy",
        "completeness",
        "clarity",
        "quality_score",
        "failure"
    ]
]


st.dataframe(
    display_df,
    use_container_width=True
)


# --------------------------------
# Failed Requests
# --------------------------------

failed_df = df[
    df["failure"] == True
]


if not failed_df.empty:

    st.subheader(
        "⚠️ Failed Evaluations"
    )

    st.dataframe(
        failed_df[
            [
                "id",
                "prompt",
                "failure_reason"
            ]
        ],
        use_container_width=True
    )