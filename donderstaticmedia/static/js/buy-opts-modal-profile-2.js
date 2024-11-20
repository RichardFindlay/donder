// Get the modal
var modal = document.getElementById("modal-buy-opts");

// Get the button that opens the modal
var buy_btn_profile = document.getElementById("profile-buy-2");

// When the user clicks the button, open the modal 
buy_btn_profile.onclick = function(buy_event) {

  // close user notification
  document.getElementById("modal-no-pro-journal-limit").style.display = "none"

  // ensure login modal is closed
  document.getElementById("modal-add-hike").style.display = "none"

  // other user notification is closed
  document.getElementById("modal-no-other-users").style.display = "none"

  // ensure any open journal entries are closed
  document.querySelectorAll('[id^="journal-details-modal-"]').forEach(function(el) {
    el.style.display = 'none'
  })

  modal.style.display = "block";
  
  // stop click from propagation onto button push conditions
  buy_event.stopPropagation();
  
  // When the user clicks anywhere outside of the modal, close it
  document.onclick = function(buy_event) {
    if (!buy_event.target.closest(".button-buy-profile")) {
      modal.style.display = "none";
    }
  }
}
