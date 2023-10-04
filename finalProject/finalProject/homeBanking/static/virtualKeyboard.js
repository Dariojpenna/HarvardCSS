document.addEventListener('DOMContentLoaded', function () {
    const virtualKeyboard = document.getElementById('virtual-keyboard');

    document.getElementById('dni').addEventListener('click', () => {
        configureVirtualKeyboard('dni');
    });
    
    document.getElementById('user').addEventListener('click', () => {
        configureVirtualKeyboard('user');
    });
    
    document.getElementById('pass').addEventListener('click', () => {
        configureVirtualKeyboard('pass');
    });

    document.addEventListener('click', (event) => {
        if (virtualKeyboard.style.display === 'block' && !virtualKeyboard.contains(event.target)) {

            virtualKeyboard.style.display = 'none';
        }
    });
    
})

function configureVirtualKeyboard(inputId) {
    if (document.getElementById('virtual-keyboard')) {
        const virtualKeyboard = document.getElementById('virtual-keyboard');
        virtualKeyboard.style.display= "block"

    }
    const currentInput = document.getElementById(inputId);
    const virtualKeyboard = document.getElementById('virtual-keyboard');
    
    virtualKeyboard.innerHTML = '';
    
    const keyboardLayout = ['1','2','3','4','5','6','7','8','9','0','Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P','A','S','D','F','G','H','J','K','L','Ñ','Z','X','C','V','B','N','M','Space','Del'];

    keyboardLayout.forEach(letter => {
        const key = document.createElement('div');
        key.classList.add('key');
        key.textContent = letter;
        key.addEventListener('click', () => {
            if (letter === 'Space') {
                currentInput.value += ' ';
            } else if (letter === 'Del') {
                currentInput.value = currentInput.value.slice(0, -1);
            } else {
                currentInput.value += letter;
            }
        });
        virtualKeyboard.appendChild(key);
    });


}