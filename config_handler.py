import json
import os

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "custo_furo_adicional": 5.00,
    "custo_corte_adicional": 6.00,
    "custo_vinco_adicional": 6.00
}

def load_config():
    """Carrega a configuração a partir do arquivo CONFIG_FILE; se não existir, retorna os valores padrão."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return DEFAULT_CONFIG.copy()

def save_config(config):
    """Salva a configuração no arquivo CONFIG_FILE."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
