const style = document.createElement('style');
style.textContent = `
  #loader-overlay {
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100vh;
    background: #111;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
    transition: opacity 0.5s ease;
  }
  .loader-container {
    text-align: center;
  }
  .loader-logo {
    width: 100px;
    height: 100px;
    animation: spin 1s linear infinite;
    margin-bottom: 10px;
  }
  #loader-overlay.fade-out {
    opacity: 0;
    pointer-events: none;
  }
  @keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }
`;
document.head.appendChild(style);

const loaderOverlay = document.createElement('div');
loaderOverlay.id = 'loader-overlay';
loaderOverlay.innerHTML = `
  <div class="loader-container">
    <img src="../assets/atom.png" alt="Loading..." class="loader-logo">
    <p style="color:#00eaff;font-family:'Montserrat';font-weight:bold;">Loading...</p>
  </div>
`;
document.body.appendChild(loaderOverlay);

function checkReady() {
  if (document.readyState === 'complete') {
    loaderOverlay.classList.add('fade-out');
    setTimeout(() => loaderOverlay.remove(), 600);
  } else {
    requestAnimationFrame(checkReady);
  }
}

window.addEventListener('load', checkReady);
document.addEventListener('readystatechange', checkReady);
