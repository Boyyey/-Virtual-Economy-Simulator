# 🌍💡 Virtual Economy Simulator

A toy universe for economics experiments: simulate thousands of AI-powered agents making economic decisions, reacting to news, and creating emergent phenomena like booms, busts, and inequality.

---

## 📝 Project Summary

Build a simulated “virtual economy” of thousands (or millions) of agents. Each agent is powered by a small language model (LLM) or rule-based AI, which can:
- 📰 Read market news / policies
- 💸 Decide what to buy, sell, save, invest, or produce
- 😱 React to panic or optimism

The system shows emergent phenomena like market crashes, bubbles, inequality, or recessions — even though no agent is explicitly programmed to cause them.

## 🚀 Features
- Agent-based model (ABM) with wealth, income, risk, and memory
- Agents reason via LLMs or rule-based logic
- Dynamic market with prices, shocks, and policy changes
- Emergent phenomena: booms, busts, inequality
- Policy layer: UBI, taxes, regulation
- **Interactive Streamlit dashboard**: configure, run, and visualize simulations in your browser
- Download results as CSV for further analysis
- Add custom news and policy events

## 🧰 Tech Stack
- **ABM:** Python, Mesa, agentpy
- **LLM:** OpenAI API, local models (Phi-3, CodeLlama, Mistral)
- **Visualization:** matplotlib, plotly, bokeh, Streamlit
- **Data storage:** CSV / SQLite
- **Frontend:** Streamlit dashboard

## ⚙️ Setup
1. Clone the repo
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ How to Run

1. **Launch the interactive dashboard:**
   ```bash
   streamlit run dashboard.py
   ```
   This opens a web UI where you can configure all simulation parameters, run/pause/reset the simulation, and visualize results live.

2. **Configure and experiment:**
   - Use the sidebar to set the number of agents, businesses, rounds, risk profiles, LLM options, and policy toggles (UBI, taxes, shocks, etc.).
   - Add custom news or policy events.
   - Start, pause, or reset the simulation at any time.
   - Download results (wealth, prices, Gini) as CSV for your own analysis.

## 🧪 Advanced Features
- **Live parameter tweaking:** Change simulation settings and rerun instantly.
- **Policy experiments:** Toggle UBI, wealth tax, and market shocks in real time.
- **Custom news/events:** Inject your own news headlines or policy changes.
- **LLM integration:** Use OpenAI or local models for agent reasoning (set API key in the dashboard).
- **Downloadable data:** Export all results for further research or visualization.

## 📊 Usage Tips
- All simulation control is now through the dashboard—no need to run `main.py` directly.
- For large simulations, increase the number of agents and rounds in the sidebar.
- Use the download buttons to save your experiment results.
- For LLM-powered agents, enter your API key and model in the sidebar.

---

Made with ❤️ for economics, AI, and complexity science. 