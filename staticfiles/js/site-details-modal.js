var prev_site_modal = null

function site_info(event, site_name, lat, lon) {

  // enusre log-in and subscribe modals are closed
  document.getElementById("modal-login").style.display = "none"
  document.getElementById("modal-buy-opts").style.display = "none"
  document.getElementById("modal-signup").style.display = "none"


  // ensure please subscribe notification is closed 
  document.getElementById("modal-no-other-users-landing").style.display = "none"

  // Get the modal
  if (prev_site_modal != null) {
    prev_site_modal.style.display = "none";
  }
  
  var details_modal = document.getElementById("details-modal-" + site_name);
  // var details_modal = getElementsByClassName("modal")

  // Get the button that opens the modal
  var site_btn = document.getElementById("tile-link-" + site_name);

  // When the user clicks the button, open the modal 
  details_modal.style.display = "block";

  // load map for current journal entry 
  mapboxgl.accessToken = 'pk.eyJ1IjoicmZpbmRsYXkiLCJhIjoiY2t4N3NtMmlqMzYxbzJ2cDhybGN5a210eCJ9.EdLcO474UjPD1AZWZ5nWLw';
  const map = new mapboxgl.Map({
    container: 'map-' + site_name, // container ID
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
      details_modal.style.display = "none";
    }
  }

  // store current site to ensure old win closes when opening new one
  prev_site_modal = details_modal

  // apply some width formatting to info-div if there are alot of elements - preventing div from being cut-off
  var modalId = 'details-modal-' + site_name; 
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

