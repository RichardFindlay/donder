

function no_community_feed(event) {

  // ensure any open journal entries are closed
  document.querySelectorAll('[id^="journal-details-modal-"]').forEach(function(el) {
    el.style.display = 'none'
  })

  // ensure other subscribe notification is closed
  document.getElementById("modal-no-pro-journal-limit").style.display = 'none'

  // Get the modal
  var modal_no_community = document.getElementById("modal-no-other-users");

  modal_no_community.style.display = "block";
  
  // stop click from propagation onto button push conditions
  event.stopPropagation();
  
  // When the user clicks anywhere outside of the modal, close it
  document.onclick = function(event) {
    if (!event.target.closest(".modal-no-other-users")) {
      modal_no_community.style.display = "none";
    }
  }
}