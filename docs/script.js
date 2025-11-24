let expression = "";
const displayEl = document.getElementById("display");

function updateDisplay(value) {
  displayEl.textContent = value || "0";
}

function clearExpression() {
  expression = "";
  updateDisplay("0");
}

function evaluateExpression() {
  if (!expression) {
    updateDisplay("0");
    return;
  }

  try {
    // Evaluate safely enough for this toy app
    const result = Function(`"use strict"; return (${expression})`)();
    expression = String(result);
    updateDisplay(expression);
  } catch (err) {
    updateDisplay("Error");
    expression = "";
  }
}

function appendValue(value) {
  const isOperator = /[+\-*/]/.test(value);

  if (displayEl.textContent === "Error") {
    expression = "";
  }

  if (!expression && isOperator) {
    // Don't allow starting with +, -, *, /
    return;
  }

  // Prevent double operator like "++", "+*", etc.
  const lastChar = expression.slice(-1);
  if (isOperator && /[+\-*/]/.test(lastChar)) {
    expression = expression.slice(0, -1) + value;
  } else {
    expression += value;
  }

  updateDisplay(expression);
}

function handleButtonClick(e) {
  const btn = e.target.closest("button");
  if (!btn) return;

  const action = btn.dataset.action;
  const value = btn.dataset.value;

  if (action === "clear") {
    clearExpression();
  } else if (action === "equals") {
    evaluateExpression();
  } else if (value !== undefined) {
    appendValue(value);
  }
}

// --- Event wiring --- //

document.querySelector(".buttons").addEventListener("click", handleButtonClick);

// Optional: basic keyboard support for desktop use
document.addEventListener("keydown", (e) => {
  const { key } = e;

  if (key >= "0" && key <= "9") {
    appendValue(key);
  } else if (["+", "-", "*", "/"].includes(key)) {
    appendValue(key);
  } else if (key === "." || key === ",") {
    appendValue(".");
  } else if (key === "Enter" || key === "=") {
    e.preventDefault();
    evaluateExpression();
  } else if (key === "Escape") {
    clearExpression();
  } else if (key === "Backspace") {
    expression = expression.slice(0, -1);
    updateDisplay(expression);
  }
});