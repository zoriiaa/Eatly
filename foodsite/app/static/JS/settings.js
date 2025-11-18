const editBtn = document.getElementById('editBtn');
const saveBtn = document.getElementById('saveBtn');
const inputs = document.querySelectorAll('#profileForm input');
const selects = document.querySelectorAll('#profileForm select');
const deleteBtn = document.querySelector('.delete-btn');

editBtn.addEventListener('click', () => {
    // Робимо всі поля редагованими
    inputs.forEach(input => input.removeAttribute('readonly'));
    selects.forEach(select => select.removeAttribute('disabled'));

    // Перемикаємо кнопки
    editBtn.style.display = 'none';
    saveBtn.style.display = 'inline-flex';
});

saveBtn.addEventListener('click', () => {
    // Повертаємо поля у readonly/disabled
    inputs.forEach(input => input.setAttribute('readonly', true));
    selects.forEach(select => select.setAttribute('disabled', true));

    // Перемикаємо кнопки назад
    saveBtn.style.display = 'none';
    editBtn.style.display = 'inline-flex';

    alert('Зміни збережено!');
});

deleteBtn.addEventListener('click', () => {
    const confirmDelete = confirm('Ви дійсно хочете видалити профіль?');
    if (confirmDelete) {
        // Тут можна виконати видалення через сервер
        alert('Профіль видалено!');
        // Наприклад, перенаправити користувача на головну сторінку
        // window.location.href = '/';
    } else {
        alert('Видалення скасовано.');
    }
});