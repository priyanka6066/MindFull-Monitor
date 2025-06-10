const apiBase = 'http://localhost:5000'; // Adjust as needed
let token = localStorage.getItem('token');




const navbtn=document.querySelector("#navbtn")

// Handle login
document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const response = await fetch(`${apiBase}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
    const result = await response.json();
    
    if (response.ok) {
        localStorage.setItem('token', result.access_token);
        window.location.href = 'http://127.0.0.1:3000/templates/index.html'; // Redirect to questions page after login
    } else {
        alert(result.error || 'Login failed');
    }
});

