const usernameField = document.querySelector("#usernameField")
const feedbackField = document.querySelector(".invalid_feedback")
const emailField = document.querySelector("#emailField")
const emailFeedbackField = document.querySelector(".emailFeedback")
let passwordToogle = document.querySelector(".showPasswordToogle")
const passwordField = document.querySelector("#passwordField")
const submitButton = document.querySelector(".submit-btn")
const handleToogleInput = (e) => {
    if (passwordToogle.textContent === "SHOW") {
        passwordToogle.textContent = "HIDE"
        passwordField.setAttribute("type", "text");
    } else {
        passwordToogle.textContent = "SHOW"
        passwordField.setAttribute("type", "password");
    }
}

passwordToogle.addEventListener("click", handleToogleInput);

usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value;

    if (usernameVal.length > 0) {
        fetch("/authentication/validate-username",
            {
                body: JSON.stringify({username: usernameVal}), method: 'POST'
            }).then((res) => res.json()).then((data) => {
            console.log('data', data)
            if (data.username_error) {
                submitButton.disabled = true
                usernameField.classList.add("is-invalid");
                feedbackField.style.display = 'block';
                feedbackField.innerHTML = `<p>${data.username_error}</p>`;
            } else {
                submitButton.removeAttribute("disabled")
                feedbackField.style.display = 'none'
                usernameField.classList.remove("is-invalid");
                usernameField.classList.add("is-valid");
            }
        });
    } else {
        submitButton.disabled = true;
        usernameField.classList.remove("is-valid");
        usernameField.classList.remove("is-invalid");
        feedbackField.style.display = 'none';
    }
});

emailField.addEventListener("keyup", (e) => {
    const emailVal = e.target.value;


    if (emailVal.length > 0) {
        fetch("/authentication/validate-email",
            {
                body: JSON.stringify({email: emailVal}), method: 'POST'
            }).then((res) => res.json()).then((data) => {
            console.log('data', data)
            if (data.email_error) {
                submitButton.disabled = true;
                emailField.classList.add("is-invalid");
                emailFeedbackField.style.display = 'block';
                emailFeedbackField.innerHTML = `<p>${data.email_error}</p>`;
            } else {
                submitButton.removeAttribute("disabled")
                emailFeedbackField.style.display = 'none'
                emailField.classList.remove("is-invalid");
                emailField.classList.add("is-valid");
            }
        });
    } else {
        submitButton.disabled = true;
        emailField.classList.remove("is-valid");
        emailField.classList.remove("is-invalid");
        emailFeedbackField.style.display = 'none';
    }
});