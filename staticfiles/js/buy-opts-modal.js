// Get the modal
var modal = document.getElementById("modal-buy-opts");

// Get the button that opens the modal
if (document.getElementById("button-buy-opts")) {
  var buy_btn = document.getElementById("button-buy-opts");


// When the user clicks the button, open the modal 
buy_btn.onclick = function(buy_event) {

  // ensure login modal is closed
  document.getElementById("modal-login").style.display = "none"

  // ensure any site details modal is closed if open 
  document.querySelectorAll('[id^="details-modal-"]').forEach(function(el) {
    el.style.display = 'none'
  })

  modal.style.display = "block";
  
  // stop click from propagation onto button push conditions
  buy_event.stopPropagation();
  
  // When the user clicks anywhere outside of the modal, close it
  document.onclick = function(buy_event) {
    if (!buy_event.target.closest(".modal, .button-buy")) {
      modal.style.display = "none";
    }
  }
}
}