#!/usr/bin/env python3
"""Gera um retrato local e datado dos modelos de linguagem do Artificial Analysis.

Uso:
    python scripts/aa_snapshot.py                 # atualiza se o retrato tiver mais de 7 dias
    python scripts/aa_snapshot.py --force         # atualiza sempre
    python scripts/aa_snapshot.py --check         # só informa se o retrato existe e está válido
    python scripts/aa_snapshot.py --creators anthropic,openai --top 30

Requer a variável de ambiente AA_API_KEY (chave gratuita em
https://artificialanalysis.ai/api-key-management-redirect). Usa só a biblioteca padrão.
Cada execução com atualização consome 1 ou 2 das 100 requisições diárias do plano gratuito.

Saída: data/aa-snapshot.md na raiz da skill (ignorado pelo Git). Dados do Artificial
Analysis exigem atribuição e não devem ser redistribuídos sem contrato.

Códigos de saída: 0 ok ou retrato válido; 1 retrato ausente/vencido em --check;
2 sem chave; 3 erro de rede/HTTP; 4 resposta inesperada.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

API_URL = "https://artificialanalysis.ai/api/v2/language/models/free"
SKILL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = SKILL_ROOT / "data" / "aa-snapshot.md"
DATE_RE = re.compile(r"^Gerado em: (\d{4}-\d{2}-\d{2})", re.MULTILINE)
MAX_PAGES = 20


def snapshot_age_days(path: Path) -> int | None:
    if not path.exists():
        return None
    match = DATE_RE.search(path.read_text(encoding="utf-8"))
    if not match:
        return None
    generated = dt.date.fromisoformat(match.group(1))
    return (dt.date.today() - generated).days


def fetch_all(api_key: str) -> dict:
    models: list[dict] = []
    meta: dict = {}
    for page in range(1, MAX_PAGES + 1):
        req = urllib.request.Request(
            f"{API_URL}?page={page}",
            headers={"x-api-key": api_key, "Accept": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = json.load(resp)
        except urllib.error.HTTPError as exc:
            hint = ""
            if exc.code == 429:
                hint = f" (cota diária esgotada; Retry-After={exc.headers.get('Retry-After')}s)"
            elif exc.code in (401, 403):
                hint = " (chave inválida ou sem acesso)"
            print(f"Erro HTTP {exc.code}{hint}", file=sys.stderr)
            sys.exit(3)
        except urllib.error.URLError as exc:
            print(f"Erro de rede: {exc.reason}", file=sys.stderr)
            sys.exit(3)
        if not isinstance(body, dict) or not isinstance(body.get("data"), list):
            print("Resposta inesperada da API", file=sys.stderr)
            sys.exit(4)
        if page == 1:
            meta = {k: body.get(k) for k in ("tier", "intelligence_index_version")}
        models.extend(body["data"])
        if not (body.get("pagination") or {}).get("has_more"):
            break
    return {**meta, "data": models}


def num(value, digits=2) -> str:
    if value is None:
        return "—"
    if isinstance(value, (int, float)):
        return f"{value:.{digits}f}"
    return str(value)


def row(model: dict) -> dict:
    ev = model.get("evaluations") or {}
    price = model.get("pricing") or {}
    perf = model.get("performance") or {}
    cost = model.get("artificial_analysis_intelligence_index_cost") or {}
    per_task = (cost.get("cost_per_task") or {}).get("total_cost")
    intel = ev.get("artificial_analysis_intelligence_index")
    ratio = intel / per_task if intel is not None and per_task else None
    return {
        "name": model.get("name") or "?",
        "slug": model.get("slug") or "?",
        "creator": (model.get("model_creator") or {}).get("name") or "?",
        "release": model.get("release_date") or "—",
        "intel": intel,
        "eng": ev.get("artificial_analysis_engineering_index"),
        "per_task": per_task,
        "ratio": ratio,
        "in": price.get("price_1m_input_tokens"),
        "out": price.get("price_1m_output_tokens"),
        "cache": price.get("price_1m_cache_hit_tokens"),
        "tps": perf.get("median_output_tokens_per_second"),
        "ttfat": perf.get("median_time_to_first_answer_token_seconds"),
    }


def render(payload: dict, creators: list[str], top: int) -> str:
    rows = [row(m) for m in payload["data"]]
    if creators:
        wanted = [c.lower() for c in creators]
        rows = [r for r in rows if any(w in r["creator"].lower() for w in wanted)]
    rows = [r for r in rows if r["intel"] is not None]
    rows.sort(key=lambda r: r["intel"], reverse=True)
    rows = rows[:top]

    lines = [
        "# Retrato do Artificial Analysis",
        "",
        f"Gerado em: {dt.date.today().isoformat()}",
        f"Versão do Intelligence Index: {payload.get('intelligence_index_version')}",
        f"Plano da chave: {payload.get('tier')}",
        f"Filtro de criadores: {', '.join(creators) if creators else 'nenhum'}; "
        f"{len(rows)} modelos com índice publicado",
        "",
        "Fonte: [Artificial Analysis](https://artificialanalysis.ai/). Uso local; não redistribuir.",
        "",
        "Colunas: Intel = Intelligence Index; Eng = Engineering Index (capacidade);"
        " US$/tarefa = custo médio por tarefa do índice, já com tokens de raciocínio;"
        " Intel/US$ = pontos por dólar de tarefa (maior é melhor custo-benefício);"
        " preços em US$ por 1M tokens; tok/s e TTFAT (s até o primeiro token de resposta) medianos da API.",
        "",
        "| Modelo | Slug | Criador | Lançamento | Intel | Eng | US$/tarefa | Intel/US$ | Entrada | Saída | Cache | tok/s | TTFAT |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['name']} | {r['slug']} | {r['creator']} | {r['release']} | "
            f"{num(r['intel'], 1)} | {num(r['eng'], 1)} | {num(r['per_task'], 4)} | "
            f"{num(r['ratio'], 0)} | {num(r['in'])} | {num(r['out'])} | {num(r['cache'])} | "
            f"{num(r['tps'], 0)} | {num(r['ttfat'], 1)} |"
        )
    lines += [
        "",
        "Leitura: benchmarks medem a API do provedor, não a cobrança nem a latência da sua CLI."
        " Em assinatura ou proxy, use os custos como comparação relativa de consumo.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--max-age-days", type=int, default=7)
    parser.add_argument("--force", action="store_true", help="atualiza mesmo se válido")
    parser.add_argument("--check", action="store_true", help="só verifica idade, sem rede")
    parser.add_argument("--creators", default="", help="lista separada por vírgulas")
    parser.add_argument("--top", type=int, default=60)
    parser.add_argument("--from-file", type=Path, help="usa JSON salvo em vez da API (testes)")
    args = parser.parse_args()

    age = snapshot_age_days(args.out)
    fresh = age is not None and age <= args.max_age_days
    if args.check:
        state = "ausente" if age is None else f"{age} dia(s)"
        print(f"{args.out}: {state}; {'válido' if fresh else 'vencido ou ausente'}")
        return 0 if fresh else 1
    if fresh and not args.force and not args.from_file:
        print(f"Retrato válido ({age} dia(s)); nada a fazer. Use --force para atualizar.")
        return 0

    if args.from_file:
        payload = json.loads(args.from_file.read_text(encoding="utf-8"))
    else:
        api_key = os.environ.get("AA_API_KEY")
        if not api_key:
            print("Defina AA_API_KEY (chave gratuita do Artificial Analysis).", file=sys.stderr)
            return 2
        payload = fetch_all(api_key)

    creators = [c.strip() for c in args.creators.split(",") if c.strip()]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render(payload, creators, args.top), encoding="utf-8")
    print(f"Retrato salvo em {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
