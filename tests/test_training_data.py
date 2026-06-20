import csv
import json
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from librandomizer import (
    TrainingDataError,
    TrainingDataGenerator,
    array_schema,
    boolean,
    choice,
    integer,
    number,
    object_schema,
    string,
    transform_spec,
)


def make_generator(seed: int = 42) -> TrainingDataGenerator:
    schema = object_schema(
        {
            "profile": object_schema(
                {
                    "age": integer(18, 65),
                    "active": boolean(),
                    "name": string(length=8),
                }
            ),
            "features": array_schema(number(0.0, 1.0, precision=3), length=3),
            "region": choice(["na", "eu", "apac"]),
        }
    )

    def transform(record):
        score = round(record["profile"]["age"] / 100 + sum(record["features"]) / 10, 3)
        return {"approved": record["profile"]["active"] and score > 0.35, "score": score}

    return TrainingDataGenerator(
        schema,
        object_schema({"approved": boolean(), "score": number(0.0, 1.5, precision=3)}),
        transform=transform,
        count=5,
        seed=seed,
        transform_spec=transform_spec("approval-score", threshold=0.35),
    )


class TrainingDataTests(unittest.TestCase):
    def test_same_seed_same_schema_same_transform_produces_identical_pairs(self):
        first = make_generator(seed=7)
        second = make_generator(seed=7)

        self.assertEqual(
            [pair.to_record() for pair in first.generate()],
            [pair.to_record() for pair in second.generate()],
        )
        self.assertEqual(first.to_spec(), second.to_spec())

    def test_different_seed_changes_generated_inputs(self):
        first = make_generator(seed=7)
        second = make_generator(seed=8)

        first_inputs = [pair.input for pair in first.generate()]
        second_inputs = [pair.input for pair in second.generate()]

        self.assertNotEqual(first_inputs, second_inputs)
        for value in first_inputs + second_inputs:
            first.input_schema.validate(value)

    def test_schema_only_input_output_generation_uses_predetermined_count(self):
        generator = TrainingDataGenerator(
            input_schema=integer(1, 3),
            output_schema=choice(["low", "medium", "high"]),
            count=4,
            seed=99,
        )

        first = [pair.to_record() for pair in generator.generate()]
        second = [pair.to_record() for pair in generator.generate()]

        self.assertEqual(len(first), 4)
        self.assertEqual(first, second)
        self.assertTrue(all(isinstance(pair["input"], int) for pair in first))
        self.assertTrue(all(pair["output"] in {"low", "medium", "high"} for pair in first))

    def test_nested_schema_generation_and_transform_output_shape(self):
        generator = make_generator(seed=3)
        pairs = generator.generate(3)

        self.assertEqual(len(pairs), 3)
        for pair in pairs:
            generator.input_schema.validate(pair.input)
            generator.output_schema.validate(pair.output)
            self.assertEqual(set(pair.output), {"approved", "score"})

    def test_json_jsonl_and_csv_exports_are_round_trippable(self):
        generator = make_generator(seed=11)

        with tempfile.TemporaryDirectory() as tempdir:
            tempdir = Path(tempdir)
            json_path = generator.write_json(tempdir / "pairs.json", 4)
            jsonl_path = generator.write_jsonl(tempdir / "pairs.jsonl", 4)
            csv_path = generator.write_csv(tempdir / "pairs.csv", 4)

            records = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(len(records), 4)
            self.assertTrue(records[0]["input"]["profile"]["name"])

            jsonl_lines = [line for line in jsonl_path.read_text(encoding="utf-8").splitlines() if line.strip()]
            self.assertEqual(len(jsonl_lines), 4)
            self.assertTrue(all(json.loads(line)["output"]["approved"] in {True, False} for line in jsonl_lines))

            with csv_path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))

            self.assertTrue(rows[0]["input.profile.age"])
            self.assertTrue(rows[0]["input.features[0]"])
            self.assertTrue(rows[0]["output.score"])

    def test_schema_and_generator_specs_round_trip(self):
        generator = make_generator(seed=19)
        spec = generator.to_spec()

        rebuilt = TrainingDataGenerator.from_spec(spec, generator.transform)
        self.assertEqual(rebuilt.to_spec(), spec)

    def test_invalid_output_schema_raises(self):
        schema = object_schema({"name": string(length=4)})

        def transform(record):
            return {"name": record["name"], "extra": True}

        generator = TrainingDataGenerator(schema, object_schema({"name": string(length=4)}), transform=transform)

        with self.assertRaisesRegex(TrainingDataError, "Object value does not match expected keys"):
            generator.generate(1)


if __name__ == "__main__":
    unittest.main()
