"""Definições compartilhadas pelos scripts do Artificial Analysis."""

from __future__ import annotations

import datetime as dt
import math
import re
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


# Tradução de família/variante, não um catálogo de versões ou disponibilidade.
CLI_MAPPING = {
    "claude-code": {"aliases": ("haiku", "sonnet", "opus", "fable"), "effort": "effort"},
    "codex": {"aliases": (), "effort": "model_reasoning_effort"},
}
EFFORT_SUFFIXES = {name.lower(): name.lower() for name in ("Low", "Medium", "High", "Xhigh", "Max", "Ultra")}


def finite_number(value) -> bool:
    try:
        return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)
    except OverflowError:
        return False


def validate_snapshot(payload: dict, require_date: bool = False) -> None:
    """Rejeita dados incompletos/inválidos antes de usá-los em decisões de custo."""
    if not isinstance(payload, dict) or not isinstance(payload.get("data"), list) or not payload["data"]:
        raise ValueError("data deve ser uma lista não vazia de modelos")
    if require_date:
        generated = payload.get("generated_at")
        if not isinstance(generated, str):
            raise ValueError("generated_at deve ser uma data ISO")
        day = dt.date.fromisoformat(generated)
        if day > dt.date.today():
            raise ValueError("generated_at está no futuro")
    seen = set()
    for model in payload["data"]:
        if not isinstance(model, dict):
            raise ValueError("modelo deve ser um objeto")
        for key in ("name", "slug"):
            if not isinstance(model.get(key), str) or not model[key].strip():
                raise ValueError(f"modelo sem {key}")
        if model["slug"] in seen:
            raise ValueError(f"slug duplicado: {model['slug']}")
        seen.add(model["slug"])
        for key in ("model_creator", "evaluations", "pricing", "performance", "performance_v3",
                    "artificial_analysis_intelligence_index_cost"):
            if model.get(key) is not None and not isinstance(model[key], dict):
                raise ValueError(f"{model['slug']}: {key} deve ser objeto")
        cost = model.get("artificial_analysis_intelligence_index_cost") or {}
        if cost.get("cost_per_task") is not None and not isinstance(cost["cost_per_task"], dict):
            raise ValueError("cost_per_task deve ser objeto")
        row = flatten(model)
        if not isinstance(row["creator"], str):
            raise ValueError("nome do criador deve ser texto")
        for key in ("in", "out", "cache", "cache_write", "per_task", "verbosity", "tps", "ttft", "ttfat", "e2e"):
            value = row[key]
            if value is not None and (not finite_number(value) or value < 0):
                raise ValueError(f"{model['slug']}: {key} deve ser número finito não negativo")
        for key, _, _ in CAPABILITIES:
            if row[key] is not None and not finite_number(row[key]):
                raise ValueError(f"{model['slug']}: {key} deve ser número finito")


def cli_parameters(row: dict, cli: str) -> str:
    """Parâmetros sugeridos; ausência de sufixo não implica esforço padrão ou Max."""
    mapping = CLI_MAPPING[cli]
    effort = None
    for value in (row["name"], row["slug"]):
        match = re.search(r"(?:^|[\s_\-(])(" + "|".join(EFFORT_SUFFIXES) + r")\)?$",
                          value, re.IGNORECASE)
        if match:
            effort = EFFORT_SUFFIXES[match.group(1).lower()]
            break
    model = row["slug"]
    if mapping["aliases"]:
        families = set(re.findall(r"[a-z]+", f"{row['name']} {row['slug']}".lower()))
        aliases = [alias for alias in mapping["aliases"] if alias in families]
        if len(aliases) != 1:
            return "não exposto nesta CLI"
        model = aliases[0]
    params = f"model={model}"
    if effort:
        return f"{params}; {mapping['effort']}={effort}"
    return f"{params} (esforço sem dados; confira na CLI)"


def num(value, digits=2) -> str:
    if value is None:
        return "—"
    if isinstance(value, (int, float)):
        return f"{value:.{digits}f}"
    return str(value)


def flatten(model: dict) -> dict:
    ev = model.get("evaluations") or {}
    price = model.get("pricing") or {}
    modern_perf = model.get("performance_v3")
    use_v3 = isinstance(modern_perf, dict)
    perf = modern_perf if use_v3 else model.get("performance") or {}
    prefix = "mean" if use_v3 else "median"
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
        "verbosity": (per_task / out_price * 1_000_000
                      if finite_number(per_task) and finite_number(out_price) and out_price > 0 else None),
        "tps": perf.get(f"{prefix}_output_tokens_per_second"),
        "ttft": perf.get(f"{prefix}_time_to_first_token_seconds"),
        "ttfat": perf.get(f"{prefix}_time_to_first_answer_token_seconds"),
        # v3 free não expõe a antiga resposta ponta a ponta de 500 tokens.
        "e2e": None if use_v3 else perf.get("median_end_to_end_response_time_seconds"),
        "perf_source": "média v3" if use_v3 else "mediana legada",
    }
    for key, _, field in CAPABILITIES:
        row[key] = ev.get(field)
    return row


def median_verbosity(rows: list[dict]) -> float | None:
    values = [r["verbosity"] for r in rows if r["verbosity"]]
    return statistics.median(values) if values else None


def profile_cost(row: dict, entrada: int, cache: float, saida: int, ref_verbosity: float | None):
    """Custo estimado em US$ de uma chamada no perfil, ou None sem preços."""
    if (not finite_number(entrada) or entrada < 0 or not finite_number(saida) or saida < 0
            or not finite_number(cache) or not 0 <= cache <= 1):
        raise ValueError("tokens devem ser não negativos e cache deve estar entre 0 e 1")
    if row["in"] is None or row["out"] is None:
        return None
    for key in ("in", "out", "cache", "cache_write", "verbosity"):
        value = row.get(key)
        if value is not None and (not finite_number(value) or value < 0):
            raise ValueError(f"{key} deve ser número finito não negativo")
    if ref_verbosity is not None and (not finite_number(ref_verbosity) or ref_verbosity <= 0):
        raise ValueError("verbosidade de referência deve ser positiva")
    new_tokens = entrada * (1 - cache)
    cached_tokens = entrada * cache
    write_price = row["cache_write"] if cache > 0 and row["cache_write"] is not None else row["in"]
    hit_price = row["cache"] if row["cache"] is not None else row["in"]
    factor = row["verbosity"] / ref_verbosity if row["verbosity"] and ref_verbosity else 1.0
    out_tokens = saida * factor
    return (new_tokens * write_price + cached_tokens * hit_price + out_tokens * row["out"]) / 1_000_000
