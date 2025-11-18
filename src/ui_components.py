"""
Reusable UI components for Mind vs Machine RNG
"""
import streamlit as st
from typing import List, Optional
from src.analytics import GameSession, Analytics
from src.config import COLORS, SPECIAL_NUMBER
import plotly.graph_objects as go
import plotly.express as px


def render_header():
    """Render application header"""
    st.title("🧠 Mind vs Machine 🎲")
    st.markdown(
        """
        <div style='text-align: center; padding: 10px; background-color: rgba(255,255,255,0.05); border-radius: 10px; margin-bottom: 20px;'>
        <h3>Can consciousness influence randomness?</h3>
        <p>Focus your intention. Make a prediction. Observe the pattern.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_special_time_badge():
    """Show special badge if it's the 47th minute"""
    from datetime import datetime
    from src.config import SPECIAL_MINUTE

    if datetime.now().minute == SPECIAL_MINUTE:
        st.markdown(
            f"""
            <div style='background-color: gold; color: black; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold;'>
            ⏰ SPECIAL TIME: {SPECIAL_MINUTE}th MINUTE - The observer becomes the observed
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_number_display(number: int, is_hit: bool = False, is_special: bool = False):
    """Display generated number with styling"""
    if is_special:
        color = COLORS["special"]
        message = f"✨ SPECIAL NUMBER: {SPECIAL_NUMBER}! ✨"
    elif is_hit:
        color = COLORS["success"]
        message = "🎯 DIRECT HIT! Perfect prediction!"
    else:
        color = COLORS["neutral"]
        message = ""

    st.markdown(
        f"""
        <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        border-radius: 15px; border: 2px solid {color}; margin: 20px 0;'>
            <h1 style='font-size: 72px; margin: 0; color: {color};'>{number}</h1>
            <p style='color: {color}; font-size: 18px; margin-top: 10px;'>{message}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stats_card(title: str, value: str, icon: str = "📊"):
    """Render a statistics card"""
    st.markdown(
        f"""
        <div style='background-color: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; text-align: center;'>
            <h3>{icon} {title}</h3>
            <h2 style='color: #00ff00; margin: 10px 0;'>{value}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_distribution_chart(sessions: List[GameSession], bins: int = 10):
    """Render distribution chart using Plotly"""
    if not sessions:
        st.info("No data to display yet. Start generating numbers!")
        return

    analytics = Analytics(sessions)
    dist_data = analytics.get_distribution_data(bins)

    fig = go.Figure(
        data=[
            go.Bar(
                x=dist_data["bins"],
                y=dist_data["counts"],
                marker_color="#00ff00",
                text=dist_data["counts"],
                textposition="auto",
            )
        ]
    )

    fig.update_layout(
        title="Number Distribution",
        xaxis_title="Number Range",
        yaxis_title="Frequency",
        template="plotly_dark",
        height=400,
        showlegend=False,
    )

    st.plotly_chart(fig, use_container_width=True)


def render_frequency_heatmap(sessions: List[GameSession], min_val: int = 0, max_val: int = 99):
    """Render frequency heatmap"""
    if not sessions:
        return

    analytics = Analytics(sessions)
    freq = analytics.number_frequency()

    # Create grid data
    numbers_per_row = 10
    rows = (max_val - min_val + 1 + numbers_per_row - 1) // numbers_per_row

    # Build matrix
    matrix = []
    labels = []
    for row in range(rows):
        row_data = []
        row_labels = []
        for col in range(numbers_per_row):
            num = min_val + row * numbers_per_row + col
            if num <= max_val:
                row_data.append(freq.get(num, 0))
                row_labels.append(str(num))
            else:
                row_data.append(0)
                row_labels.append("")
        matrix.append(row_data)
        labels.append(row_labels)

    # Create heatmap
    fig = go.Figure(
        data=go.Heatmap(
            z=matrix,
            text=labels,
            texttemplate="%{text}",
            colorscale="Greens",
            showscale=True,
        )
    )

    fig.update_layout(
        title="Number Frequency Heatmap",
        template="plotly_dark",
        height=400,
        xaxis=dict(showticklabels=False),
        yaxis=dict(showticklabels=False),
    )

    st.plotly_chart(fig, use_container_width=True)


def render_history_table(sessions: List[GameSession], max_rows: int = 10):
    """Render recent history as a table"""
    if not sessions:
        st.info("No history yet. Start making predictions!")
        return

    # Get recent sessions
    recent = sessions[-max_rows:][::-1]  # Reverse to show newest first

    # Build table data
    data = []
    for i, session in enumerate(recent, 1):
        prediction_str = str(session.prediction) if session.prediction is not None else "—"
        hit_str = "✅" if session.is_hit() else "❌" if session.prediction is not None else "—"
        distance_str = str(session.distance()) if session.distance() is not None else "—"

        data.append(
            {
                "#": len(sessions) - i + 1,
                "Predicted": prediction_str,
                "Generated": session.generated,
                "Hit": hit_str,
                "Distance": distance_str,
                "Algorithm": session.algorithm[:8],
            }
        )

    import pandas as pd

    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)


def render_insights(sessions: List[GameSession], min_val: int = 0, max_val: int = 99):
    """Render insights and pattern analysis"""
    if len(sessions) < 3:
        st.info("Generate more numbers to see pattern insights...")
        return

    analytics = Analytics(sessions)

    st.subheader("🔍 Pattern Insights")

    col1, col2 = st.columns(2)

    with col1:
        # Hot numbers
        st.markdown("**🔥 Hot Numbers**")
        hot = analytics.hot_numbers(5)
        if hot:
            for num, count in hot:
                st.write(f"• **{num}** appeared {count}x")
        else:
            st.write("Not enough data")

    with col2:
        # Cold numbers
        st.markdown("**🧊 Cold Numbers**")
        cold = analytics.cold_numbers(5, min_val, max_val)
        if cold:
            for num in cold:
                st.write(f"• **{num}** (rare/never)")
        else:
            st.write("Not enough data")

    # Special number tracking
    special_count = analytics.special_number_count(SPECIAL_NUMBER)
    if special_count > 0:
        st.markdown(
            f"""
            <div style='background-color: gold; color: black; padding: 10px; border-radius: 5px; margin-top: 10px;'>
            ✨ Special number <b>{SPECIAL_NUMBER}</b> appeared <b>{special_count}</b> time(s)
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_prediction_input(min_val: int, max_val: int, game_mode: str) -> Optional[int]:
    """Render prediction input based on game mode"""
    if game_mode == "exact_match":
        prediction = st.number_input(
            "🎯 Enter your prediction:",
            min_value=min_val,
            max_value=max_val,
            value=min_val,
            step=1,
            help="Try to predict the exact number",
        )
        return int(prediction)
    elif game_mode == "high_low":
        # Simple high/low prediction
        st.write("🎯 Make your prediction:")
        choice = st.radio("Will the number be:", ["High", "Low"], horizontal=True)
        # For high/low we'll return a special code
        # High = max_val, Low = min_val (simplified)
        return max_val if choice == "High" else min_val
    else:
        # Default to exact match
        return st.number_input(
            "🎯 Enter your prediction:",
            min_value=min_val,
            max_value=max_val,
            value=min_val,
            step=1,
        )


def render_sidebar_settings():
    """Render sidebar settings"""
    st.sidebar.title("⚙️ Settings")

    # Algorithm selection
    from src.config import RNG_ALGORITHMS

    algorithm = st.sidebar.selectbox(
        "Random Algorithm:",
        options=list(RNG_ALGORITHMS.keys()),
        format_func=lambda x: RNG_ALGORITHMS[x],
        help="Choose the randomness algorithm",
    )

    # Game mode
    from src.config import GAME_MODES

    game_mode = st.sidebar.selectbox(
        "Game Mode:",
        options=list(GAME_MODES.keys()),
        format_func=lambda x: GAME_MODES[x],
        help="Choose how to play",
    )

    # Range settings
    st.sidebar.subheader("Number Range")
    min_val = st.sidebar.number_input("Minimum", value=0, min_value=0, max_value=10000)
    max_val = st.sidebar.number_input("Maximum", value=99, min_value=0, max_value=10000)

    # Theme toggle
    dark_mode = st.sidebar.checkbox("Dark Mode", value=True)

    return {
        "algorithm": algorithm,
        "game_mode": game_mode,
        "min_val": int(min_val),
        "max_val": int(max_val),
        "dark_mode": dark_mode,
    }
