document.addEventListener("DOMContentLoaded", () => {
  const isMobile =
    /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
      navigator.userAgent
    ) || window.innerWidth <= 700;

  const popupDismissed = localStorage.getItem("mobilePopupDismissed");

  if (isMobile && !popupDismissed) {
    const popup = document.createElement("div");
    popup.id = "mobile-popup";
    popup.innerHTML = `
      <div class="popup-content">
        <h2>Heads up!</h2>
        <p>Games work best on PC for smoother performance and features.</p>
        <button id="close-popup">Got it</button>
      </div>
    `;
    document.body.appendChild(popup);

    const closeBtn = document.getElementById("close-popup");
    if (closeBtn) {
      closeBtn.addEventListener("click", () => {
        document.body.classList.add("mobile-mode");
        popup.style.opacity = "0";
        setTimeout(() => popup.remove(), 400);
        localStorage.setItem("mobilePopupDismissed", "true");
      });
    }
  } else if (isMobile) {
    document.body.classList.add("mobile-mode");
  }
});
