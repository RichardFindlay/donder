

function terms_and_conditions(event) {

  // ensure any open journal entries are closed
  document.querySelectorAll('[id^="journal-details-modal-"]').forEach(function(el) {
    el.style.display = 'none'
  })

  // ensure other subscribe notification is closed
  // document.getElementById("modal-no-pro-journal-limit").style.display = 'none'

  // Get the modal
  var terms_modal = document.getElementById("modal-terms-conditions");

  terms_modal.style.display = "block";
  
  // stop click from propagation onto button push conditions
  event.stopPropagation();
  
  // Add event listener to "I understand" button to close modal
  var button_understand = document.getElementById("button-terms-conditions");
  button_understand.addEventListener("click", function() {
    terms_modal.style.display = "none";
  });

}