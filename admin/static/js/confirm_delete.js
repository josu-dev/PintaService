document.addEventListener('DOMContentLoaded', (event) => {
    const deleteButtons = document.querySelectorAll('.delete-button');
    deleteButtons.forEach((button) => {
        button.addEventListener('click', (event) => {
            const username = event.target.getAttribute('data-user');
            if (!confirm(`¿Estás seguro de que quieres eliminar al usuario ${username}?`)) {
                event.preventDefault();
            }
        });
    });
});