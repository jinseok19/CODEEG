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
  const element = document.querySelector("main");
  
  const opt = {
    margin: [0.5, 0.5, 0.5, 0.5],
    filename: "CODEEG_report.pdf",
    image: { type: "jpeg", quality: 0.95 },
    html2canvas: { 
      scale: 2,
      useCORS: true,
      letterRendering: true,
      scrollY: 0,
      windowWidth: document.documentElement.scrollWidth
    },
    jsPDF: { 
      unit: "in",
      format: [8.5, 18],
      orientation: "portrait",
      compress: true
    },
    pagebreak: { 
      mode: ['css', 'legacy'],
      before: '.page-break',
      after: '.page-break',
      avoid: '.avoid-page-break'
    },
    enableLinks: false
  };

  // PDF의 세로 크기 조정
  const contentHeight = element.scrollHeight / 90; // 96 DPI 기준으로 계산
  opt.jsPDF.format = [11.7, contentHeight]; // 가로는 고정, 세로는 내용에 맞춤

  // 직접 PDF 생성 및 저장
  html2pdf().set(opt).from(element).save();
}

