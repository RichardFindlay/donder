// Get the modal
var modal_landing_sub = document.getElementById("modal-buy-opts");

// Get the button that opens the modal
if (document.getElementById("profile-buy-landing")) {
  var buy_btn_land = document.getElementById("profile-buy-landing");


// When the user clicks the button, open the modal 
buy_btn_land.onclick = function(buy_event) {

  // ensure any site details modal is closed if open 
  document.querySelectorAll('[id^="details-modal-"]').forEach(function(el) {
    el.style.display = 'none'
  })

  // other user notification is closed
  document.getElementById("modal-no-other-users-landing").style.display = "none"

  modal_landing_sub.style.display = "block";
  
  // stop click from propagation onto button push conditions
  buy_event.stopPropagation();
  
  // When the user clicks anywhere outside of the modal, close it
  document.onclick = function(buy_event) {
    if (!buy_event.target.closest(".button-buy-profile")) {
      modal_landing_sub.style.display = "none";
    }
  }
}
}