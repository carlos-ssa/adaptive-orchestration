"""Registros sintéticos em diretório temporário dentro do repositório."""

import datetime as dt
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix=".test-log-", dir=ROOT)
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "local" / "calibracao.jsonl"

    def run_log(self, *args, code=0):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "aa_log.py"), "--arquivo", str(self.path), *args],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
        )
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return result

    def record(self, result="aceito", reason=None, model="executor-A", tier=2, kind="codigo", extra=()):
        args = ["--faixa", str(tier), "--tipo", kind, "--modelo", model,
                "--esforco", "medium", "--resultado", result]
        if reason:
            args += ["--motivo", reason]
        return self.run_log(*args, *extra)

    def test_append_preserves_fields_and_optional_consumption(self):
        self.record(extra=("--data", "2026-01-02", "--consumo", "1200 tokens"))
        self.record("corrigido", "capacidade")
        rows = [json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines()]
        self.assertEqual(rows[0], {
            "data": "2026-01-02", "faixa": 2, "tipo": "codigo", "modelo": "executor-A",
            "esforco": "medium", "resultado": "aceito", "consumo": "1200 tokens",
        })
        self.assertEqual(rows[1]["data"], dt.date.today().isoformat())
        self.assertEqual(rows[1]["motivo"], "capacidade")
        self.assertNotIn("consumo", rows[1])

    def test_summary_counts_results_across_efforts_without_writing(self):
        self.record()
        self.record("corrigido", "capacidade")
        self.record("refeito", "capacidade", extra=("--esforco", "high"))
        before = self.path.read_bytes()
        output = self.run_log("--resumo").stdout
        self.assertIn("| 2 | codigo | executor-A | 1 | 1 | 1 |", output)
        self.assertIn("2 falhas por capacidade → elevar piso", output)
        self.assertEqual(before, self.path.read_bytes())

    def test_capacity_threshold_combines_models_but_separates_tier_and_type(self):
        self.record("corrigido", "capacidade", model="executor-A")
        self.record("refeito", "capacidade", model="executor-B")
        self.record("corrigido", "capacidade", tier=1)
        self.record("corrigido", "capacidade", kind="extracao")
        output = self.run_log("--resumo").stdout
        self.assertIn("| 2 | codigo | executor-A | 0 | 1 | 0 |", output)
        self.assertIn("| 2 | codigo | executor-B | 0 | 0 | 1 |", output)
        self.assertIn("Faixa 2 / codigo: 2 falhas por capacidade → elevar piso", output)
        self.assertEqual(output.count("elevar piso"), 1)

    def test_other_failure_reasons_do_not_raise_floor(self):
        self.record("corrigido", "capacidade")
        for reason in ("contexto", "acesso", "ferramenta", "infra"):
            self.record("refeito", reason)
        output = self.run_log("--resumo").stdout
        self.assertIn("| 2 | codigo | executor-A | 0 | 1 | 4 |", output)
        self.assertNotIn("elevar piso", output)

    def test_reason_required_for_nonaccepted_results(self):
        for result in ("corrigido", "refeito"):
            with self.subTest(result=result):
                response = self.run_log("--faixa", "1", "--tipo", "extracao", "--modelo", "ensaio",
                                        "--esforco", "low", "--resultado", result, code=2)
                self.assertIn("--motivo é obrigatório", response.stderr)
        self.assertFalse(self.path.exists())

    def test_invalid_arguments_do_not_create_log(self):
        valid = ["--faixa", "2", "--tipo", "codigo", "--modelo", "ensaio",
                 "--esforco", "medium", "--resultado", "aceito"]
        for extra in (("--data", "2026-02-30"), ("--faixa", "4"), ("--resultado", "falhou"),
                      ("--motivo", "infra"), ("--tipo", " ")):
            with self.subTest(extra=extra):
                self.run_log(*valid, *extra, code=2)
        self.run_log("--faixa", "1", code=2)
        self.assertFalse(self.path.exists())

    def test_empty_summary_does_not_create_log(self):
        self.assertIn("Nenhum bloco registrado", self.run_log("--resumo").stdout)
        self.assertFalse(self.path.exists())

    def test_summary_ignores_blank_lines_but_preserves_error_line_numbers(self):
        self.record()
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write("\n \t \n")
        self.record("corrigido", "contexto")
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write("\n")
        output = self.run_log("--resumo").stdout
        self.assertIn("| 2 | codigo | executor-A | 1 | 1 | 0 |", output)
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write("nao e json\n")
        response = self.run_log("--resumo", code=1)
        self.assertIn("linha 6 inválida", response.stderr)

    def test_malformed_json_reports_line(self):
        self.path.parent.mkdir(parents=True)
        self.path.write_text("nao e json\n", encoding="utf-8")
        response = self.run_log("--resumo", code=1)
        self.assertIn("linha 1 inválida", response.stderr)


if __name__ == "__main__":
    unittest.main()
