const examples = {
  classification: `from librandomizer import TrainingDataGenerator, integer, choice

generator = TrainingDataGenerator(
    input_schema=integer(0, 99),
    output_schema=choice(["low", "medium", "high"]),
    count=100,
    seed=42,
)

pairs = generator.generate()`,
  regression: `from librandomizer import TrainingDataGenerator, object_schema, number

input_schema = object_schema({
    "x": number(0.0, 10.0, precision=3),
    "y": number(0.0, 10.0, precision=3),
})

def transform(row):
    return {"target": round(row["x"] * 0.7 + row["y"] * 0.3, 3)}

generator = TrainingDataGenerator(
    input_schema=input_schema,
    output_schema=object_schema({"target": number(0.0, 10.0, precision=3)}),
    count=250,
    seed=42,
    transform=transform,
)`,
  sequence: `from librandomizer import TrainingDataGenerator, string, array_schema

generator = TrainingDataGenerator(
    input_schema=array_schema(string(length=6), length=4),
    output_schema=string(length=6),
    count=100,
    seed=42,
)`,
  tabular: `from librandomizer import TrainingDataGenerator, object_schema, integer, boolean, number, choice

input_schema = object_schema({
    "age": integer(18, 65),
    "visits": integer(0, 100),
    "active": boolean(),
    "score": number(0.0, 1.0, precision=3),
})

def transform(row):
    return {"score_bucket": "high" if row["score"] > 0.7 else "low"}

generator = TrainingDataGenerator(
    input_schema=input_schema,
    output_schema=object_schema({"score_bucket": choice(["low", "high"])}),
    count=500,
    seed=42,
    transform=transform,
)`,
};

const tabs = Array.from(document.querySelectorAll(".tab"));
const code = document.querySelector("#example-code");
const title = document.querySelector("[data-example-title]");
const copyButton = document.querySelector(".copy-button");

function setExample(name) {
  code.textContent = examples[name];
  title.textContent = name[0].toUpperCase() + name.slice(1);
  tabs.forEach((tab) => tab.classList.toggle("active", tab.dataset.example === name));
  copyButton.textContent = "Copy";
}

tabs.forEach((tab) => {
  tab.addEventListener("click", () => setExample(tab.dataset.example));
});

copyButton.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(code.textContent);
    copyButton.textContent = "Copied";
  } catch {
    copyButton.textContent = "Select";
  }
});

setExample("classification");
