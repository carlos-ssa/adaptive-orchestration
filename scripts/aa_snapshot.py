#!/usr/bin/env python3
"""Gera um retrato local e datado dos modelos de linguagem do Artificial Analysis.

Uso:
    python scripts/aa_snapshot.py            # atualiza se o retrato tiver mais de 7 dias
    python scripts/aa_snapshot.py --force    # atualiza sempre
    python scripts/aa_snapshot.py --check    # só informa se o retrato existe e está válido

Requer a variável de ambiente AA_API_KEY (chave gratuita em
https://artificialanalysis.ai/api-key-management-redirect). Usa só a biblioteca padrão.
Cada atualização consome cerca de 4 das 100 requisições diárias do plano gratuito.

Saída, na pasta data/ da skill (ignorada pelo Git):
- aa-snapshot.json: todos os campos do plano gratuito, consultado por scripts/aa_rank.py;
- aa-snapshot.md: tabelas de capacidade, custo e velocidade para leitura humana.
Dados do Artificial Analysis exigem atribuição e não devem ser redistribuídos sem contrato.

Códigos de saída: 0 ok ou retrato válido; 1 retrato ausente/vencido em --check;
2 sem chave; 3 erro de rede/HTTP; 4 resposta inesperada.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from aa_common import CAPABILITIES, DATA_DIR, flatten, num  # noqa: E402

API_URL = "https://artificialanalysis.ai/api/v2/language/models/free"
MAX_PAGES = 20


def snapshot_age_days(path: Path) -> int | None:
    if not path.exists():
        return None
    try:
        generated = json.loads(path.read_text(encoding="utf-8"))["generated_at"]
    except (ValueError, KeyError):
        return None
    return (dt.date.today() - dt.date.fromisoformat(generated)).days


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


def render_markdown(snapshot: dict, creators: list[str]) -> str:
    rows = [flatten(m) for m in snapshot["data"]]
    if creators:
        wanted = [c.lower() for c in creators]
        rows = [r for r in rows if any(w in r["creator"].lower() for w in wanted)]
    rows = [r for r in rows if r["intel"] is not None]
    rows.sort(key=lambda r: r["intel"], reverse=True)

    cap_header = " | ".join(label for _, label, _ in CAPABILITIES)
    lines = [
        "# Retrato do Artificial Analysis",
        "",
        f"Gerado em: {snapshot['generated_at']} · Intelligence Index v{snapshot.get('intelligence_index_version')}"
        f" · plano {snapshot.get('tier')} · {len(rows)} modelos com índice"
        f" · criadores: {', '.join(creators) if creators else 'todos'}",
        "",
        "Fonte: [Artificial Analysis](https://artificialanalysis.ai/). Uso local; não redistribuir."
        " Para escolher, prefira `python scripts/aa_rank.py`, que cruza capacidade, custo e velocidade.",
        "",
        "## Capacidade",
        "",
        "Intel = Intelligence Index geral. As demais são os Capability Indexes por área.",
        "",
        f"| Modelo | Criador | Lançamento | {cap_header} |",
        "|---|---|---|" + "---|" * len(CAPABILITIES),
    ]
    for r in rows:
        caps = " | ".join(num(r[key], 1) for key, _, _ in CAPABILITIES)
        lines.append(f"| {r['name']} | {r['creator']} | {r['release']} | {caps} |")

    lines += [
        "",
        "## Custo",
        "",
        "Preços em US$ por 1M tokens. US$/tarefa = custo médio por tarefa do Intelligence Index."
        " Saída/tarefa = estimativa (limite superior) de tokens gerados por tarefa, incluindo"
        " raciocínio: mede a verbosidade.",
        "",
        "| Modelo | Entrada | Cache (leitura) | Cache (gravação) | Saída | US$/tarefa | Saída/tarefa (mil tok) |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        verb = r["verbosity"] / 1000 if r["verbosity"] else None
        lines.append(
            f"| {r['name']} | {num(r['in'])} | {num(r['cache'], 3)} | {num(r['cache_write'], 3)} | "
            f"{num(r['out'])} | {num(r['per_task'], 4)} | {num(verb, 0)} |"
        )

    lines += [
        "",
        "## Velocidade",
        "",
        "Medianas da API do provedor: tokens de saída por segundo, segundos até o primeiro token,"
        " até o primeiro token de resposta (após o raciocínio) e resposta completa de 500 tokens.",
        "",
        "| Modelo | tok/s | 1º token | 1º token de resposta | Ponta a ponta |",
        "|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['name']} | {num(r['tps'], 0)} | {num(r['ttft'], 1)} | {num(r['ttfat'], 1)} | {num(r['e2e'], 1)} |"
        )
    lines += [
        "",
        "Benchmarks medem a API do provedor, não a cobrança nem a latência da sua CLI."
        " Em assinatura ou proxy, use os custos como comparação relativa de consumo.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dir", type=Path, default=DATA_DIR, help="pasta de saída")
    parser.add_argument("--max-age-days", type=int, default=7)
    parser.add_argument("--force", action="store_true", help="atualiza mesmo se válido")
    parser.add_argument("--check", action="store_true", help="só verifica idade, sem rede")
    parser.add_argument("--creators", default="", help="filtra o Markdown; o JSON guarda todos")
    parser.add_argument("--from-file", type=Path, help="usa JSON salvo em vez da API (testes)")
    args = parser.parse_args()

    json_path = args.dir / "aa-snapshot.json"
    age = snapshot_age_days(json_path)
    fresh = age is not None and age <= args.max_age_days
    if args.check:
        state = "ausente" if age is None else f"{age} dia(s)"
        print(f"{json_path}: {state}; {'válido' if fresh else 'vencido ou ausente'}")
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

    snapshot = {
        "generated_at": dt.date.today().isoformat(),
        "source": "https://artificialanalysis.ai/",
        "tier": payload.get("tier"),
        "intelligence_index_version": payload.get("intelligence_index_version"),
        "data": payload["data"],
    }
    creators = [c.strip() for c in args.creators.split(",") if c.strip()]
    args.dir.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(snapshot, ensure_ascii=False), encoding="utf-8")
    (args.dir / "aa-snapshot.md").write_text(render_markdown(snapshot, creators), encoding="utf-8")
    print(f"Retrato salvo em {args.dir} ({len(snapshot['data'])} modelos)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
