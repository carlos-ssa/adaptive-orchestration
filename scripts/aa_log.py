#!/usr/bin/env python3
"""Registra resultados locais de blocos e resume a calibração por faixa/tipo/modelo.

Uso:
    python scripts/aa_log.py --faixa 2 --tipo codigo --modelo executor --esforco medium --resultado aceito
    python scripts/aa_log.py --resumo

Grava data/calibracao.jsonl (ignorado pelo Git). --consumo aceita texto com unidade,
como "1200 tokens"; não estima nem converte cota em dinheiro. Sem rede.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from aa_common import DATA_DIR  # noqa: E402

RESULTS = ("aceito", "corrigido", "refeito")
REASONS = ("capacidade", "contexto", "acesso", "ferramenta", "infra")


def iso_date(value: str) -> str:
    try:
        return dt.date.fromisoformat(value).isoformat()
    except ValueError:
        raise argparse.ArgumentTypeError("use data ISO: AAAA-MM-DD")


def nonempty(value: str) -> str:
    if not value.strip():
        raise argparse.ArgumentTypeError("o valor não pode ser vazio")
    return value.strip()


def validate_record(row: dict) -> None:
    if not isinstance(row, dict):
        raise ValueError("registro deve ser objeto")
    if type(row.get("faixa")) is not int or row["faixa"] not in range(4):
        raise ValueError("faixa deve ser inteiro de 0 a 3")
    for key in ("data", "tipo", "modelo", "esforco"):
        if not isinstance(row.get(key), str) or not row[key].strip():
            raise ValueError(f"{key} deve ser texto não vazio")
    try:
        iso_date(row["data"])
    except argparse.ArgumentTypeError as exc:
        raise ValueError(str(exc)) from exc
    if row.get("resultado") not in RESULTS:
        raise ValueError("resultado inválido")
    if row["resultado"] == "aceito":
        if row.get("motivo") is not None:
            raise ValueError("aceito não deve ter motivo")
    elif row.get("motivo") not in REASONS:
        raise ValueError("corrigido/refeito exige motivo válido")
    if "consumo" in row and (not isinstance(row["consumo"], str) or not row["consumo"].strip()):
        raise ValueError("consumo deve ser texto com unidade")


def summarize(path: Path) -> None:
    groups = defaultdict(Counter)
    failures = Counter()
    if path.exists():
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
                validate_record(row)
                key = (row["faixa"], row["tipo"], row["modelo"])
                result = row["resultado"]
                if result not in RESULTS:
                    raise ValueError("resultado inválido")
                groups[key][result] += 1
                if result != "aceito" and row.get("motivo") == "capacidade":
                    failures[key[:2]] += 1
            except (ValueError, KeyError, TypeError) as exc:
                raise ValueError(f"linha {line_number} inválida: {exc}") from exc
    if not groups:
        print("Nenhum bloco registrado.")
        return
    print("| Faixa | Tipo | Modelo | Aceito | Corrigido | Refeito |")
    print("|---|---|---|---|---|---|")
    for (tier, kind, model), counts in sorted(groups.items()):
        print(f"| {tier} | {kind} | {model} | {counts['aceito']} | {counts['corrigido']} | {counts['refeito']} |")
    # O piso vale para a faixa/tipo, mesmo quando as falhas vieram de modelos distintos.
    for (tier, kind), count in sorted(failures.items()):
        if count >= 2:
            print(f"Faixa {tier} / {kind}: {count} falhas por capacidade → elevar piso.")


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--arquivo", type=Path, default=DATA_DIR / "calibracao.jsonl")
    parser.add_argument("--resumo", action="store_true", help="só lê e agrega os registros")
    parser.add_argument("--data", type=iso_date, default=dt.date.today().isoformat())
    parser.add_argument("--faixa", type=int, choices=range(4))
    parser.add_argument("--tipo", type=nonempty, help="tipo de tarefa, ex.: codigo ou extracao")
    parser.add_argument("--modelo", type=nonempty)
    parser.add_argument("--esforco", type=nonempty, help="valor efetivo ou 'não exposto'")
    parser.add_argument("--resultado", choices=RESULTS)
    parser.add_argument("--motivo", choices=REASONS)
    parser.add_argument("--consumo", type=nonempty, help="consumo observado, com unidade")
    args = parser.parse_args()

    if not args.resumo:
        for name in ("faixa", "tipo", "modelo", "esforco", "resultado"):
            if getattr(args, name) is None:
                parser.error(f"--{name} é obrigatório para registrar")
        if args.resultado != "aceito" and args.motivo is None:
            parser.error("--motivo é obrigatório quando o resultado não é aceito")
        if args.resultado == "aceito" and args.motivo is not None:
            parser.error("--motivo só se aplica a corrigido ou refeito")

    try:
        if args.resumo:
            summarize(args.arquivo)
        else:
            row = {name: getattr(args, name) for name in
                   ("data", "faixa", "tipo", "modelo", "esforco", "resultado")}
            for name in ("motivo", "consumo"):
                if getattr(args, name) is not None:
                    row[name] = getattr(args, name)
            args.arquivo.parent.mkdir(parents=True, exist_ok=True)
            # Uma escrita binária evita fundir o registro com a última linha sem LF.
            with args.arquivo.open("a+b") as stream:
                stream.seek(0, 2)
                prefix = b""
                if stream.tell():
                    stream.seek(-1, 2)
                    if stream.read(1) != b"\n":
                        prefix = b"\n"
                stream.write(prefix + (json.dumps(row, ensure_ascii=False) + "\n").encode("utf-8"))
            print(f"Bloco registrado em {args.arquivo}")
    except (OSError, ValueError) as exc:
        print(f"Erro na calibração: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
