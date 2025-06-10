const apiBase = 'http://localhost:5000';

document.getElementById('registerForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const phone = document.getElementById('phone').value;

    const response = await fetch(`${apiBase}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password, phone })
    });
    const result = await response.json();
    
    if (response.ok) {
        alert('Registration successful! Please log in.');
        window.location.href = 'http://127.0.0.1:3000/templates/sign-in.html'; // Redirect to login
    } else {
        alert(result.error || 'Registration failed');
    }
});