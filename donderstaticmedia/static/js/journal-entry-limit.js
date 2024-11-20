

function journal_lim(event) {

  // ensure any open journal entries are closed
  document.querySelectorAll('[id^="journal-details-modal-"]').forEach(function(el) {
    el.style.display = 'none'
  })

  //  close other subscribe notification from journal limit 
  document.getElementById("modal-no-other-users").style.display = 'none'

  // Get the modal
  var modal_journal_lim = document.getElementById("modal-no-pro-journal-limit");

  modal_journal_lim.style.display = "block";
  
  // stop click from propagation onto button push conditions
  event.stopPropagation();
  
  // When the user clicks anywhere outside of the modal, close it
  document.onclick = function(event) {
    if (!event.target.closest(".modal-journal-lim")) {
      modal_journal_lim.style.display = "none";
    }
  }
}