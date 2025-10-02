document.addEventListener('DOMContentLoaded', function () {
	// --- Carousel (full-width) ---
	const slidesContainer = document.getElementById('slides');
	const prevBtn = document.getElementById('prev');
	const nextBtn = document.getElementById('next');
	const dots = document.querySelectorAll('#carousel .carousel-dot');
	const carousel = document.getElementById('carousel');
	const slides = slidesContainer ? slidesContainer.querySelectorAll('.min-w-full') : [];

	let currentIndex = 0;
	let totalSlides = slides.length;
	let autoplayTimer = null;
	const slideDuration = 5000;

	function resetDotProgress() {
		dots.forEach(dot => {
			const progress = dot.querySelector('.dot-progress');
			if (progress) {
				progress.style.width = '0%';
				progress.style.transition = 'none';
			}
		});
	}

	function animateDotProgress(dot) {
		const progress = dot.querySelector('.dot-progress');
		if (!progress) return;
		
		// Reset and start animation
		progress.style.width = '0%';
		progress.style.transition = 'width 5000ms linear';
		
		// Force reflow
		progress.offsetHeight;
		
		// Start animation
		progress.style.width = '100%';
	}

	function goToSlide(index) {
		if (!slidesContainer || !totalSlides) return;
		currentIndex = (index + totalSlides) % totalSlides;
		const offset = -currentIndex * 100;
		slidesContainer.style.transform = `translateX(${offset}%)`;
		
		// Mark active slide for any CSS animations
		slides.forEach((slide, i) => {
			slide.classList.toggle('active-slide', i === currentIndex);
		});
		
		// Update dots with enhanced visual feedback
		updateDots();
		
		// Reset and animate dot progress
		resetDotProgress();
		animateDotProgress(dots[currentIndex]);
	}

	function nextSlide() { goToSlide(currentIndex + 1); }
	function prevSlide() { goToSlide(currentIndex - 1); }

	function updateDots() {
		dots.forEach((dot, i) => {
			const isActive = i === currentIndex;
			dot.classList.toggle('active', isActive);
			dot.setAttribute('aria-selected', String(isActive));
			
			// Add visual feedback
			if (isActive) {
				dot.style.transform = 'scale(1.1)';
				dot.style.boxShadow = '0 0 20px rgba(241, 228, 0, 0.5)';
			} else {
				dot.style.transform = 'scale(1)';
				dot.style.boxShadow = 'none';
			}
		});
	}

	function attachCarouselEvents() {
		if (prevBtn) prevBtn.addEventListener('click', () => {
			stopAutoplay();
			prevSlide();
			startAutoplay();
		});
		if (nextBtn) nextBtn.addEventListener('click', () => {
			stopAutoplay();
			nextSlide();
			startAutoplay();
		});
		
		// Fix dots click events
		dots.forEach((dot, i) => {
			dot.addEventListener('click', () => {
				stopAutoplay();
				goToSlide(i);
				startAutoplay();
			});
		});
		
		// Keyboard navigation
		window.addEventListener('keydown', (e) => {
			if (e.key === 'ArrowRight') {
				stopAutoplay();
				nextSlide();
				startAutoplay();
			}
			if (e.key === 'ArrowLeft') {
				stopAutoplay();
				prevSlide();
				startAutoplay();
			}
		});
		
		// Touch swipe
		let startX = 0;
		let isSwiping = false;
		if (slidesContainer) {
			slidesContainer.addEventListener('touchstart', (e) => {
				startX = e.touches[0].clientX;
				isSwiping = true;
				stopAutoplay();
			});
			slidesContainer.addEventListener('touchmove', (e) => {
				if (!isSwiping) return;
				const diff = e.touches[0].clientX - startX;
				if (Math.abs(diff) > 50) {
					isSwiping = false;
					if (diff < 0) nextSlide(); else prevSlide();
					startAutoplay();
				}
			});
			slidesContainer.addEventListener('touchend', () => {
				isSwiping = false;
				startAutoplay();
			});
		}
		
		// Hover pause
		if (carousel) {
			carousel.addEventListener('mouseenter', stopAutoplay);
			carousel.addEventListener('mouseleave', startAutoplay);
		}
	}

	function startAutoplay() {
		stopAutoplay();
		autoplayTimer = setInterval(() => {
			nextSlide();
		}, slideDuration);
	}
	
	function stopAutoplay() {
		if (autoplayTimer) {
			clearInterval(autoplayTimer);
			autoplayTimer = null;
		}
	}

	// Initialize carousel
	(function initializeCarousel() {
		if (!slidesContainer || !totalSlides) {
			console.error('Carousel initialization failed: missing elements');
			return;
		}
		
		console.log('✅ Initializing carousel with', totalSlides, 'slides');
		console.log('✅ Found dots:', dots.length);
		console.log('✅ Autoplay will start in 1 second');
		
		// Ensure starting position
		slidesContainer.style.transform = 'translateX(0%)';
		attachCarouselEvents();
		goToSlide(0);
		
		// Start autoplay after a short delay
		setTimeout(() => {
			console.log('🚀 Starting autoplay...');
			startAutoplay();
		}, 1000);
	})();

	// --- Témoignages slider (pile de cartes) ---
	(function enhanceTestimonials() {
		const tContainer = document.getElementById('testimonials');
		if (!tContainer) return;

		const tCards = tContainer.querySelectorAll('.temoignage-card');
		const tPrev = document.getElementById('t-prev');
		const tNext = document.getElementById('t-next');
		const tDots = tContainer.querySelectorAll('.t-dot');

		let tIndex = 0;
		let tTimer = null;

		function renderTestimonial(newIndex) {
			if (!tCards.length) return;
			tIndex = (newIndex + tCards.length) % tCards.length;
			tCards.forEach((card, i) => {
				const isActive = i === tIndex;
				card.style.opacity = isActive ? '1' : '0';
				card.style.zIndex = isActive ? '10' : '0';
				card.style.pointerEvents = isActive ? 'auto' : 'none';
				card.style.transform = isActive ? 'translateY(0)' : 'translateY(8px)';
			});
			tDots.forEach((dot, i) => {
				dot.classList.toggle('bg-primary-300', i === tIndex);
				dot.classList.toggle('bg-gray-300', i !== tIndex);
				dot.setAttribute('aria-selected', String(i === tIndex));
			});
		}

		function tNextSlide() { renderTestimonial(tIndex + 1); }
		function tPrevSlide() { renderTestimonial(tIndex - 1); }

		function startTestimonialAutoplay() {
			stopTestimonialAutoplay();
			tTimer = setInterval(tNextSlide, 6000);
		}
		function stopTestimonialAutoplay() {
			if (tTimer) clearInterval(tTimer);
			tTimer = null;
		}

		if (tPrev) tPrev.addEventListener('click', tPrevSlide);
		if (tNext) tNext.addEventListener('click', tNextSlide);
		tDots.forEach((dot, i) => dot.addEventListener('click', () => renderTestimonial(i)));
		tContainer.addEventListener('mouseenter', stopTestimonialAutoplay);
		tContainer.addEventListener('mouseleave', startTestimonialAutoplay);

		renderTestimonial(0);
		startTestimonialAutoplay();
	})();
});

