# 🚀 ERP Trend Agent

A powerful multi-agent system built with **AutoGen** and **Streamlit** for analyzing ERP industry trends. This application uses 4 specialized AI agents working in a Round Robin Group Chat to research, write, optimize, and verify trending news content.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![AutoGen](https://img.shields.io/badge/AutoGen-0.4.8-purple.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40-red.svg)

## ✨ Features

- **🔍 Trend Collector Agent**: Researches and identifies the latest ERP industry trends
- **✍️ Content Writer Agent**: Creates engaging, well-structured content
- **🚀 SEO Optimizer Agent**: Optimizes content for search engine visibility
- **✅ Fact Checker Agent**: Verifies accuracy and provides credibility scores

### UI Features

- 🎨 Modern, dark-themed UI with gradient accents
- 📊 Real-time workflow visualization
- 📈 Interactive pie charts and bar graphs for credibility scores
- 🔄 Live agent progress tracking
- 📋 Detailed output for each agent step

## 🛠️ Installation

### Prerequisites

- Python 3.10 or higher
- OpenAI API key

### Setup

1. **Clone the repository**
   ```bash
   cd /Users/jameer-15545/StudioProjects/genai/trendAgent
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp env.template .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your-actual-api-key-here
   OPENAI_MODEL=gpt-4o-mini  # or gpt-4o for better results
   ```

## 🚀 Usage

1. **Start the application**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser** at `http://localhost:8501`

3. **Enter a topic** (optional) or leave blank for general ERP trends

4. **Click "Analyze Trends"** to start the multi-agent workflow

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Round Robin Group Chat                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│   │  Trend   │───▶│ Content  │───▶│   SEO    │───▶│   Fact   │
│   │Collector │    │  Writer  │    │Optimizer │    │ Checker  │
│   └──────────┘    └──────────┘    └──────────┘    └──────────┘
│       🔍              ✍️              🚀              ✅      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Agent Workflow

1. **TrendCollector** → Researches ERP trends and news
2. **ContentWriter** → Creates engaging article content
3. **SEOOptimizer** → Optimizes for search engines
4. **FactChecker** → Verifies and scores credibility

## 📁 Project Structure

```
trendAgent/
├── app.py              # Main Streamlit application
├── agents.py           # AutoGen agent definitions
├── requirements.txt    # Python dependencies
├── env.template        # Environment template (copy to .env)
├── .env               # Your API keys (create from template)
└── README.md          # This file
```

## 📊 Credibility Scoring

The Fact Checker agent provides detailed credibility analysis:

| Category | Weight | Description |
|----------|--------|-------------|
| Factual Accuracy | 40% | Verifies claims and statistics |
| Source Credibility | 25% | Assesses reliability of sources |
| Content Quality | 20% | Checks logical consistency |
| Timeliness | 15% | Verifies information currency |

## 🎨 UI Theme

The application features a stunning dark theme with:
- **Primary**: Indigo (#6366f1)
- **Secondary**: Purple (#8b5cf6)
- **Accent**: Cyan (#06b6d4)
- **Success**: Emerald (#10b981)

## 🔧 Configuration Options

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `OPENAI_API_KEY` | Required | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-4o-mini` | Model to use for agents |

## 📝 Example Topics

- "SAP S/4HANA Cloud migration trends"
- "Oracle NetSuite AI capabilities"
- "Microsoft Dynamics 365 updates"
- "ERP and Industry 4.0 integration"
- Leave blank for general ERP trends

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

MIT License - feel free to use this project for your own purposes.

## 🙏 Acknowledgments

- [Microsoft AutoGen](https://github.com/microsoft/autogen) - Multi-agent framework
- [Streamlit](https://streamlit.io/) - Web application framework
- [Plotly](https://plotly.com/) - Interactive visualizations
