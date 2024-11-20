// Get the modal
var signup_modal = document.getElementById("modal-signup");

// Get the button that opens the modal
var signup_btn = document.getElementById("sign-up-btn");

// sign up button from insights modals
var signup_btn_2 = document.getElementById("sign-up-btn-2");

// sign up button from insights modals
var signup_btn_4 = document.getElementById("sign-up-btn-3");

// sign up button from insights modals
var signup_btn_3 = document.getElementById("sign-up-btn-hero");

// open modal if there is a login messge error
if (document.getElementsByClassName('signup-message')[0] != undefined) {
    if (document.getElementsByClassName('signup-message')[0].innerHTML == 'It looks like this email address is already registered' || document.getElementsByClassName('signup-message')[0].innerHTML == 'Password not matching' || document.getElementsByClassName('signup-message')[0].innerHTML == 'Please enter requested details to create an account') {
      // run modal open func
      signupmodal()
    }
  }

// When the user clicks the button, open the modal - only run when login button is present 
if (document.getElementsByClassName('button-signup')[0] != undefined) {
    signup_btn.onclick = signupmodal 
  }

// id user is clicking on user activity 
if (document.getElementsByClassName('button-signup-2')[0] != undefined) {
  signup_btn_2.onclick = signupmodal 
}

// id user is clicking on user activity 
if (document.getElementsByClassName('button-signup-3')[0] != undefined) {
  signup_btn_4.onclick = signupmodal(public=true) 
}

//  if user clicks hero image email
if (document.getElementsByClassName('btn-hero-sign-up')[0] != undefined) {
  signup_btn_3.onclick = signupmodal 
}




// When the user clicks the button, open the modal 
function signupmodal(signup_event, public=false)  {

  // get value from input email
  var inputElement = document.getElementById("floatingTextInput1");
  if (inputElement) {
    var email = inputElement.value;
  } 
  else {
    var email = "";
  }
  document.getElementById("sign-up-email").value = email;

  // ensure login modal is closed
  if (public === false) {
  document.getElementById("modal-login").style.display = "none"

  // ensure sign-up / subsribe notification is closed
  
  document.getElementById("modal-no-other-users-landing").style.display = "none"

  // ensure any site details modal is closed if open 
  document.querySelectorAll('[id^="details-modal-"]').forEach(function(el) {
    el.style.display = 'none'
  })
  }

  signup_modal.style.display = "block";
  
  // stop click from propagation onto button push conditions
  if (signup_event != undefined) {
    signup_event.stopPropagation();
  }
  
  // When the user clicks anywhere outside of the modal, close it

    document.onclick = function(signup_event) {
      if (document.getElementById("modal-terms-conditions").style.display != "block") {
      if (!signup_event.target.closest(".modal-signup", ".button-signup")) {
          signup_modal.style.display = "none";

          // remove any messages from modal after closing
          document.getElementById('signup-message').innerHTML = '';
          document.getElementById('login-message').innerHTML = '';

      }
    }
}



}
