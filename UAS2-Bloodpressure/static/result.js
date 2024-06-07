document.addEventListener('DOMContentLoaded', function () {
  const resultBox = document.getElementById('resultBox');
  const premiValue = {{ result|tojson|safe }};  // Dapatkan nilai premi dari Flask

  if (premiValue !== null) {
    resultBox.textContent = `Biaya Premi: ${premiValue} untuk ${document.getElementById('lamaTahunSelect').value} Tahun`;
  } else {
    resultBox.textContent = "Tidak dapat menghitung premi. Harap masukkan nilai yang valid.";
  }
});

document.getElementById('lamaTahunSelect').addEventListener('change', function () {
  const resultBox = document.getElementById('resultBox');
  resultBox.textContent = `Biaya Premi untuk ${this.value} Tahun`;
});

