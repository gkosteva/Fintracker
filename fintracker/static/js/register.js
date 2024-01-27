const usernameField = document.querySelector("#usernameField")
const feedbackField = document.querySelector(".invalid_feedback")
const emailField = document.querySelector("#emailField")
const emailFeedbackField = document.querySelector(".emailFeedback")

usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value;

    if (usernameVal.length > 0) {
        fetch("/authentication/validate-username",
            {
                body: JSON.stringify({username: usernameVal}), method: 'POST'
            }).then((res) => res.json()).then((data) => {
            console.log('data', data)
            if (data.username_error) {
                usernameField.classList.add("is-invalid");
                feedbackField.style.display = 'block';
                feedbackField.innerHTML = `<p>${data.username_error}</p>`;
            } else {
                feedbackField.style.display = 'none'
                usernameField.classList.remove("is-invalid");
                usernameField.classList.add("is-valid");
            }
        });
    } else {
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
                emailField.classList.add("is-invalid");
                emailFeedbackField.style.display = 'block';
                emailFeedbackField.innerHTML = `<p>${data.email_error}</p>`;
            } else {
                emailFeedbackField.style.display = 'none'
                emailField.classList.remove("is-invalid");
                emailField.classList.add("is-valid");
            }
        });
    } else {
        emailField.classList.remove("is-valid");
        emailField.classList.remove("is-invalid");
        emailFeedbackField.style.display = 'none';
    }
});