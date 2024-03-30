var form_fields = document.getElementsByTagName('input')
        form_fields[1].placeholder = 'Email address';
        form_fields[2].placeholder = 'First name';
        form_fields[3].placeholder = 'Last name';
        form_fields[4].placeholder = 'Password';
        form_fields[5].placeholder = 'Re-enter password';
        form_fields[6].placeholder = 'Mobile phone';

        for (var i = 0; i < form_fields.length; i++) {

            if (form_fields[i].type !== 'submit') {  
                form_fields[i].className += ' form-control form-control-lg bg-light fs-6';
            }
        }