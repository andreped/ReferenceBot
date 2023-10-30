---
title: "ReferenceBot: KnowledgeGPT + Azure OpenAI = <3"
colorFrom: indigo
colorTo: indigo
sdk: streamlit
sdk_version: 1.27.2
app_port: 8501
emoji: 💬
pinned: false
license: mit
app_file: knowledge_gpt/main.py
---

# [ReferenceBot](https://github.com/andreped/referencebot#referencebot)

[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://referencebot.streamlit.app)

# [Installation](https://github.com/andreped/referencebot#installation)

Follow the instructions below to run the Streamlit server locally.

### [Prerequisites](https://github.com/andreped/referencebot#prerequisites)

Make sure you have Python `≥3.10` installed.

### [Steps](https://github.com/andreped/referencebot#steps)

These instructions were tested on macOS 13.6 Ventura with ARM CPU and Python `3.10.11`.

1. Clone the repository:

```bash
git clone https://github.com/andreped/ReferenceBot
cd ReferenceBot
```

2. Setup virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Create the secrets file at `.streamlit/secrets.toml` and fill in the relevant info:

```bash
OPENAI_API_KEY = "<insert OpenAI API key>"
CHATGPT_MODEL = "<insert model name>"
OPENAI_API_BASE = "https://<insert-openai-service-name>.openai.azure.com"
OPENAI_API_VERSION = "<insert version>"
ENGINE = "<insert deployment model name>"
ENGINE_EMBEDDING = "<insert deployment embedding name>"
```

4. Run the Streamlit server

```bash
streamlit run knowledge_gpt/main.py
```

# [Build with Docker](https://github.com/andreped/referencebot#build-with-docker)

Run the following commands to build and run the Docker image.

```bash
cd knowledge_gpt
docker build -t ReferenceBot .
docker run -p 8501:8501 ReferenceBot
```

Open http://localhost:8501 in your browser to access the app.

## [Acknowledgements](https://github.com/andreped/referencebot#acknowledgements)

We have built on-top of [KnowledgeGPT](https://github.com/mmz-001/knowledge_gpt) to enable the tool be be used with Azure OpenAI Services. Thus, all credit should go towards the original developers.

## [License](https://github.com/andreped/referencebot#license)

Distributed under the MIT License. See [LICENSE](https://github.com/andreped/ReferenceBot/blob/main/LICENSE) for more information.
