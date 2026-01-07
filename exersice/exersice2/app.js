// 地域リストAPI
const AREA_URL = "https://www.jma.go.jp/bosai/common/const/area.json";

// HTML要素取得
const areaSelect = document.getElementById("areaSelect");
const weatherDiv = document.getElementById("weather");

// 地域リストを取得して表示
fetch(AREA_URL)
  .then(response => response.json())
  .then(data => {
    const offices = data.offices;

    for (const code in offices) {
      const option = document.createElement("option");
      option.value = code;
      option.textContent = offices[code].name;
      areaSelect.appendChild(option);
    }
  })
  .catch(error => {
    console.error("地域リストの取得に失敗しました", error);
  });

// 地域が選択されたら天気予報を取得
areaSelect.addEventListener("change", () => {
  const areaCode = areaSelect.value;

  if (areaCode === "") {
    weatherDiv.textContent = "";
    return;
  }

  const FORECAST_URL =
    `https://www.jma.go.jp/bosai/forecast/data/forecast/${areaCode}.json`;

  fetch(FORECAST_URL)
    .then(response => response.json())
    .then(data => {
      // 今日の天気を取得
      const weather =
        data[0].timeSeries[0].areas[0].weathers[0];

      weatherDiv.textContent = `今日の天気：${weather}`;
    })
    .catch(error => {
      console.error("天気予報の取得に失敗しました", error);
      weatherDiv.textContent = "天気情報を取得できませんでした。";
    });
});
