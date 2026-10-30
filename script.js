// fills the hevy card from hevy.json (a github action updates that file daily)
function daysAgo(dateString) {
  const days = Math.floor((Date.now() - new Date(dateString)) / 86400000);
  if (days <= 0) return "today";
  if (days === 1) return "yesterday";
  return days + "d ago";
}

const recentBox = document.getElementById("hevy-recent");

if (recentBox) {
  fetch("hevy.json")
    .then((res) => res.json())
    .then((data) => {
      document.getElementById("hevy-total").textContent = data.workout_count;
      document.getElementById("hevy-week").textContent = data.this_week;
      document.getElementById("hevy-streak").textContent = data.streak_weeks;
      document.getElementById("hevy-updated").textContent = "from hevy · updated " + daysAgo(data.updated);

      recentBox.innerHTML = "";
      data.recent.forEach((w) => {
        const row = document.createElement("div");
        row.className = "workout";
        row.innerHTML = "<div><b></b><span></span></div><small></small>";
        row.querySelector("b").textContent = w.title.toLowerCase();
        row.querySelector("span").textContent = w.exercises + " exercises · " + w.minutes + " min";
        row.querySelector("small").textContent = daysAgo(w.date);
        recentBox.appendChild(row);
      });
    })
    .catch(() => {
      recentBox.innerHTML = '<div class="workout"><div><b>stats load once the site is online</b><span>see the readme</span></div></div>';
    });
}
