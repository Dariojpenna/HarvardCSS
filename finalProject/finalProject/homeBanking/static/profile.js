document.addEventListener('DOMContentLoaded', function () {

    emailBtn = document.querySelectorAll('.btn-email'),
        numberPhoneBtn = document.getElementById('btn-numberPhone')
    
    emailBtn.forEach(element => {
        element.addEventListener('click', function (ev) {
            target = ev.target.textContent
            element.style.display = 'none'
            email_field = document.getElementById('email_field')
            var inputForm = document.createElement("input");
            var btnForm = document.createElement("button")
            var email = document.getElementById("email")
            var emailText = email.innerText
            var errorMessage = document.getElementById("error-msge");
            var phoneNumber = document.getElementById("phone_number")
            var phoneField = document.getElementById("phone_field")
            var phoneText = phoneNumber.innerText


            inputForm.setAttribute("type", "email");
            
            inputForm.id = "email_input"

            btnForm.textContent = "Send"
            btnForm.classList.add("btn", "btn-primary")
            btnForm.style.marginLeft = "3px"
            btnForm.id = "btn-email-send"


            if (target == "Modify Email"){

                email.style.display = 'none'
                inputForm.placeholder = emailText
                email_field.appendChild(inputForm)
                email_field.appendChild(btnForm)

                btnForm.addEventListener('click', function () {
                    

                    if (validateEmail(inputForm.value)) {

                    function getCookie(csrftoken) {
                        const value = `; ${document.cookie}`;
                        const parts = value.split(`; ${csrftoken}=`);
                        if (parts.length == 2) return parts.pop().split(';').shift();

                    }

                    fetch('/editEmail/', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                    'X-CSRFToken': getCookie('csrftoken') 
                                },
                                body: JSON.stringify({
                                    new_email: inputForm.value
                                }),
                            })
                            .then(response => response.json())
                            .then(data => {
                                email.innerHTML = data.email;
                                clickOutsideListener(btnForm);
                            })
                            .catch(error => {
                                console.log('Error al guardar la publicación:', error);
                                
                            });

                    } else {

                        errorMessage.style.display = 'block'
                        errorMessage.innerHTML = "Enter a valid email address"
                    }
                })
            }else{
                inputForm.placeholder = phoneText
                phoneNumber.style.display = "none"
                phoneField.appendChild(inputForm)
                phoneField.appendChild(btnForm)

                btnForm.addEventListener('click', function () {

                    if (validatePhone(inputForm.value)){
                        function getCookie(csrftoken) {
                            const value = `; ${document.cookie}`;
                            const parts = value.split(`; ${csrftoken}=`);
                            if (parts.length == 2) return parts.pop().split(';').shift();
    
                        }
                        console.log(inputForm.value)
                        fetch('/editPhone/', {
                                    method: 'POST',
                                    headers: {
                                        'Content-Type': 'application/json',
                                        'X-CSRFToken': getCookie('csrftoken') 
                                    },
                                    body: JSON.stringify({
                                        new_phone: inputForm.value
                                        
                                    }),
                            })
                            .then(response => response.json())
                            .then(data => {
                                phoneNumber.innerHTML = data.phoneNumber
                                clickOutsideListener(btnForm);
                            })
                            .catch(error => {
                                console.log('Error al guardar la publicación:', error);
                                    
                            });
                    }else{
                        console.log("Correo electrónico no válido:", inputForm.value);
                        errorMessage.style.display = 'block'
                        errorMessage.innerHTML = "Enter a valid Phone Number"
                    }
                    
                }
            )}

            clickOutsideListener = function (event) {
                if (!email_field.contains(event.target) & (!phoneField.contains(event.target))) {
                    
                    element.style.display = "block";
                    email.style.display = "block";
                    inputForm.remove()
                    btnForm.remove()
                    errorMessage.style.display = 'none'
                    phoneNumber.style.display = "block";
                    document.removeEventListener("click", clickOutsideListener);
                }
            };

            setTimeout(function () {
                document.addEventListener("click", clickOutsideListener);
            }, 50);
        })
    });
})

function validateEmail(email) {
    var emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailPattern.test(email);
}

function validatePhone(phoneNumber){
    var phonePattern = /^\+\d{1,3}\d{6,14}$/
    return phonePattern.test(phoneNumber);
}