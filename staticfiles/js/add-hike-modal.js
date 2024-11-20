


// open modal if there is an add hike error message
if (document.getElementsByClassName('addhike-message')[0] != undefined) {
  if (document.getElementsByClassName('addhike-message')[0].innerHTML == 'Please select a mountain name from the dropdown list and enter a climb date in the correct format') {
    // run modal open func
    add_hike()
  }
}



function add_hike(event) {

  // ensure any open journal entries are closed
  document.querySelectorAll('[id^="journal-details-modal-"]').forEach(function(el) {
    el.style.display = 'none'
  })
  
  // Get the modal
  var modal_add_hike = document.getElementById("modal-add-hike");

  // Get the button that opens the modal
  var btn = document.getElementById("button-add-hike");

    modal_add_hike.style.display = "block";
    
    // stop click from propagation onto button push conditions
  // stop click from propagation onto button push conditions
    if (event != undefined) {
      event.stopPropagation();
    }
    
    // When the user clicks anywhere outside of the modal, close it
    document.onclick = function(event) {
      if (!event.target.closest(".modal", ".autocomplete", ".autocomplete-input", ".autocomplete-result-list") && !event.target.classList.contains("autocomplete-result")) {
        modal_add_hike.style.display = "none";
      }
    }

}


