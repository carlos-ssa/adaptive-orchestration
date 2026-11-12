"""Definições compartilhadas pelos scripts do Artificial Analysis."""

from __future__ import annotations

import statistics
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# (chave curta, rótulo, campo em evaluations)
CAPABILITIES = [
    ("intel", "Intel", "artificial_analysis_intelligence_index"),
    ("eng", "Eng", "artificial_analysis_engineering_index"),
    ("fin", "Fin", "artificial_analysis_finance_and_accounting_index"),
    ("estr", "Estr", "artificial_analysis_strategy_and_ops_index"),
    ("jur", "Jur", "artificial_analysis_legal_index"),
    ("saude", "Saúde", "artificial_analysis_healthcare_and_medical_index"),
    ("econ", "Econ", "artificial_analysis_economics_index"),
]

# Perfis de uso ilustrativos por chamada delegada. Ajuste com --entrada, --cache e --saida.
# "saida" é a saída de um modelo de verbosidade mediana; cada modelo é escalado pela sua.
PROFILES = {
    "leitura": {"entrada": 200_000, "cache": 0.50, "saida": 4_000,
                "desc": "ler arquivos ou logs e devolver resumo"},
    "codigo": {"entrada": 150_000, "cache": 0.85, "saida": 15_000,
               "desc": "alteração delimitada com testes, várias rodadas"},
    "agente": {"entrada": 1_000_000, "cache": 0.90, "saida": 30_000,
               "desc": "sessão longa com muitas rodadas e contexto reenviado"},
    "geracao": {"entrada": 10_000, "cache": 0.0, "saida": 20_000,
                "desc": "escrever texto ou código novo a partir de pouco contexto"},
}


def num(value, digits=2) -> str:
    if value is None:
        return "—"
    if isinstance(value, (int, float)):
        return f"{value:.{digits}f}"
    return str(value)


def flatten(model: dict) -> dict:
    ev = model.get("evaluations") or {}
    price = model.get("pricing") or {}
    perf = model.get("performance") or {}
    cost = model.get("artificial_analysis_intelligence_index_cost") or {}
    per_task = (cost.get("cost_per_task") or {}).get("total_cost")
    out_price = price.get("price_1m_output_tokens")
    row = {
        "name": model.get("name") or "?",
        "slug": model.get("slug") or "?",
        "creator": (model.get("model_creator") or {}).get("name") or "?",
        "release": model.get("release_date") or "—",
        "in": price.get("price_1m_input_tokens"),
        "cache": price.get("price_1m_cache_hit_tokens"),
        "cache_write": price.get("price_1m_cache_write_tokens"),
        "out": out_price,
        "per_task": per_task,
        # Limite superior: o custo por tarefa inclui a entrada, atribuída aqui à saída.
        "verbosity": per_task / out_price * 1_000_000 if per_task and out_price else None,
        "tps": perf.get("median_output_tokens_per_second"),
        "ttft": perf.get("median_time_to_first_token_seconds"),
        "ttfat": perf.get("median_time_to_first_answer_token_seconds"),
        "e2e": perf.get("median_end_to_end_response_time_seconds"),
    }
    for key, _, field in CAPABILITIES:
        row[key] = ev.get(field)
    return row


def median_verbosity(rows: list[dict]) -> float | None:
    values = [r["verbosity"] for r in rows if r["verbosity"]]
    return statistics.median(values) if values else None


def profile_cost(row: dict, entrada: int, cache: float, saida: int, ref_verbosity: float | None):
    """Custo estimado em US$ de uma chamada no perfil, ou None sem preços."""
    if row["in"] is None or row["out"] is None:
        return None
    new_tokens = entrada * (1 - cache)
    cached_tokens = entrada * cache
    write_price = row["cache_write"] if cache > 0 and row["cache_write"] is not None else row["in"]
    hit_price = row["cache"] if row["cache"] is not None else row["in"]
    factor = row["verbosity"] / ref_verbosity if row["verbosity"] and ref_verbosity else 1.0
    out_tokens = saida * factor
    return (new_tokens * write_price + cached_tokens * hit_price + out_tokens * row["out"]) / 1_000_000
