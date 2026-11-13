"""Testes sem rede: nomes, notas e preços abaixo são todos sintéticos."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from aa_common import cli_parameters, profile_cost


def synthetic_model(family, effort, intel, eng, price, ttfat):
    return {
        "name": f"Claude {family.title()} Ensaio ({effort.title()})",
        "slug": f"ensaio-{family}-{effort}",
        "model_creator": {"name": "Criador sintético"},
        "evaluations": {
            "artificial_analysis_intelligence_index": intel,
            "artificial_analysis_engineering_index": eng,
        },
        "pricing": {"price_1m_input_tokens": price, "price_1m_output_tokens": price},
        "performance": {
            "median_time_to_first_answer_token_seconds": ttfat,
            "median_output_tokens_per_second": 50,
        },
    }


class ProfileCostTests(unittest.TestCase):
    def setUp(self):
        self.row = {"in": 2, "out": 8, "cache": 0.2, "cache_write": 2.5, "verbosity": 200}

    def test_cache_write_hit_and_verbosity(self):
        # 250*2.5 + 750*0.2 + (100*2)*8, por milhão.
        self.assertAlmostEqual(profile_cost(self.row, 1000, 0.75, 100, 100), 0.002375)

    def test_without_cache_uses_input_price(self):
        self.assertAlmostEqual(profile_cost(self.row, 1000, 0, 100, 100), 0.0036)

    def test_missing_cache_and_verbosity_fall_back(self):
        self.row.update(cache=None, cache_write=None, verbosity=None)
        self.assertAlmostEqual(profile_cost(self.row, 1000, 0.75, 100, None), 0.0028)

    def test_missing_prices(self):
        for field in ("in", "out"):
            with self.subTest(field=field):
                row = dict(self.row, **{field: None})
                self.assertIsNone(profile_cost(row, 1000, 0.5, 100, 100))


class RankTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix=".test-rank-", dir=ROOT)
        self.addCleanup(self.temp.cleanup)
        self.snapshot = Path(self.temp.name) / "snapshot.json"
        self.models = [
            synthetic_model("haiku", "low", 40, 30, 1, 40),
            synthetic_model("sonnet", "medium", 80, 72, 1.5, 8),
            synthetic_model("opus", "high", 100, 90, 4, 15),
            synthetic_model("externo", "xhigh", 60, 60, 2, None),
        ]
        self.snapshot.write_text(json.dumps({"generated_at": "2026-01-01", "data": self.models}),
                                 encoding="utf-8")

    def run_rank(self, *args, code=0):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "aa_rank.py"),
             "--snapshot", str(self.snapshot), *args],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
        )
        self.assertEqual(result.returncode, code, result.stderr + result.stdout)
        return result

    def slugs(self, output):
        return [line.split("|")[2].strip() for line in output.splitlines()
                if line.startswith("| Claude ")]

    def test_cost_and_value_orders(self):
        cost = self.run_rank("--ordem", "custo").stdout
        value = self.run_rank("--ordem", "valor").stdout
        self.assertEqual(self.slugs(cost), ["ensaio-haiku-low", "ensaio-sonnet-medium",
                                           "ensaio-externo-xhigh", "ensaio-opus-high"])
        self.assertEqual(self.slugs(value)[0], "ensaio-sonnet-medium")
        self.assertIn("ordem por valor", self.run_rank().stdout)
        self.assertIn("ordem por custo", self.run_rank("--min", "1").stdout)

    def test_relative_floor_in_task_capability(self):
        output = self.run_rank("--capacidade", "eng", "--ref", "ensaio-opus-high", "--pct", "80").stdout
        self.assertIn("Eng ≥ 72.0", output)
        self.assertIn("ordem por custo", output)
        self.assertEqual(self.slugs(output), ["ensaio-sonnet-medium", "ensaio-opus-high"])
        higher = self.run_rank("--capacidade", "eng", "--ref", "ensaio-opus-high", "--pct", "90").stdout
        self.assertIn("Eng ≥ 81.0", higher)
        self.assertEqual(self.slugs(higher), ["ensaio-opus-high"])
        absolute = self.run_rank("--capacidade", "eng", "--ref", "ensaio-opus-high",
                                 "--pct", "80", "--min", "85").stdout
        self.assertIn("Eng ≥ 85.0", absolute)
        self.assertEqual(self.slugs(absolute), ["ensaio-opus-high"])

    def test_ambiguous_ref_fails(self):
        result = self.run_rank("--ref", "ensaio", code=1)
        self.assertIn("--ref deve identificar um modelo", result.stderr)
        self.assertIn("ensaio-haiku-low", result.stderr)
        self.assertIn("ensaio-opus-high", result.stderr)

    def test_max_ttfat_excludes_slow_and_unknown(self):
        output = self.run_rank("--max-ttfat", "8").stdout
        self.assertEqual(self.slugs(output), ["ensaio-sonnet-medium"])
        self.assertIn("3 lento", output)

    def test_cli_claude_code_marks_unmapped_without_filtering(self):
        plain = self.run_rank("--ordem", "custo").stdout
        output = self.run_rank("--ordem", "custo", "--cli", "claude-code").stdout
        self.assertIn("model=haiku; effort=low", output)
        self.assertIn("model=sonnet; effort=medium", output)
        self.assertIn("model=opus; effort=high", output)
        self.assertIn("não exposto nesta CLI", output)
        self.assertEqual(self.slugs(plain), self.slugs(output))
        # Sem --cli, as colunas/valores existentes são idênticos.
        plain_rows = [line for line in plain.splitlines() if line.startswith("| Claude ")]
        cli_rows = [line.rsplit("|", 2)[0] + "|" for line in output.splitlines()
                    if line.startswith("| Claude ")]
        self.assertEqual(plain_rows, cli_rows)
        self.assertNotIn("Parâmetros CLI", plain)

    def test_cli_codex_emits_slug_and_effort_with_warning(self):
        output = self.run_rank("--cli", "codex").stdout
        self.assertIn("model=ensaio-externo-xhigh; model_reasoning_effort=xhigh", output)
        self.assertIn("confira o nome e o esforço aceitos em /model", output)

    def test_missing_snapshot_points_to_provisional_tables(self):
        self.snapshot.unlink()
        result = self.run_rank(code=1)
        self.assertIn("preferences.local.md", result.stderr)
        self.assertIn("references/claude-code.md", result.stderr)
        self.assertIn("references/codex.md", result.stderr)

    def test_long_context_warning_is_generic(self):
        output = self.run_rank().stdout
        self.assertIn("confira a tabela do provedor", output)
        self.assertNotIn("5 vezes", output)
        self.assertNotIn("Atenção:", self.run_rank("--entrada", "100000").stdout)


class CliMappingTests(unittest.TestCase):
    def test_aliases_and_all_effort_suffixes(self):
        for alias in ("haiku", "sonnet", "opus", "fable"):
            for effort in ("low", "medium", "high", "xhigh", "max"):
                with self.subTest(alias=alias, effort=effort):
                    # Nome com sufixo e slug sem sufixo; família pode vir de ambos.
                    row = {"name": f"Ensaio ({effort.title()})", "slug": f"claude-{alias}-ensaio"}
                    self.assertEqual(cli_parameters(row, "claude-code"),
                                     f"model={alias}; effort={effort}")
                    row = {"name": f"Ensaio {alias.title()}", "slug": f"ensaio-{effort}"}
                    self.assertEqual(cli_parameters(row, "codex"),
                                     f"model=ensaio-{effort}; model_reasoning_effort={effort}")
                    self.assertEqual(cli_parameters(row, "claude-code"),
                                     f"model={alias}; effort={effort}")

    def test_missing_effort_is_not_inferred(self):
        row = {"name": "Claude Fable Ensaio", "slug": "claude-fable-ensaio"}
        for cli in ("claude-code", "codex"):
            with self.subTest(cli=cli):
                output = cli_parameters(row, cli)
                self.assertIn("esforço sem dados", output)
                self.assertNotIn("effort=", output)

    def test_partial_or_ambiguous_family_is_not_an_alias(self):
        for name in ("Haikuzinho Ensaio High", "Claude Haiku Sonnet Ensaio High"):
            with self.subTest(name=name):
                self.assertEqual(cli_parameters({"name": name, "slug": "ensaio-high"}, "claude-code"),
                                 "não exposto nesta CLI")


if __name__ == "__main__":
    unittest.main()
