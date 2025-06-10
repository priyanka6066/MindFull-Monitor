// Get the token from local storage
let token = localStorage.getItem("token");

// Define the base URL for the API
const apiBase = "http://localhost:5000";

// Select DOM elements
const navbtn = document.querySelector("#navbtn");
const navbtn1 = document.querySelector(".navbtn1");
const detect = document.querySelector(".detect");
const user = document.querySelector(".user");

// Fetch user details from the backend
if (token) {
  detect.style.display = "block";
  navbtn1.style.display = "none";
  fetch(`${apiBase}/user`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.username) {
        user.innerText = `${data.username} || `;
        navbtn.innerHTML = `<a href="#" onclick="logout()">Logout</a>`;
      } else {
        // Handle cases where user data is not returned
        navbtn.innerHTML = `<li><a class="nav-link mha-nav" href="./sign-in.html">Login</a></li> 

                    <li><a class="nav-link mha-nav" href="./sign-up.html">Register</a></li> `;
      }
    })
    .catch((error) => {
      console.error("Error fetching user data:", error);
      user.innerText = "Error fetching user data";
    });
} else {
  // If there's no token, set up the nav button for login
  navbtn.style.display = "none";
  detect.style.display = "none";
}

// Function to handle logout
function logout() {
  localStorage.removeItem("token");

  window.location.href = "http://127.0.0.1:3000/templates/index.html";
}
