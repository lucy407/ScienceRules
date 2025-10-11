let games = [];
let currentIndex = 0;
let autoSlideInterval;

async function loadGames() {
  try {
    const response = await fetch("scripts/games.json");
    games = await response.json();
    games = games.sort(() => 0.5 - Math.random()).slice(0, 9);
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

    const gamesGroup = games.slice(i * 3, i * 3 + 3);
    const gamesHTML = gamesGroup.map(game => `
      <a href="../pages/games.html?game=${encodeURIComponent(game.id)}" class="carousel-link">
        <div class="carousel-image-container">
          <img src="${game.image}" alt="${game.title}">
          <div class="carousel-title">${game.title}</div>
        </div>
      </a>
    `).join("");

    slide.innerHTML = `<div class="carousel-grid">${gamesHTML}</div>`;
    carousel.appendChild(slide);
  }
}

function showSlide(index) {
  const slides = document.querySelectorAll(".carousel-slide");
  slides.forEach((slide, i) => {
    slide.classList.toggle("active", i === index);
  });
}

function prevSlide() {
  const slides = document.querySelectorAll(".carousel-slide");
  currentIndex = (currentIndex - 1 + slides.length) % slides.length;
  showSlide(currentIndex);
}

function nextSlide() {
  const slides = document.querySelectorAll(".carousel-slide");
  currentIndex = (currentIndex + 1) % slides.length;
  showSlide(currentIndex);
}

function startAutoSlide() {
  if (autoSlideInterval) clearInterval(autoSlideInterval);
  autoSlideInterval = setInterval(nextSlide, 5000);
}

document.addEventListener("DOMContentLoaded", loadGames);
