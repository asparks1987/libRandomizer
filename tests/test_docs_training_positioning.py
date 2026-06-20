import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DocsTrainingPositioningTests(unittest.TestCase):
    def test_homepage_quickstart_is_valid_and_current(self):
        html = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

        self.assertIn("Reproducible training pairs for prediction networks.", html)
        self.assertIn("input_schema=integer(0, 99)", html)
        self.assertIn('output_schema=choice(["low", "medium", "high"])', html)
        self.assertIn("count=100", html)
        self.assertIn("seed=42", html)
        self.assertNotIn("Generate input/output pairs with a schema, a seed, and a transform.", html)
        self.assertNotIn("<h3>Python reference SDK</h3>\ngenerator =", html)

    def test_readme_documents_current_public_api(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("input_schema", readme)
        self.assertIn("output_schema", readme)
        self.assertIn("count", readme)
        self.assertIn("seed", readme)
        self.assertIn("write_jsonl", readme)
        self.assertIn("write_csv", readme)

    def test_training_spec_makes_transform_optional(self):
        spec = (ROOT / "spec" / "training" / "README.md").read_text(encoding="utf-8")

        self.assertIn("Schema-only generation is the default workflow", spec)
        self.assertIn("`output_schema`: a serializable schema", spec)
        self.assertIn("`transform`: an optional host-language callback", spec)


if __name__ == "__main__":
    unittest.main()
