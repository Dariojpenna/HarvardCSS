document.addEventListener('DOMContentLoaded', function () {

    document.getElementById('input1').addEventListener('click', () => {
        configureVirtualKeyboard('input1');
    });
    
    document.getElementById('input2').addEventListener('click', () => {
        configureVirtualKeyboard('input2');
    });
    
    document.getElementById('input3').addEventListener('click', () => {
        configureVirtualKeyboard('input3');
    });
    
    
           
    



    
})

function configureVirtualKeyboard(inputId) {
    if (document.getElementById('virtual-keyboard')) {
        const virtualKeyboard = document.getElementById('virtual-keyboard');
        /* Falta ocultar el teclado y ver porque se duplica*/
    }

    const virtualKeyboard = document.getElementById('virtual-keyboard');
    const currentInput = document.getElementById(inputId);
    
    const keyboardLayout = ['1','2','3','4','5','6','7','8','9','0','Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P','A','S','D','F','G','H','J','K','L','Ñ','Z','X','C','V','B','N','M'];

    keyboardLayout.forEach(letter => {
        const key = document.createElement('div');
        
        key.classList.add('key');
        key.textContent = letter;
        key.addEventListener('click', () => {
            textInput.value += letter;
        });
        virtualKeyboard.appendChild(key);
    });


}