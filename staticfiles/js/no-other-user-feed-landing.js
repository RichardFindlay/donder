

function no_community_feed_landing(event) {

  // ensure any site details modal is closed if open 
  document.querySelectorAll('[id^="details-modal-"]').forEach(function(el) {
    el.style.display = 'none'
  })  

  // Get the modal
  var modal_no_community_landing = document.getElementById("modal-no-other-users-landing");

  modal_no_community_landing.style.display = "block";
  
  // stop click from propagation onto button push conditions
  event.stopPropagation();
  
  // When the user clicks anywhere outside of the modal, close it
  document.onclick = function(event) {
    if (!event.target.closest(".modal-no-other-users-landing")) {
      modal_no_community_landing.style.display = "none";
    }
  }

}