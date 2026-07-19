document.addEventListener("DOMContentLoaded", function() {
    const rows = document.querySelectorAll(".table-row");
    
    rows.forEach((row, index) => {
        // Hide initially
        row.style.opacity = "0";
        row.style.transform = "translateX(-10px)";
        row.style.transition = "all 0.3s ease";

        // Staggered reveal
        setTimeout(() => {
            row.style.opacity = "1";
            row.style.transform = "translateX(0)";
        }, 100 * index); 
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.getElementById('sidebar-menu');
    const toggleBtn = document.getElementById('toggle-btn');
    const navLogo = document.getElementById('nav-logo');
    const rows = document.querySelectorAll('.t-row');

    // Sidebar Toggle
    toggleBtn.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
        navLogo.classList.toggle('hidden');
    });

    //  Real-time Staggered Animation
    rows.forEach((row, index) => {
        setTimeout(() => {
            row.style.transition = "all 0.4s ease";
            row.style.opacity = "1";
            row.style.transform = "translateY(0)";
        }, 80 * index);
    });
});
