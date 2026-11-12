#!/usr/bin/env python3
"""Lista candidatos para uma tarefa cruzando capacidade, custo do perfil de uso e velocidade.

Exemplos:
    python scripts/aa_rank.py --perfil leitura --creators anthropic,openai
    python scripts/aa_rank.py --perfil codigo --capacidade eng --min 55
    python scripts/aa_rank.py --perfil codigo --capacidade eng --ref claude-opus-5-5-high --pct 90
    python scripts/aa_rank.py --perfil agente --min 45 --max-ttfat 30 --ordem valor
    python scripts/aa_rank.py --entrada 50000 --cache 0.7 --saida 8000 --capacidade jur

Lê data/aa-snapshot.json (gere com scripts/aa_snapshot.py). Sem rede.
--ref e --pct definem o piso relativo ao modelo principal, que acompanha novas versões sem
fixar nomes. Ordem "custo": o mais barato entre os que atingem o piso. Ordem "valor": mais pontos por dólar.
O nome da variante (Low, Medium, High...) indica o esforço a usar na CLI.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from aa_common import CAPABILITIES, DATA_DIR, PROFILES, flatten, median_verbosity, num, profile_cost  # noqa: E402


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    caps = {key: label for key, label, _ in CAPABILITIES}
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--perfil", choices=PROFILES, default="leitura")
    parser.add_argument("--entrada", type=int, help="tokens de entrada (substitui o perfil)")
    parser.add_argument("--cache", type=float, help="fração da entrada lida do cache, 0 a 1")
    parser.add_argument("--saida", type=int, help="tokens de saída de um modelo mediano")
    parser.add_argument("--capacidade", choices=caps, default="intel",
                        help="índice que importa para a tarefa")
    parser.add_argument("--min", type=float, default=0, help="nota mínima na capacidade")
    parser.add_argument("--ref", help="slug do modelo principal, para piso relativo")
    parser.add_argument("--pct", type=float, default=90, help="piso em %% da nota do --ref")
    parser.add_argument("--creators", default="", help="ex.: anthropic,openai")
    parser.add_argument("--max-ttfat", type=float, help="segundos máximos até a resposta")
    parser.add_argument("--min-tps", type=float, help="tokens/s mínimos")
    parser.add_argument("--ordem", choices=("custo", "valor"),
                        help="padrão: custo com --min, valor sem --min")
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--snapshot", type=Path, default=DATA_DIR / "aa-snapshot.json")
    args = parser.parse_args()

    if not args.snapshot.exists():
        print("Retrato ausente. Rode: python scripts/aa_snapshot.py", file=sys.stderr)
        return 1
    snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
    profile = dict(PROFILES[args.perfil])
    for key in ("entrada", "cache", "saida"):
        if getattr(args, key) is not None:
            profile[key] = getattr(args, key)

    rows = [flatten(m) for m in snapshot["data"]]
    ref = median_verbosity(rows)
    cap = args.capacidade
    ref_row = None
    if args.ref:
        matches = [r for r in rows if r["slug"] == args.ref] or [r for r in rows if args.ref in r["slug"]]
        if len(matches) != 1:
            names = ", ".join(r["slug"] for r in matches[:10]) or "nenhum"
            print(f"--ref deve identificar um modelo; encontrados: {names}", file=sys.stderr)
            return 1
        ref_row = matches[0]
        if ref_row[cap] is None:
            print(f"{ref_row['slug']} não tem nota em {cap}", file=sys.stderr)
            return 1
        args.min = max(args.min, ref_row[cap] * args.pct / 100)
    if args.creators:
        wanted = [c.strip().lower() for c in args.creators.split(",") if c.strip()]
        rows = [r for r in rows if any(w in r["creator"].lower() for w in wanted)]
    if args.ordem is None:
        args.ordem = "custo" if args.min > 0 else "valor"
    excluded = {"sem nota": 0, "abaixo do mínimo": 0, "sem preço": 0, "lento": 0}
    candidates = []
    for r in rows:
        if r[cap] is None:
            excluded["sem nota"] += 1
            continue
        if r[cap] < args.min:
            excluded["abaixo do mínimo"] += 1
            continue
        if (args.max_ttfat is not None and (r["ttfat"] is None or r["ttfat"] > args.max_ttfat)) or (
            args.min_tps is not None and (r["tps"] is None or r["tps"] < args.min_tps)
        ):
            excluded["lento"] += 1
            continue
        cost = profile_cost(r, profile["entrada"], profile["cache"], profile["saida"], ref)
        if cost is None:
            excluded["sem preço"] += 1
            continue
        r["profile_cost"] = cost
        r["value"] = r[cap] / cost if cost else None
        candidates.append(r)

    if args.ordem == "custo":
        candidates.sort(key=lambda r: (r["profile_cost"], -r[cap]))
    else:
        candidates.sort(key=lambda r: -(r["value"] or 0))

    label = caps[cap]
    intel_h, intel_sep = ("", "") if cap == "intel" else (" Intel |", "---|")
    print(
        f"Retrato de {snapshot['generated_at']} · perfil {args.perfil}: {profile['entrada']:,} tokens de entrada,"
        f" {profile['cache']:.0%} do cache, {profile['saida']:,} de saída (modelo mediano)"
        f" · capacidade {label} ≥ {args.min:.1f} · ordem por {args.ordem}"
    )
    if ref_row:
        cost = profile_cost(ref_row, profile["entrada"], profile["cache"], profile["saida"], ref)
        print(f"Piso: {args.pct:g}% de {ref_row['name']} ({num(ref_row[cap], 1)} em {label}),"
              f" que custaria US$ {num(cost, 4)} neste perfil")
    print(f"Excluídos: {', '.join(f'{v} {k}' for k, v in excluded.items() if v) or 'nenhum'}")
    print()
    print(f"| Modelo | Slug | {label} |{intel_h} US$ no perfil | {label}/US$ | US$/tarefa | Saída/tarefa (mil) | tok/s | 1º token de resposta (s) |")
    print("|---|---|---|" + intel_sep + "---|" * 6)
    for r in candidates[: args.top]:
        verb = r["verbosity"] / 1000 if r["verbosity"] else None
        print(
            f"| {r['name']} | {r['slug']} | {num(r[cap], 1)} |"
            + ("" if cap == "intel" else f" {num(r['intel'], 1)} |")
            + f" {num(r['profile_cost'], 4)} | "
            f"{num(r['value'], 0)} | {num(r['per_task'], 4)} | {num(verb, 0)} | {num(r['tps'], 0)} | {num(r['ttfat'], 1)} |"
        )
    print()
    print("Estimativas a partir de preços e verbosidade publicados pelo Artificial Analysis;"
          " confira disponibilidade, contexto, modalidades e ferramentas na CLI antes de escolher.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
