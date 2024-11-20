// Get the modal
var edit_profile_modal = document.getElementById("edit-profile-modal");

// Get the button that opens the modal
var edit_profile_btn = document.getElementById("edit-profile-button");

// When the user clicks the button, open the modal 
edit_profile_btn.onclick = function(edit_profile_event) {

  // ensure login modal is closed
  // document.getElementById("modal-login").style.display = "none"

  // ensure any site details modal is closed if open 
  // document.querySelectorAll('[id^="details-modal-"]').forEach(function(el) {
  //   el.style.display = 'none'
  // })

  edit_profile_modal.style.display = "block";
  
  // stop click from propagation onto button push conditions
  edit_profile_event.stopPropagation();
  
  // When the user clicks anywhere outside of the modal, close it
  document.onclick = function(edit_profile_event) {
    if (!edit_profile_event.target.closest(".modal, .button-edit-profile")) {
      edit_profile_modal.style.display = "none";
    }
  }
}
