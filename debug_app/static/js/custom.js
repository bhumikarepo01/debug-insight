// Debug Insight — Custom JS

document.addEventListener('DOMContentLoaded', function () {

    // ─── Delete confirmation (sidebar delete button) ─────────────────────────
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const url = this.getAttribute('href');
            if (confirm('Delete this error? This cannot be undone.')) {
                window.location.href = url;
            }
        });
    });

    // ─── Auto-resize textareas ───────────────────────────────────────────────
    document.querySelectorAll('textarea').forEach(ta => {
        const resize = () => {
            ta.style.height = 'auto';
            ta.style.height = ta.scrollHeight + 'px';
        };
        ta.addEventListener('input', resize);
        // run once on load to size pre-filled values
        resize();
    });

    // ─── Navbar scroll shadow ────────────────────────────────────────────────
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            navbar.style.boxShadow = window.scrollY > 10
                ? '0 4px 30px rgba(0,0,0,0.4)'
                : 'none';
        }, { passive: true });
    }

    // ─── Stagger fade-in for error cards ────────────────────────────────────
    document.querySelectorAll('.error-card').forEach((card, i) => {
        card.style.animationDelay = `${i * 0.06}s`;
    });

});
