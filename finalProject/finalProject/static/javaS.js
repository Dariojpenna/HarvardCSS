document.addEventListener('DOMContentLoaded', function () {
    const modal = document.querySelector(".modal");
    const btnGenerator = document.getElementById('codeGenerator');
    const codeChecker = document.getElementById('codeChecker');
    const codeInput = document.getElementById('codeInput');
    const transferBtn = document.getElementById('transfer-button');
    const modalBtn = document.getElementById("modalBtn")
    const btn_modal_close = document.getElementById("btn_modal_close")

    btnGenerator.addEventListener('click', () => {
        fetch('/code_generator/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')  // Get the token CSRF
            },
        });
    });

    codeChecker.addEventListener('click', () => {
        const code = codeInput.value;
        console.log(code)
        fetch('code_checker/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken') 
            },
            body: `code=${code}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.message == "1"){
                console.log(data.message)
                modal.style.display = 'none';
                transferBtn.style.display = 'block';
                modalBtn.style.display = "none"
            }else{
                console.log(data.message)
                console.log("The code is not correct")
            }

        });
    });

    // Función para obtener el token CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
    return cookieValue;
    }


    btn_modal_close.addEventListener('click',()=>{
        modal.style.display = 'none';
    })

});

function whatsapp_validation(){
    var modal = document.querySelector(".modal");
    modal.style.display = 'block';
}







