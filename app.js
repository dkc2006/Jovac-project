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

const searchInput = document.getElementById("search-input");
const boxes = document.querySelectorAll(".box");

// Function to filter and sort trip cards
function filterAndSortTrips() {
  const searchTerm = searchInput.value.toLowerCase();
  const sortedBoxes = Array.from(boxes).sort((a, b) => {
    const nameA = a.querySelector(".place_name").innerText.toLowerCase();
    const nameB = b.querySelector(".place_name").innerText.toLowerCase();
    return nameA.localeCompare(nameB);
  });

  sortedBoxes.forEach((box) => {
    const placeName = box.querySelector(".place_name").innerText.toLowerCase();
    // Filter based on search term
    if (placeName.includes(searchTerm)) {
      box.style.display = "block"; // Show matching boxes
    } else {
      box.style.display = "none"; // Hide non-matching boxes
    }
  });
}

// Event listener for input change
searchInput.addEventListener("input", filterAndSortTrips);

// Initial sorting on page load
filterAndSortTrips();

let currentSlide = 0;
const slides = document.querySelectorAll(".carousel-image");

function showSlide(index) {
  slides.forEach((slide, i) => {
    slide.style.display = i === index ? "block" : "none"; // Show the current slide, hide the others
  });
}

function changeSlide(n) {
  currentSlide += n; // Update the current slide index
  if (currentSlide >= slides.length) {
    currentSlide = 0; // Wrap around to the first slide
  } else if (currentSlide < 0) {
    currentSlide = slides.length - 1; // Wrap around to the last slide
  }
  showSlide(currentSlide); // Show the updated slide
}

// Initialize the carousel by displaying the first slide
showSlide(currentSlide);

// Optional: If you want the slideshow to change automatically, uncomment the below code
setInterval(() => {
  changeSlide(1); // Automatically change to the next slide every 5 seconds
}, 2000);
