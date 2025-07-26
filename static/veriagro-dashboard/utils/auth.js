export function setupAuth() {
    document.getElementById('login-form').addEventListener('submit', async (e) => {
        e.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        const form = new URLSearchParams();
        form.append('email', email);
        form.append('password', password);

        try {
            const response = await fetch(`http://127.0.0.1:8000/users/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email,
                    password
                })
            });


            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Login failed: ${errorText}`);
            }

            const data = await response.json();
            localStorage.setItem('accessToken', data.access_token);
            window.location.hash = '#devices';
            location.reload();
        } catch (err) {
            alert(err.message);
        }
    });

    document.getElementById('logout-button').addEventListener('click', () => {
        localStorage.removeItem('accessToken');
        location.reload();
    });
}
