// const modal = document.getElementById('modal');
// const overlay = document.querySelector('.overlay');
// const btnCloseModal = document.querySelector('.close-modal');
// const btnsOpenModal = document.querySelectorAll('.show-modal');
// const form = document.querySelector('form');
// const successSpan = document.getElementById('success-message');



// const openModal = function () {
//     const formErrors = document.querySelectorAll('.error-message');
//     if (formErrors.length === 0) {
//         modal.classList.remove('hidden');
//         overlay.classList.remove('hidden');
//     }
// };

// const closeModal = function () {
//     modal.classList.add('hidden');
//     overlay.classList.add('hidden');
// };

// for (let i = 0; i < btnsOpenModal.length; i++){
//     btnsOpenModal[i].addEventListener('click', openModal);
// }

// btnCloseModal.addEventListener('click', closeModal);
// overlay.addEventListener('click', closeModal);

// document.addEventListener('keydown', function (e) {
//     if (e.key === 'Escape' && !modal.classList.contains('hidden')) {
//         closeModal();
//     }
// });


// const handleFormSubmission = async function (event) {
//     event.preventDefault();
//     const formData = new FormData(form);
//     const response = await fetch(form.action, {
//         method: 'POST',
//         body: formData
//     });
//     const data = await response.json();
//     if (data.success) {
//         // closeModal();
//         successSpan.textContent = 'Category added';
        
//         // Close modal after one second
//         setTimeout(function() {
//             closeModal();
//         }, 2000);

//     } else {
//         const errors = JSON.parse(data.errors);
//         console.log(errors);
//         const errorSpan = document.getElementById('form-errors');
//         errorSpan.textContent = errors;
//     }
// };

// form.addEventListener('submit', handleFormSubmission);


labels = document.querySelectorAll('label');
for (var i = 0; i < labels.length; i++) {
    labels[i].classList.add('form-label');
}

inputs = document.querySelectorAll('input');
for (var i = 0; i < inputs.length; i++) {
    inputs[i].classList.add('form-control');
}

// ================ prevent the modal from auto colsing when there is an error raised =============================
// $(document).ready(function(){
//     $('#myModal form').submit(function(e){
//         e.preventDefault();
//         $.ajax({
//             type: "POST",
//             url: "{% url 'create_new_category' %}",
//             data: $(this).serialize(),
//             success: function(response){
//                 // Check if response contains error message
//                 if (response.startsWith('Category created')) {
//                     // Close modal and reload page if successful
//                     $('#myModal').modal('hide');
//                     location.reload();
//                 } else {
//                     // Display error message and keep modal open
//                     $('#myModal .modal-body').html(response);
//                 }
//             }
//         });
//     });
// });