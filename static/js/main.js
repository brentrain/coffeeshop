document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                // Close mobile menu if open
                const navbarCollapse = document.querySelector('.navbar-collapse');
                if (navbarCollapse.classList.contains('show')) {
                    navbarCollapse.classList.remove('show');
                }
                
                // Scroll to target
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add to cart functionality
    const addToCartButtons = document.querySelectorAll('.btn-primary');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const itemName = this.parentElement.querySelector('h5').textContent;
            const itemPrice = this.parentElement.querySelector('p').textContent;
            
            // Create a notification
            const notification = document.createElement('div');
            notification.className = 'alert alert-success alert-dismissible fade show';
            notification.innerHTML = `
                ${itemName} added to cart!
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            
            // Add notification to the page
            document.querySelector('.container').prepend(notification);
            
            // Auto-dismiss after 3 seconds
            setTimeout(() => {
                notification.remove();
            }, 3000);
        });
    });

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const password = this.querySelector('input[type="password"]');
            const confirmPassword = this.querySelector('input[name="confirm_password"]');
            
            if (confirmPassword && password.value !== confirmPassword.value) {
                event.preventDefault();
                alert('Passwords do not match!');
            }
        });
    });

    // Handle mobile menu collapse on window resize
    window.addEventListener('resize', function() {
        const navbarCollapse = document.querySelector('.navbar-collapse');
        if (window.innerWidth >= 992 && navbarCollapse.classList.contains('show')) {
            navbarCollapse.classList.remove('show');
        }
    });
}); 