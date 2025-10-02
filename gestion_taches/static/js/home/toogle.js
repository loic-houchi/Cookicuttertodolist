document.addEventListener('DOMContentLoaded', function () {
const toggleButton = document.getElementById('menuToggle');
	const mobileMenu = document.getElementById('mobileMenu');
	if (toggleButton && mobileMenu) {
		function toggleMenu() {
			const isHidden = mobileMenu.classList.contains('hidden');
			mobileMenu.classList.toggle('hidden');
			toggleButton.setAttribute('aria-expanded', String(isHidden));
		}
		toggleButton.addEventListener('click', toggleMenu);
		mobileMenu.querySelectorAll('a').forEach(function (link) {
			link.addEventListener('click', function () {
				if (!mobileMenu.classList.contains('hidden')) toggleMenu();
			});
		});
	}
})