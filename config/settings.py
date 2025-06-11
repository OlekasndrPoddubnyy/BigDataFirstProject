# config/settings.py

import os
from dotenv import load_dotenv

# Carica variabili da .env (solo se esiste)
load_dotenv()

# === Modalità applicazione ===
# Se TEST_APP è 'ON', si usa la modalità test con job statici
TEST_APP = os.getenv("TEST_APP", "ON").upper() == "ON"

# === OpenAI API Key ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# === Log Level default per Spark ===
SPARK_LOG_LEVEL = os.getenv("SPARK_LOG_LEVEL", "WARN")
