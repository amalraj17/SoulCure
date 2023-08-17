document.addEventListener('DOMContentLoaded', function () {
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const phoneInput = document.getElementById('phone');
    const passwordInput = document.getElementById('pass');
    const confirmPasswordInput = document.getElementById('cpass');


    nameInput.addEventListener('blur', validateName);
    emailInput.addEventListener('blur', validateEmail);
    passwordInput.addEventListener('blur', validatePassword);
    confirmPasswordInput.addEventListener('blur', validateConfirmPassword);
    phoneInput.addEventListener('blur', validatePhoneNumber);

    // Validation functions go here
    function validateName() {
        const namePattern = /^[A-Za-z ]+$/;
        const nameValidation = document.getElementById('nameValidation');
        const nameValid = document.getElementById('nameValid');

        if (!namePattern.test(nameInput.value)) {
            nameInput.classList.add('is-invalid');
            nameInput.classList.remove('is-valid');
            nameValidation.style.display = 'block';
            nameValid.style.display = 'none';
        } else {
            nameInput.classList.remove('is-invalid');
            nameInput.classList.add('is-valid');
            nameValidation.style.display = 'none';
            nameValid.style.display = 'block';
        }
    }
    function validateName() {
        var letters = /^[A-Za-z ]*$/;
        var regex = /^\s/;
        var username = document.getElementById("username");
        if (username.value.length >= 3 && username.value.match(regex)) {
          document.getElementById("submit").disabled = true;
          return true;
        }
        if (username.value.match(letters) && username.value.length >= 3) {
          text = "";
          document.getElementById("name_err").innerHTML = text;
          document.getElementById("submit").disabled = false;
          return false;
        } else {
          text = "Please enter username minimum 3 character allowed"
          document.getElementById("name_err").innerHTML = text;
          document.getElementById("submit").disabled = true;
          return true;
        }
      }

    function validateEmail() {
        const emailPattern = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
        const emailValidation = document.getElementById('emailValidation');
        const emailValid = document.getElementById('emailValid');

        if (!emailPattern.test(emailInput.value)) {
            emailInput.classList.add('is-invalid');
            emailInput.classList.remove('is-valid');
            emailValidation.style.display = 'block';
            emailValid.style.display = 'none';
        } else {
            emailInput.classList.remove('is-invalid');
            emailInput.classList.add('is-valid');
            emailValidation.style.display = 'none';
            emailValid.style.display = 'block';
        }
    }

    function validatePhoneNumber() {
        const phoneNumberPattern = /^\d{10}$/; // Adjust the pattern as needed
        const phoneValidation = document.getElementById('phoneValidation');
        if (!phoneNumberPattern.test(phoneInput.value)) {
            phoneInput.classList.add('is-invalid');
            phoneInput.classList.remove('is-valid');
            phoneValidation.style.display = 'block';
        } else {
            phoneInput.classList.remove('is-invalid');
            phoneInput.classList.add('is-valid');
            phoneValidation.style.display = 'none';
        }
    }

    function validatePassword() {
        const passwordPattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+[\]{}|;:'",.<>?/~`]).{8,}$/;
        const passValidation = document.getElementById('passValidation');
        const passValid = document.getElementById('passValid');

        if (!passwordPattern.test(passwordInput.value)) {
            passwordInput.classList.add('is-invalid');
            passwordInput.classList.remove('is-valid');
            passValidation.style.display = 'block';
            passValid.style.display = 'none';
        } else {
            passwordInput.classList.remove('is-invalid');
            passwordInput.classList.add('is-valid');
            passValidation.style.display = 'none';
            passValid.style.display = 'block';
        }
    }

    function validateConfirmPassword() {
        const confirmPasswordValidation = document.getElementById('cpassValidation');
        const confirmPasswordValid = document.getElementById('cpassValid');

        if (passwordInput.value !== confirmPasswordInput.value) {
            confirmPasswordInput.classList.add('is-invalid');
            confirmPasswordInput.classList.remove('is-valid');
            confirmPasswordValidation.style.display = 'block';
            confirmPasswordValid.style.display = 'none';
        } else {
            confirmPasswordInput.classList.remove('is-invalid');
            confirmPasswordInput.classList.add('is-valid');
            confirmPasswordValidation.style.display = 'none';
            confirmPasswordValid.style.display = 'block';
        }
    }
});
