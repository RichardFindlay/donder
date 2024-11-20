// Get the modal
var modal_login = document.getElementById("modal-login");

// Get the button that opens the modal
var login_btn = document.getElementById("login-button");

// open modal if there is a login messge error
if (document.getElementsByClassName('login-message')[0] != undefined) {
  if (document.getElementsByClassName('login-message')[0].innerHTML == 'Credentials Invalid') {
    // run modal open func
    loginmodal()
  }
}

// When the user clicks the button, open the modal - only run when login button is present 
if (document.getElementsByClassName('button-login')[0] != undefined) {
  login_btn.onclick = loginmodal 
}

// login function
function loginmodal(event) {

  // ensure buy modal is closed
  document.getElementById("modal-signup").style.display = "none"

  // ensure any site details modal is closed if open 
  document.querySelectorAll('[id^="details-modal-"]').forEach(function(el) {
    el.style.display = 'none'
  })

  modal_login.style.display = "block";
  
  // stop click from propagation onto button push conditions
  if (event != undefined) {
    event.stopPropagation();
  }

  // When the user clicks anywhere outside of the modal, close it
  document.onclick = function(event) {
    if (!event.target.closest(".modal-login, .login-button")) {
      modal_login.style.display = "none";

        // remove any messages from modal after closing
        document.getElementById('signup-message').innerHTML = '';
        document.getElementById('login-message').innerHTML = '';
    }
  }
}
