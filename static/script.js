// static/script.js

document.addEventListener('DOMContentLoaded', () => {
    const loginSection = document.getElementById('login-section');
    const dashboardSection = document.getElementById('dashboard-section');
    const loginForm = document.getElementById('login-form');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const loginError = document.getElementById('login-error');
    const logoutButton = document.getElementById('logout-button');
    const welcomeUsername = document.getElementById('welcome-username');
    const projectsUl = document.getElementById('projects-ul');
    const leaderboardOl = document.getElementById('leaderboard-ol');
    const badgesUl = document.getElementById('badges-ul');

    const token = localStorage.getItem('accessToken');
    if (token) {
        showDashboard();
    } else {
        showLogin();
    }

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData();
        formData.append('username', usernameInput.value);
        formData.append('password', passwordInput.value);
        try {
            const response = await fetch('/auth/token', { method: 'POST', body: formData });
            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('accessToken', data.access_token);
                showDashboard();
            } else {
                const errorData = await response.json();
                loginError.textContent = errorData.detail || 'Login failed.';
            }
        } catch (error) {
            loginError.textContent = 'An error occurred.';
        }
    });

    logoutButton.addEventListener('click', () => {
        localStorage.removeItem('accessToken');
        showLogin();
    });

    function showLogin() {
        dashboardSection.style.display = 'none';
        loginSection.style.display = 'block';
        projectsUl.innerHTML = '';
        leaderboardOl.innerHTML = '';
        badgesUl.innerHTML = '';
    }

    function showDashboard() {
        loginSection.style.display = 'none';
        dashboardSection.style.display = 'block';
        loginError.textContent = '';
        fetchDashboardData();
    }
    
    async function fetchDashboardData() {
        const token = localStorage.getItem('accessToken');
        if (!token) { showLogin(); return; }
        
        const headers = { 'Authorization': `Bearer ${token}` };

        try {
            const decodedToken = JSON.parse(atob(token.split('.')[1]));
            welcomeUsername.textContent = decodedToken.sub;
            
            const [projectsResponse, leaderboardResponse, badgesResponse] = await Promise.all([
                fetch('/api/v1/projects', { headers }),
                fetch('/api/v1/leaderboard', { headers }),
                fetch('/api/v1/users/me/badges', { headers })
            ]);

            if (projectsResponse.status === 401 || leaderboardResponse.status === 401 || badgesResponse.status === 401) {
                logoutButton.click();
                return;
            }

            // Handle projects
            const projects = await projectsResponse.json();
            projectsUl.innerHTML = '';
            if (projects.length === 0) {
                 projectsUl.innerHTML = '<li>No projects analyzed yet. Use the API docs to analyze one!</li>';
            } else {
                projects.forEach(project => {
                    const li = document.createElement('li');
                    li.textContent = `${project.name} (ID: ${project.id})`;
                    projectsUl.appendChild(li);
                });
            }

            // Handle leaderboard
            const leaderboard = await leaderboardResponse.json();
            leaderboardOl.innerHTML = '';
             if (leaderboard.length === 0) {
                 leaderboardOl.innerHTML = '<li>No points scored yet! Resolve an issue to get on the board.</li>';
            } else {
                leaderboard.forEach(user => {
                    const li = document.createElement('li');
                    li.textContent = `${user.username} - ${user.total_points} points`;
                    leaderboardOl.appendChild(li);
                });
            }

            // Handle badges
            const userBadges = await badgesResponse.json();
            badgesUl.innerHTML = '';
            if (userBadges.length === 0) {
                badgesUl.innerHTML = '<li>No badges earned yet. Keep fixing issues!</li>';
            } else {
                userBadges.forEach(userBadge => {
                    const li = document.createElement('li');
                    li.innerHTML = `<strong>${userBadge.badge.name}</strong>: ${userBadge.badge.description}`;
                    badgesUl.appendChild(li);
                });
            }
        } catch (error) {
            console.error('Failed to fetch dashboard data:', error);
            logoutButton.click();
        }
    }
});