document.addEventListener('DOMContentLoaded', function () {
    const submitBtn = document.getElementById('form-submit');
    const contactForm = document.getElementById('form');

    if (submitBtn && contactForm) {
        submitBtn.addEventListener('click', function (e) {
            e.preventDefault();
            const formData = new FormData(contactForm);
            fetch('', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('modal-toggle').click();
                        contactForm.reset();
                        document.getElementById('name-error').innerText = "";
                        document.getElementById('email-error').innerText = "";
                        document.getElementById('message-error').innerText = "";
                    } else {
                        if (data.errors.name) document.getElementById('name-error').innerText = data.errors.name;
                        if (data.errors.email) document.getElementById('email-error').innerText = data.errors.email;
                        if (data.errors.message) document.getElementById('message-error').innerText = data.errors.message;
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert("Something went wrong. Please try again later.");
                });
        });
    }
});