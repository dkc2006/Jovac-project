// Back to top Symbol

//Get the button
let mybutton = document.getElementById("btn-back-to-top");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function () {
  scrollFunction();
};
function scrollFunction() {
  if (document.body.scrollTop > 40 || document.documentElement.scrollTop > 40) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}
// When the user clicks on the button, scroll to the top of the document
mybutton.addEventListener("click", backToTop);

function backToTop() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}

// for login model

// document.addEventListener("DOMContentLoaded", function () {
//   // Login Button Interaction
//   const loginBtn = document.querySelector(".nav-singin p");
//   const loginModal = document.createElement("div");
//   loginModal.classList.add("login-modal");
//   loginModal.innerHTML = `
//                 <div class="login-modal-content">
//                     <span class="close" id="closeModal">&times;</span>
//                     <input type="text" placeholder="Phone number, username, or email">
//                     <input type="password" placeholder="Password">
//                     <button class="login-btn">Log in</button>
//                     <div class="or">OR</div>
//                     <button class="facebook-login">Log in with Facebook</button>
//                     <a href="#" class="forgot-password">Forgot password?</a>
//                     <div class="signup-section">
//                         <span>Don't have an account?</span> <a href="./register.html" class="signup-link">Sign up</a>
//                     </div>
//                 </div>
//             `;
//   document.body.appendChild(loginModal);

//   loginBtn.addEventListener("click", function () {
//     loginModal.style.display = "flex";
//   });

//   document.getElementById("closeModal").addEventListener("click", function () {
//     loginModal.style.display = "none";
//   });

//   window.addEventListener("click", function (event) {
//     if (event.target == loginModal) {
//       loginModal.style.display = "none";
//     }
//   });
// });
