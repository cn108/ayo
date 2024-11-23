// core/static/js/scripts.js

document.addEventListener('DOMContentLoaded', function() {
    console.log("JavaScript is working!");

    // Example: Toggle functionality
    const toggles = document.querySelectorAll('.toggle-btn');
    toggles.forEach(btn => {
        btn.addEventListener('click', function() {
            const content = document.querySelector(this.dataset.target);
            content.classList.toggle('d-none');
        });
    });
});
