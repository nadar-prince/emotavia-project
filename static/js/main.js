
document.addEventListener('DOMContentLoaded', function() {
    const myButton = document.getElementById('home-mood-btn');

    myButton.addEventListener('click', function() {
        window.location.href = "/userlogin";
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const myButton = document.getElementById('home-login-signup-btn');

    myButton.addEventListener('click', function() {
        window.location.href = "/userlogin";
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const myButton = document.getElementById('user-mood-btn');

    myButton.addEventListener('click', function() {
        window.location.href = "/check_mood";
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const myButton = document.getElementById('user-logout');

    myButton.addEventListener('click', function() {
        window.location.href = "/userlogout";
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const myButton = document.getElementById('support-contactus');

    myButton.addEventListener('click', function() {
        window.location.href = "/contact";
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const myButton = document.getElementById('user-support-contactus');

    myButton.addEventListener('click', function() {
        window.location.href = "/user_contact";
    });
});

document.getElementById('contact-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission to allow validation

    // Get form inputs
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;

    // Regular expression patterns
    const namePattern = /^[A-Z][a-z]+(\s[A-Z][a-z]+)*$/;
    const emailPattern = /^[a-z][a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,6}$/;

    // Clear previous error messages
    document.getElementById('name-error').innerHTML = '';
    document.getElementById('email-error').innerHTML = '';

    // Validation flags
    let valid = true;

    // Name validation
    if (!namePattern.test(name)) {
        document.getElementById('name-error').innerHTML = 'Invalid Name. Must start with an uppercase letter and contain only alphabets.';
        valid = false;
    }

    // Email validation
    if (!emailPattern.test(email)) {
        document.getElementById('email-error').innerHTML = 'Invalid Email. Email should be a valid format.';
        valid = false;
    }

    // If all validations pass, submit the form
    if (valid) {
        // Submit the form if all validations are successful
        this.submit();
    }

    const form = event.target;

    form.reset();

});


document.getElementById('signup-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission to allow validation

    // Get form inputs
    const name = document.getElementById('name').value;
    const phone = document.getElementById('phone').value;
    const email = document.getElementById('email').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;

    // Regular expression patterns
    const namePattern = /^[A-Z][a-z]+(\s[A-Z][a-z]+)*$/;
    const phonePattern = /^[9876]\d{9}$/;
    const emailPattern = /^[a-z][a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,6}$/;
    const usernamePattern = /^[a-z][a-zA-Z0-9@_]{8,15}$/;
    const passwordPattern = /^[A-Z][a-z]*(?=.*[0-9])(?=.*[!@#$%^&*])[A-Za-z0-9!@#$%^&*]{8,15}$/;

    // Clear previous error messages
    document.getElementById('name-error').innerHTML = '';
    document.getElementById('phone-error').innerHTML = '';
    document.getElementById('email-error').innerHTML = '';
    document.getElementById('username-error').innerHTML = '';
    document.getElementById('password-error').innerHTML = '';
    document.getElementById('confirm-password-error').innerHTML = '';

    // Validation flags
    let valid = true;

    // Name validation
    if (!namePattern.test(name)) {
        document.getElementById('name-error').innerHTML = 'Invalid Name. Must start with an uppercase letter and contain only alphabets.';
        valid = false;
    }

    // Phone number validation
    if (!phonePattern.test(phone)) {
        document.getElementById('phone-error').innerHTML = 'Invalid Mobile Number. Number must start with 6,7,8,9 and it should be a 10-digit number.';
        valid = false;
    }

    // Email validation
    if (!emailPattern.test(email)) {
        document.getElementById('email-error').innerHTML = 'Invalid Email. Email should be a valid format.';
        valid = false;
    }

    // Username validation
    if (!usernamePattern.test(username)) {
        document.getElementById('username-error').innerHTML = 'Invalid Username. Must start with a lowercase letter and be a maximum of 16 characters..';
        valid = false;
    }

    // Password validation
    if (!passwordPattern.test(password)) {
        document.getElementById('password-error').innerHTML = 'Invalid Password. Must start with an uppercase letter, followed by lowercase letters, contain a symbol and a number, and have a length of 8–16 characters.';
        valid = false;
    }

    // Confirm password check
    if (password !== confirmPassword) {
        document.getElementById('confirm-password-error').innerHTML = 'Passwords do not match!';
        valid = false;
    }

    // If all validations pass, submit the form
    if (valid) {
        // Submit the form if all validations are successful
        this.submit();
    }
});

function togglePassword(fieldId, iconElement) {
    const input = document.getElementById(fieldId);

    if (input.type === "password") {
        input.type = "text";
        iconElement.src = "/static/hidden.png"; // hide eye
    } else {
        input.type = "password";
        iconElement.src = "/static/eye.png"; // show eye
    }
}

