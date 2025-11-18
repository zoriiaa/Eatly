const passwordInput = document.querySelector('.password-input');
const eyeIcon = document.querySelector('.eye-icon');

eyeIcon.addEventListener('click', () => {
  if (passwordInput.type === 'password') {
    passwordInput.type = 'text';
    eyeIcon.src = 'images/eye.svg';
  } else {
    passwordInput.type = 'password';
    eyeIcon.src = 'images/eye-off.svg';
  }
});


