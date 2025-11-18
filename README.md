# Mind vs Machine RNG – Code 47ne 🧠🎲

## Enhanced Edition v2.0

This is not just a number generator.
It's a perception test.
A probability resonance probe.
A glitch trap.

**Focus. Predict. Observe.**

Do the numbers know you're watching?

---

> "At 47 minutes past the hour, the observer becomes the observed."
> – Simulation Protocol Fragment, Rev 2.3

---

## ✨ Features

### Core Functionality
- 🎯 **Prediction Tracking** - Record your predictions and track accuracy
- 🎲 **Multiple RNG Algorithms** - Standard, Cryptographic, and Time-Based random generation
- 📊 **Statistical Analysis** - Real-time analytics and pattern detection
- 📈 **Data Visualization** - Distribution charts, heatmaps, and frequency analysis
- 💾 **Data Persistence** - Sessions auto-save and can be exported to CSV
- 🎮 **Game Modes** - Exact Match, Range Prediction, and High/Low

### Advanced Features
- 🔥 **Streak Tracking** - Monitor consecutive hits
- 🌡️ **Hot/Cold Numbers** - Identify frequently and rarely generated numbers
- ⏰ **Special Time Detection** - Special events at the 47th minute
- ✨ **Special Number (47)** - Track occurrences of the significant number
- 📜 **Session History** - View detailed history of all attempts
- 🎨 **Custom Styling** - Beautiful dark mode interface with animations

---

## 🚀 Quick Start

### Running Locally

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   streamlit run rng_mind_vs_machine.py
   ```

3. **Access in browser:**
   - Local: `http://localhost:8501`
   - Network: `http://<your-ip>:8501`

### Running in GitHub Codespaces

The application auto-starts when you open the Codespace!

1. Open this repository in GitHub Codespaces
2. Wait for the container to build
3. The app will automatically launch on port 8501
4. Access via the forwarded port (Codespaces will show you the URL)

---

## 📁 Project Structure

```
mindvsmachine/
├── src/
│   ├── __init__.py
│   ├── config.py           # Configuration constants
│   ├── rng_engine.py       # RNG algorithms and validation
│   ├── analytics.py        # Statistics and data analysis
│   └── ui_components.py    # Reusable UI elements
├── assets/
│   └── style.css           # Custom CSS styling
├── data/                   # Session data (gitignored)
│   ├── sessions.json
│   └── exports/
├── .devcontainer/          # Development container config
├── rng_mind_vs_machine.py  # Main application
└── requirements.txt        # Python dependencies
```

---

## 🎮 How to Use

### 1. **Configure Settings** (Sidebar)
   - Choose your RNG algorithm
   - Select game mode
   - Set number range (min/max)

### 2. **Make a Prediction**
   - Enter your predicted number
   - Focus your intention
   - Clear your mind

### 3. **Generate Number**
   - Click "Generate Number"
   - Observe the result
   - Check if you hit!

### 4. **Analyze Patterns**
   - View statistics dashboard
   - Study distribution charts
   - Look for hot/cold numbers
   - Track your accuracy

### 5. **Export Data**
   - Download sessions as CSV
   - Analyze externally
   - Share your results

---

## 🔧 RNG Algorithms

### Standard Python Random
- **Type:** Pseudo-random (Mersenne Twister)
- **Use Case:** General purpose randomness
- **Predictable:** Yes (given seed)

### Cryptographic Random
- **Type:** Cryptographically secure
- **Use Case:** High-entropy randomness
- **Predictable:** No (uses OS entropy)

### Time-Based Seed
- **Type:** Microsecond timestamp seeded
- **Use Case:** Temporal influence testing
- **Predictable:** Partially

---

## 📊 Statistics Explained

- **Total Attempts:** All number generations
- **Predictions:** Attempts where you made a prediction
- **Direct Hits:** Exact matches between prediction and result
- **Hit Rate:** Percentage of successful predictions
- **Current Streak:** Consecutive hits
- **Hot Numbers:** Most frequently generated
- **Cold Numbers:** Rarely or never generated

---

## 🔒 Security & Privacy

- ✅ XSRF protection enabled
- ✅ Data stored locally only
- ✅ No external data transmission
- ✅ Session data can be cleared anytime

---

## 🛠️ Development

### Requirements
- Python 3.8+
- Streamlit 1.28+
- Plotly 5.17+
- Pandas 2.0+

### Testing
Run the application in development mode:
```bash
streamlit run rng_mind_vs_machine.py --server.runOnSave true
```

---

## 📝 License

Open source - Use freely for research and experimentation.

---

## 🤔 The Experiment

This tool explores the fascinating question: **Can human consciousness influence random number generation?**

While mainstream science says no, anomalous cognition research suggests otherwise. Use this tool to:
- Test your intuition
- Look for statistical anomalies
- Track your "psychic" accuracy
- Explore observer effects

Remember: True randomness is rare. Patterns emerge. The question is whether you can influence them.

---

## 🌟 Special Features

### The 47th Minute
At 47 minutes past each hour, special detection is enabled. According to the "Simulation Protocol Fragment, Rev 2.3," this is when observer effects may be strongest.

### The Special Number
The number 47 holds special significance. Track how often it appears in your sessions.

---

**Focus your mind. Trust your intuition. Watch the patterns emerge.**

🧠 *The observer becomes the observed.* 🎲
