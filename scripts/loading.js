const style = document.createElement('style');
style.textContent = `
  #loader-overlay {
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100vh;
    background: radial-gradient(circle at center, #001319 0%, #000000 90%);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
    transition: opacity 0.6s ease;
    overflow: hidden;
  }

  #loader-overlay::before {
    content: "";
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
      to bottom,
      rgba(0, 255, 204, 0.05) 0px,
      rgba(0, 255, 204, 0.05) 2px,
      transparent 3px,
      transparent 4px
    );
    animation: scan 3s linear infinite;
    pointer-events: none;
  }

  @keyframes scan {
    0% { background-position: 0 0; }
    100% { background-position: 0 100px; }
  }

  .loader-container {
    text-align: center;
    color: #00ffcc;
    font-family: 'VT323', monospace;
    z-index: 2;
  }

  .loader-logo {
    width: 120px;
    height: 120px;
    filter: drop-shadow(0 0 20px #00ffcc);
    animation: spin 3s linear infinite, glow 1.5s ease-in-out infinite alternate;
    margin-bottom: 20px;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  @keyframes glow {
    0% { filter: drop-shadow(0 0 5px #00ffee); }
    100% { filter: drop-shadow(0 0 25px #00ffee); }
  }

  .loader-text {
    font-size: 1.2em;
    letter-spacing: 2px;
    text-shadow: 0 0 10px #00ffee;
    animation: blinkText 1.5s infinite;
  }

  @keyframes blinkText {
    50% { opacity: 0.6; }
  }

  #loader-overlay.fade-out {
    opacity: 0;
    pointer-events: none;
  }
`;
document.head.appendChild(style);

const loaderOverlay = document.createElement('div');
loaderOverlay.id = 'loader-overlay';
loaderOverlay.innerHTML = `
  <div class="loader-container">
    <img src="../assets/atom.png" alt="Loading..." class="loader-logo">
    <p class="loader-text">INITIALIZING SYSTEM...</p>
  </div>
`;
document.body.appendChild(loaderOverlay);

function checkReady() {
  if (document.readyState === 'complete') {
    loaderOverlay.classList.add('fade-out');
    setTimeout(() => loaderOverlay.remove(), 800);
  } else {
    requestAnimationFrame(checkReady);
  }
}

window.addEventListener('load', checkReady);
document.addEventListener('readystatechange', checkReady);