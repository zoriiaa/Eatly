// Progress Bars - Universal function for updating circular progress indicators
function updateProgressBars() {
  // Update nutrient progress circles
  document.querySelectorAll('.nutrient[data-progress]').forEach(function (nutrient) {
    const progress = parseInt(nutrient.getAttribute('data-progress')) || 0;
    const progressCircle = nutrient.querySelector('.nutrient__progress-circle');

    if (progressCircle) {
      const radius = parseInt(progressCircle.getAttribute('r')) || 40;
      const circumference = 2 * Math.PI * radius;
      const offset = circumference - (progress / 100) * circumference;

      progressCircle.style.strokeDasharray = `${circumference} ${circumference}`;
      progressCircle.style.strokeDashoffset = offset;
    }
  });

  // Update main calorie diagram
  const mainDiagram = document.querySelector('.calorie-diagram [data-progress]');
  if (mainDiagram) {
    const progress = parseInt(mainDiagram.getAttribute('data-progress')) || 0;
    const radius = parseInt(mainDiagram.getAttribute('r')) || 102;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (progress / 100) * circumference;

    mainDiagram.style.strokeDasharray = `${circumference} ${circumference}`;
    mainDiagram.style.strokeDashoffset = offset;
  }
}

// Auto-initialize on page load
document.addEventListener('DOMContentLoaded', updateProgressBars);
