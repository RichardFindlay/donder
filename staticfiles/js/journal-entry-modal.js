var prev_journal_modal = null

function journal_entry_info(event, id, lat, lon) {


  // close user notification
  document.getElementById("modal-no-pro-journal-limit").style.display = "none"

  //  close other subscribe notification from journal limit 
  document.getElementById("modal-no-other-users").style.display = 'none'

  // ensure add hike modal is closed
  document.getElementById("modal-add-hike").style.display = "none"

  // Get the modal
  if (prev_journal_modal != null) {
    prev_journal_modal.style.display = "none";
  }
  var journal_details_modal = document.getElementById("journal-details-modal-" + id);
  // var details_modal = getElementsByClassName("modal")

  // Get the button that opens the modal
  var site_btn = document.getElementById("journal-tile-link-" + id);

  // When the user clicks the button, open the modal 
  journal_details_modal.style.display = "block";

  // load map for current journal entry 
  mapboxgl.accessToken = 'pk.eyJ1IjoicmZpbmRsYXkiLCJhIjoiY2t4N3NtMmlqMzYxbzJ2cDhybGN5a210eCJ9.EdLcO474UjPD1AZWZ5nWLw';
    const map = new mapboxgl.Map({
    container: 'map-' + id, // container ID
    // Choose from Mapbox's core styles, or make your own style with Mapbox Studio
    style: 'mapbox://styles/rfindlay/clf8uclhd009s01mx7jaqmx5s', // style URL
    center: [lon, lat], // starting position [lng, lat]
    zoom: 13 // starting zoom
  });
  
  // stop click from propagation onto button push conditions
  event.stopPropagation();

  // When the user clicks anywhere outside of the modal, close it
  document.onclick = function(event) {
    if (!event.target.closest(".modal")) {
      journal_details_modal.style.display = "none";
      document.getElementById('map-' + id).innerHTML = "";
    }
  }
  
  // store current site to ensure old win closes when opening new one
  prev_journal_modal = journal_details_modal

  // apply some width formatting to info-div if there are alot of elements - preventing div from being cut-off
  var modalId = 'journal-details-modal-' + id; 
  var modal = document.getElementById(modalId);

  var infoDivs = modal.querySelectorAll('.info-element');
  var numInfoDivs = infoDivs.length;

  var infoDiv = modal.querySelector('.information-div');

  // get the number of characters in the info-text to see if width too long
  var info_text_region = modal.querySelector('.info-region-text'); 
  var content = info_text_region.innerHTML;
  var numChars = content.length;

  if (parseInt(numInfoDivs) >= 6 && numChars > 25) {
    infoDiv.style.justifyContent = "flex-start";
  } else {
    infoDiv.style.justifyContent = "center";
  }

}

