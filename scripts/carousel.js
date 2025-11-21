let games = [];
let currentIndex = 0;
let autoSlideInterval;

async function loadGames() {
  try {
    const response = await fetch("scripts/games.json");
    if (!response.ok) throw new Error('Failed to fetch games');
    games = await response.json();
    games = games.sort(() => Math.random() - 0.5).slice(0, 9);
    renderCarousel();
    startAutoSlide();
  } catch (err) {
    console.error("Failed to load games.json", err);
    const carousel = document.getElementById("game-carousel");
    if (carousel) carousel.innerHTML = '<p style="color: #ccc; padding: 20px;">Failed to load games. Please refresh the page.</p>';
  }
}

function renderCarousel() {
  const carousel = document.getElementById("game-carousel");
  if (!carousel) return;
  carousel.innerHTML = "";

  const slidesCount = Math.ceil(games.length / 3);
  for (let i = 0; i < slidesCount; i++) {
    const slide = document.createElement("div");
    slide.className = "carousel-slide";
    if (i === 0) slide.classList.add("active");

    const group = games.slice(i * 3, i * 3 + 3);
    function escapeHtml(text) {
      const div = document.createElement('div');
      div.textContent = text;
      return div.innerHTML;
    }
    
    slide.innerHTML = group
      .map(
        g => {
          const safeTitle = escapeHtml(g.title);
          const safeUrl = escapeHtml(g.url);
          const safeImage = escapeHtml(g.image);
          return `
          <a href="${safeUrl}" class="carousel-link">
            <div class="carousel-image-container">
              <img src="${safeImage}" alt="${safeTitle}" loading="lazy">
              <div class="carousel-title">${safeTitle}</div>
            </div>
          </a>
        `;
        }
      )
      .join("");
    carousel.appendChild(slide);
  }
}

function showSlide(index) {
  const slides = document.querySelectorAll(".carousel-slide");
  if (slides.length === 0) return;
  slides.forEach((slide, i) => {
    slide.classList.toggle("active", i === index);
  });
}

function nextSlide() {
  const slides = document.querySelectorAll(".carousel-slide");
  if (slides.length === 0) return;
  currentIndex = (currentIndex + 1) % slides.length;
  showSlide(currentIndex);
}

function startAutoSlide() {
  clearInterval(autoSlideInterval);
  autoSlideInterval = setInterval(nextSlide, 5000);
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', loadGames);
} else {
  loadGames();
}
