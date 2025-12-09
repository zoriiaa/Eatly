function toggleFav(button) {
    const emptyHeart = button.querySelector(".empty");
    const filledHeart = button.querySelector(".filled");

    const isActive = button.classList.toggle("active");

    if (isActive) {
        emptyHeart.style.display = "none";
        filledHeart.style.display = "block";
        filledHeart.style.animation = "pop 0.25s ease";
        alert(`Страва додана до улюблених`);
    } else {
        emptyHeart.style.display = "block";
        filledHeart.style.display = "none";
        alert(`Страва більше не улюблена`);
    }

}

const wrapper = document.querySelector('.menu-wrapper');
const btn = wrapper.querySelector('.add-btn');
const dropdownButtons = wrapper.querySelectorAll('.dropdown-menu button');
const message = document.getElementById('message');

btn.addEventListener('click', () => {
    wrapper.classList.toggle('active');
});

dropdownButtons.forEach(d => {
    d.addEventListener('click', () => {
        const meal = d.textContent;

        alert(`${meal} додано до меню!`);
        wrapper.classList.remove('active');

    });
});
