document.addEventListener('DOMContentLoaded', function () {
    const virtualKeyboard = document.getElementById('virtual-keyboard');
    let isUpperCase = false;

    document.getElementById('dni').addEventListener('click', () => {
        configureVirtualKeyboard('dni');
    });

    document.getElementById('user').addEventListener('click', () => {
        configureVirtualKeyboard('user');
    });

    document.getElementById('pass').addEventListener('click', () => {
        configureVirtualKeyboard('pass');
    });

    const form = document.getElementById('login_form');


    document.addEventListener('click', (event) => {
        if ((virtualKeyboard.style.display === 'block' || virtualKeyboard.style.display === 'flex') && !form.contains(event.target)) {
            virtualKeyboard.style.display = 'none';
        } else if (event.target.classList.contains('key')) {

            event.stopPropagation();
        }
    });

    function configureVirtualKeyboard(inputId) {
        if (document.getElementById('virtual-keyboard')) {
            const virtualKeyboard = document.getElementById('virtual-keyboard');
            virtualKeyboard.style.display = "flex";
        }
        const currentInput = document.getElementById(inputId);
        const virtualKeyboard = document.getElementById('virtual-keyboard');

        virtualKeyboard.innerHTML = '';

        const keyboardLayout = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ñ', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'Case', 'Space', 'Del'];

        keyboardLayout.forEach(letter => {
            const key = document.createElement('div');
            key.classList.add('key');
            key.textContent = letter;

            key.addEventListener('click', () => {
                if (letter === 'Space') {
                    currentInput.value += ' ';
                } else if (letter === 'Del') {
                    currentInput.value = currentInput.value.slice(0, -1);
                } else if (letter === 'Case') {
                    isUpperCase = !isUpperCase;
                    updateKeyboardCase();
                } else {
                    const character = (isUpperCase) ? letter.toUpperCase() : letter.toLowerCase();
                    currentInput.value += character;
                }
            });

            virtualKeyboard.appendChild(key);
        });

        updateKeyboardCase();
        
    }

    function updateKeyboardCase() {
        const keys = document.querySelectorAll('.key');
        keys.forEach(key => {
            if (key.textContent !== 'Case') {
                const character = (isUpperCase) ? key.textContent.toUpperCase() : key.textContent.toLowerCase();
                key.textContent = character;
            }
        });
    }
});