"""
Mind vs Machine RNG - Enhanced Version
A consciousness-randomness exploration tool
"""
import streamlit as st
from datetime import datetime
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from src.rng_engine import RNGEngine, validate_range
from src.analytics import GameSession, Analytics, SessionManager
from src.ui_components import (
    render_header,
    render_special_time_badge,
    render_number_display,
    render_stats_card,
    render_distribution_chart,
    render_frequency_heatmap,
    render_history_table,
    render_insights,
    render_prediction_input,
    render_sidebar_settings,
)
from src.config import DEFAULT_MIN_VALUE, DEFAULT_MAX_VALUE, SPECIAL_NUMBER

# Page configuration
st.set_page_config(
    page_title="Mind vs Machine RNG",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load custom CSS
css_file = os.path.join(os.path.dirname(__file__), "assets", "style.css")
if os.path.exists(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if "sessions" not in st.session_state:
        # Load existing sessions from disk
        session_manager = SessionManager()
        st.session_state.sessions = session_manager.load_sessions()

    if "last_number" not in st.session_state:
        st.session_state.last_number = None

    if "last_prediction" not in st.session_state:
        st.session_state.last_prediction = None

    if "show_prediction" not in st.session_state:
        st.session_state.show_prediction = True

    if "confirm_delete" not in st.session_state:
        st.session_state.confirm_delete = False


def save_session(prediction, generated, game_mode, min_val, max_val, algorithm):
    """Save a game session"""
    session = GameSession(
        prediction=prediction,
        generated=generated,
        game_mode=game_mode,
        min_val=min_val,
        max_val=max_val,
        algorithm=algorithm,
    )
    st.session_state.sessions.append(session)

    # Save to disk
    session_manager = SessionManager()
    session_manager.save_sessions(st.session_state.sessions)


def main():
    """Main application logic"""
    initialize_session_state()

    # Render header
    render_header()

    # Show special time badge if applicable
    render_special_time_badge()

    # Sidebar settings
    settings = render_sidebar_settings()

    # Validate range
    is_valid, error_msg = validate_range(settings["min_val"], settings["max_val"])
    if not is_valid:
        st.error(f"⚠️ {error_msg}")
        return

    # Create RNG engine
    rng_engine = RNGEngine(algorithm=settings["algorithm"])

    # Show algorithm info
    algo_info = rng_engine.get_algorithm_info()
    st.sidebar.info(f"**{algo_info['name']}**\n\n{algo_info['description']}")

    # Main content area
    st.markdown("---")

    # Game controls
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        st.subheader("🎯 Make Your Prediction")
        if st.session_state.show_prediction:
            prediction = render_prediction_input(
                settings["min_val"], settings["max_val"], settings["game_mode"]
            )
            st.session_state.last_prediction = prediction
        else:
            st.info("Number generated! Ready for next round.")

    with col2:
        st.subheader("🎲 Generate")
        if st.button("🎲 Generate Number", use_container_width=True, type="primary"):
            try:
                generated = rng_engine.generate(settings["min_val"], settings["max_val"])
                st.session_state.last_number = generated

                # Save session
                save_session(
                    prediction=st.session_state.last_prediction,
                    generated=generated,
                    game_mode=settings["game_mode"],
                    min_val=settings["min_val"],
                    max_val=settings["max_val"],
                    algorithm=settings["algorithm"],
                )

                st.session_state.show_prediction = False
                st.rerun()
            except Exception as e:
                st.error(f"Error generating number: {e}")

    with col3:
        st.subheader("🔄 Reset")
        if st.button("🔄 New Round", use_container_width=True):
            st.session_state.last_number = None
            st.session_state.last_prediction = None
            st.session_state.show_prediction = True
            st.rerun()

    # Display result
    if st.session_state.last_number is not None:
        last_session = st.session_state.sessions[-1] if st.session_state.sessions else None
        if last_session:
            is_hit = last_session.is_hit()
            is_special = st.session_state.last_number == SPECIAL_NUMBER
            render_number_display(st.session_state.last_number, is_hit, is_special)

            # Show prediction result
            if last_session.prediction is not None:
                distance = last_session.distance()
                if is_hit:
                    st.success(f"🎯 **PERFECT!** You predicted exactly right!")
                else:
                    st.info(f"📏 Distance from prediction: **{distance}**")

    st.markdown("---")

    # Statistics Dashboard
    if st.session_state.sessions:
        analytics = Analytics(st.session_state.sessions)

        st.header("📊 Statistics Dashboard")

        # Key metrics
        metric_cols = st.columns(5)
        with metric_cols[0]:
            render_stats_card("Total Attempts", str(analytics.total_attempts()), "🎲")
        with metric_cols[1]:
            render_stats_card("Predictions", str(analytics.total_predictions()), "🎯")
        with metric_cols[2]:
            render_stats_card("Direct Hits", str(analytics.total_hits()), "✅")
        with metric_cols[3]:
            hit_rate = analytics.hit_rate()
            render_stats_card("Hit Rate", f"{hit_rate:.1f}%", "📈")
        with metric_cols[4]:
            render_stats_card("Current Streak", str(analytics.current_streak()), "🔥")

        # Charts
        st.markdown("---")
        chart_tabs = st.tabs(["📊 Distribution", "🗺️ Heatmap", "📜 History", "🔍 Insights"])

        with chart_tabs[0]:
            render_distribution_chart(st.session_state.sessions)

        with chart_tabs[1]:
            render_frequency_heatmap(
                st.session_state.sessions, settings["min_val"], settings["max_val"]
            )

        with chart_tabs[2]:
            st.subheader("Recent History")
            max_display = st.slider("Show last N attempts:", 5, 50, 10)
            render_history_table(st.session_state.sessions, max_display)

        with chart_tabs[3]:
            render_insights(st.session_state.sessions, settings["min_val"], settings["max_val"])

        # Data export
        st.markdown("---")
        st.subheader("💾 Export Data")
        export_cols = st.columns([1, 1, 2])

        with export_cols[0]:
            if st.button("📥 Export to CSV", use_container_width=True):
                session_manager = SessionManager()
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"data/exports/sessions_{timestamp}.csv"
                os.makedirs("data/exports", exist_ok=True)

                if session_manager.export_to_csv(st.session_state.sessions, output_path):
                    st.success(f"✅ Exported to {output_path}")
                else:
                    st.error("❌ Export failed")

        with export_cols[1]:
            # Show confirmation button if delete was clicked
            if not st.session_state.confirm_delete:
                if st.button("🗑️ Clear All Data", use_container_width=True):
                    st.session_state.confirm_delete = True
                    st.rerun()
            else:
                # Confirmation mode
                st.warning("⚠️ This will delete all session data!")
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("✅ Yes, Delete", use_container_width=True, type="primary"):
                        st.session_state.sessions = []
                        session_manager = SessionManager()
                        session_manager.save_sessions([])
                        st.session_state.confirm_delete = False
                        st.success("✅ All data cleared!")
                        st.rerun()
                with col_b:
                    if st.button("❌ Cancel", use_container_width=True):
                        st.session_state.confirm_delete = False
                        st.rerun()

        with export_cols[2]:
            st.info(f"📊 Total sessions stored: {len(st.session_state.sessions)}")

    else:
        st.info("👋 Welcome! Make your first prediction and generate a number to begin.")

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #888; padding: 20px;'>
        <p><i>"At 47 minutes past the hour, the observer becomes the observed."</i></p>
        <p style='font-size: 12px;'>Mind vs Machine RNG v2.0 - Enhanced Edition</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
