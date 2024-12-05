document.addEventListener("DOMContentLoaded", function () {
  const dropdownToggles = document.querySelectorAll(".dropdown-toggle");
  dropdownToggles.forEach((dropdown) => {
    new bootstrap.Dropdown(dropdown);
  });
});

// Add a click event listener to the button
document.querySelector(".icon-button").addEventListener("click", () => {
  alert("Icon button clicked!");
});

document.querySelector(".dropdown-toggle").addEventListener("click", function () {
  const isExpanded = this.getAttribute("aria-expanded") === "true";
  this.setAttribute("aria-expanded", !isExpanded);
});

function generatePDF() {
  // PDF로 변환할 요소
  const element = document.querySelector("main");

  // PDF 설정
  const opt = {
    margin: 1,
    filename: "CODEEG_report.pdf",
    image: { type: "jpeg", quality: 0.98 },
    html2canvas: { scale: 2 },
    jsPDF: { unit: "in", format: "a4", orientation: "portrait" }
  };

  // PDF 생성
  html2pdf().set(opt).from(element).save();
}
