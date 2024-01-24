const usernameField = document.querySelector("#usernameField")
const feedbackField = document.querySelector(".invalid-feedback")

usernameField.addEventListener("keyup", (e) => {
    console.log("777777", 777777)
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
    }
    else{
        usernameField.classList.remove("is-valid");
    }
});