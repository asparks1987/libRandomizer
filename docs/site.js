const examples = {
  python: `from librandomizer import random_int

value = random_int()`,
  javascript: `const { randomInt } = require("@librandomizer/javascript");

const value = randomInt();`,
  go: `import "github.com/asparks1987/librandomizer/packages/go"

value := librandomizer.RandomInt()`,
  rust: `use librandomizer::random_int;

let value = random_int();`,
  swift: `import LibRandomizer

let value = LibRandomizer.randomInt()`,
};

const code = document.querySelector("#example-code");
const copyButton = document.querySelector(".copy-button");
const tabs = Array.from(document.querySelectorAll(".tab"));

tabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    tabs.forEach((item) => item.classList.remove("active"));
    tab.classList.add("active");
    code.textContent = examples[tab.dataset.language];
    copyButton.textContent = "Copy";
  });
});

copyButton.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(code.textContent);
    copyButton.textContent = "Copied";
  } catch {
    copyButton.textContent = "Select";
  }
});
