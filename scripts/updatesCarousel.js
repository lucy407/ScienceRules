const updateImages = [
  { src: 'assets/image.png', title: 'Favoriting', description: 'Be not afraid, never miss out on any games anymore.'},
  { src: 'assets/image2.png', title: 'Themes', description: 'Add to your gaming experience with 9 new themes! ' },
  { src: 'assets/image3.png', title: 'Clock', description: 'Keep track of the time with our new clock feature. Dont be late to class!' },
  { src: 'assets/image4.png', title: 'Sleek & Responsive UI', description: 'Our new UI is sleek and responsive, making it easier to navigate the site.' },
  { src: 'assets/image5.png', title: 'Cookies', description: 'We now use cookies to track your preferences and improve your experience.' }
];

let currentUpdateIndex = 0;
let updateAutoSlideInterval;
let isCinematicView = false;

function renderUpdatesCarousel() {
  const carousel = document.getElementById('updates-carousel');
  if (!carousel) return;
  
  const slideContainer = carousel.querySelector('.update-slide-container');
  if (slideContainer) {
    slideContainer.removeEventListener('click', openCinematicView);
  }
  
  carousel.innerHTML = `
    <div class="update-slide-container">
      <img src="${updateImages[currentUpdateIndex].src}" alt="${updateImages[currentUpdateIndex].title}" class="update-slide-image" loading="lazy">
      <div class="update-slide-overlay">
        <p class="update-slide-text">See the newest updates</p>
      </div>
    </div>
  `;
  
  const newSlideContainer = carousel.querySelector('.update-slide-container');
  if (newSlideContainer) {
    newSlideContainer.addEventListener('click', openCinematicView);
  }
  
  if (!isCinematicView) {
    startAutoSlide();
  }
}

function startAutoSlide() {
  clearInterval(updateAutoSlideInterval);
  updateAutoSlideInterval = setInterval(() => {
    if (!isCinematicView) {
      currentUpdateIndex = (currentUpdateIndex + 1) % updateImages.length;
      renderUpdatesCarousel();
    }
  }, 4000);
}

function openCinematicView() {
  if (isCinematicView) return;
  isCinematicView = true;
  clearInterval(updateAutoSlideInterval);
  document.body.style.overflow = 'hidden';
  
  const existingOverlay = document.querySelector('.cinematic-overlay');
  if (existingOverlay) {
    existingOverlay.remove();
  }
  
  const cinematicOverlay = document.createElement('div');
  cinematicOverlay.className = 'cinematic-overlay';
  cinematicOverlay.innerHTML = `
    <button class="cinematic-exit" aria-label="Exit">✕</button>
    <div class="cinematic-content">
      <img src="${updateImages[currentUpdateIndex].src}" alt="${updateImages[currentUpdateIndex].title}" class="cinematic-image">
      <div class="cinematic-description">
        <h3>${updateImages[currentUpdateIndex].title}</h3>
        <p>${updateImages[currentUpdateIndex].description}</p>
      </div>
    </div>
    <div class="cinematic-nav">
      <button class="cinematic-nav-btn cinematic-prev" aria-label="Previous">←</button>
      <span class="cinematic-counter">${currentUpdateIndex + 1} / ${updateImages.length}</span>
      <button class="cinematic-nav-btn cinematic-next" aria-label="Next">→</button>
    </div>
  `;
  
  document.body.appendChild(cinematicOverlay);
  
  const exitBtn = cinematicOverlay.querySelector('.cinematic-exit');
  const prevBtn = cinematicOverlay.querySelector('.cinematic-prev');
  const nextBtn = cinematicOverlay.querySelector('.cinematic-next');
  
  exitBtn.addEventListener('click', closeCinematicView);
  prevBtn.addEventListener('click', () => navigateUpdate(-1));
  nextBtn.addEventListener('click', () => navigateUpdate(1));
  
  const keyHandler = (e) => {
    if (e.key === 'Escape') {
      closeCinematicView();
    } else if (e.key === 'ArrowLeft') {
      navigateUpdate(-1);
    } else if (e.key === 'ArrowRight') {
      navigateUpdate(1);
    }
  };
  
  document.addEventListener('keydown', keyHandler);
  cinematicOverlay._keyHandler = keyHandler;
}

function navigateUpdate(direction) {
  currentUpdateIndex = (currentUpdateIndex + direction + updateImages.length) % updateImages.length;
  const overlay = document.querySelector('.cinematic-overlay');
  if (overlay) {
    overlay.querySelector('.cinematic-image').src = updateImages[currentUpdateIndex].src;
    overlay.querySelector('.cinematic-image').alt = updateImages[currentUpdateIndex].title;
    overlay.querySelector('.cinematic-description h3').textContent = updateImages[currentUpdateIndex].title;
    overlay.querySelector('.cinematic-description p').textContent = updateImages[currentUpdateIndex].description;
    overlay.querySelector('.cinematic-counter').textContent = `${currentUpdateIndex + 1} / ${updateImages.length}`;
  }
}

function closeCinematicView() {
  const overlay = document.querySelector('.cinematic-overlay');
  if (overlay) {
    if (overlay._keyHandler) {
      document.removeEventListener('keydown', overlay._keyHandler);
    }
    overlay.remove();
  }
  isCinematicView = false;
  document.body.style.overflow = '';
  startAutoSlide();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', renderUpdatesCarousel);
} else {
  renderUpdatesCarousel();
}

