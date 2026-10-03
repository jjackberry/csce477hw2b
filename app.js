const form = document.getElementById("login-form");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const message = document.getElementById("message");

function validateLogin(email, password) {
  if (email.trim() === "" || password === "") {
    return "Email and password are required.";
  }
  if (!email.includes("@")) {
    return "Email must contain @.";
  }
  if (password.length < 8) {
    return "Password must be at least 8 characters.";
  }
  return "";
}

function showMessage(text) {
  message.textContent = text;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const email = emailInput.value;
  const password = passwordInput.value;
  const clientError = validateLogin(email, password);

  if (clientError) {
    showMessage(clientError);
    return;
  }

  try {
    const response = await fetch("/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    const data = await response.json();
    showMessage(data.error || "Login failed.");
  } catch (error) {
    showMessage("Could not reach the server. Start server.py and try again.");
  }
});
