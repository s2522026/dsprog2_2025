const AREA_URL = "https://www.jma.go.jp/bosai/common/const/area.json";

const areaSelect = document.getElementById("areaSelect");
const weatherDiv = document.getElementById("weather");
const dateInput = document.getElementById("dateInput");
const historyBtn = document.getElementById("historyBtn");

// 地域リスト取得
fetch(AREA_URL)
  .then(res => res.json())
  .then(data => {
    const offices = data.offices;
    for (const code in offices) {
      const option = document.createElement("option");
      option.value = code;
      option.textContent = offices[code].name;
      areaSelect.appendChild(option);
    }
  });

// 今日の天気（API → DB保存）
areaSelect.addEventListener("change", () => {
  const areaCode = areaSelect.value;
  if (!areaCode) return;

  fetch(`/forecast/${areaCode}`)
    .then(res => res.json())
    .then(data => {
      weatherDiv.textContent =
        `${data.area}（${data.date}）の天気：${data.weather}`;
    });
});

// 過去の天気（DB参照）
historyBtn.addEventListener("click", () => {
  const areaCode = areaSelect.value;
  const date = dateInput.value;

  if (!areaCode || !date) {
    alert("地域と日付を選択してください");
    return;
  }

  fetch(`/history/${areaCode}/${date}`)
    .then(res => res.json())
    .then(data => {
      weatherDiv.textContent =
        `${date} の天気：${data.weather}`;
    });
});
