let games = [];
let currentIndex = 0;
let autoSlideInterval;

async function loadGames() {
  try {
    const response = await fetch("scripts/games.json");
    games = await response.json();
    games = games.sort(() => Math.random() - 0.5).slice(0, 9);
    renderCarousel();
    startAutoSlide();
  } catch (err) {
    console.error("Failed to load games.json", err);
  }
}

function renderCarousel() {
  const carousel = document.getElementById("game-carousel");
  carousel.innerHTML = "";

  const slidesCount = Math.ceil(games.length / 3);
  for (let i = 0; i < slidesCount; i++) {
    const slide = document.createElement("div");
    slide.className = "carousel-slide";
    if (i === 0) slide.classList.add("active");

    const group = games.slice(i * 3, i * 3 + 3);
    slide.innerHTML = `
      ${group
        .map(
          g => `
          <a href="../pages/games.html?game=${encodeURIComponent(g.id)}" class="carousel-link">
            <div class="carousel-image-container">
              <img src="${g.image}" alt="${g.title}">
              <div class="carousel-title">${g.title}</div>
            </div>
          </a>
        `
        )
        .join("")}
    `;
    carousel.appendChild(slide);
  }
}

function showSlide(index) {
  const slides = document.querySelectorAll(".carousel-slide");
  slides.forEach((slide, i) => {
    slide.classList.toggle("active", i === index);
  });
}

function nextSlide() {
  const slides = document.querySelectorAll(".carousel-slide");
  currentIndex = (currentIndex + 1) % slides.length;
  showSlide(currentIndex);
}

function startAutoSlide() {
  clearInterval(autoSlideInterval);
  autoSlideInterval = setInterval(nextSlide, 5000);
}

document.addEventListener("DOMContentLoaded", loadGames);
