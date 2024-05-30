const SERVER_URL = "http://127.0.0.1:8000";
const WEATHER_ICON_URL = "http://openweathermap.org/img/w/"



const showLoader = () => {
    let loader = document.querySelector(".pre-loader");
    loader.style.display="flex";
}

const hideLoader = () => {
    let loader = document.querySelector(".pre-loader");
    loader.style.display="none";
}





showLoader();
const currentLocation = navigator.geolocation.getCurrentPosition(async (position) => {
    let [lat, lon] = [position.coords.latitude, position.coords.longitude];
    let response = await fetch(`${SERVER_URL}/api/weather/current?lat=${lat}&lon=${lon}`);
    if (response.status === 200) {
        let data = await response.json()
        populateData(data)
    } else {
        console.log(await response.text())
    }
    hideLoader();
}, (err) => {
    hideLoader();
    console.log(err);
});



const searchWeather = async (e) => {
    e.preventDefault();
    showLoader()
    let response = await fetch(`${SERVER_URL}/api/weather/city?city=${e.target.elements.city.value}`)
    if (response.status === 200) {
        let data = await response.json()
        populateData(data)
        hideLoader()
    } else {
        console.log(await response.text())
    }
}


const populateData = (data) => {
    let temperatureSection = document.querySelector(".container .temperature");
    temperatureSection.querySelector("div h2").innerHTML=data.city
    temperatureSection.querySelector("div p").innerHTML=`Humidity: ${data.humidity}%`
    temperatureSection.querySelector("h1").innerHTML=`${data.temp}°C`
    temperatureSection.querySelector("img").src=`${WEATHER_ICON_URL}${data.icon}.png`

    let dom = "";
    data.today_forecast.forEach((forecast, index)=>{
        dom+=`<div class="card">
            <p>${forecast.time}</p>
            <img src="${WEATHER_ICON_URL}${forecast.icon}.png" alt="...">
            <h3>${forecast.temp}°</h3>
        </div>`
    })
    document.querySelector(".forecast .forecast-cards").innerHTML=dom
    
    let airConditionSection = document.querySelectorAll(".details .air-conditions .conditions h3");
    airConditionSection[0].innerHTML=`${data.real_feel}°C`
    airConditionSection[1].innerHTML=`${data.wind} Km/h`
    airConditionSection[2].innerHTML=`${data.humidity}%`
    airConditionSection[3].innerHTML=`${Math.round(data.visibility/1000)} Km`

    dom = "";
    for(let i=0; i < data.week_forecast.length; i+=8) {
        dom+=`<div class="cards">
            <p class="day">${data.week_forecast[i].time}</p>
            <div>
                <img src="${WEATHER_ICON_URL}${data.week_forecast[i].icon}.png" alt="...">
                <p class="description">${data.week_forecast[i].description}</p>
            </div>
            <p class="temp">${data.week_forecast[i].temp}°C</p>
        </div>`
    }
    document.querySelector(".daily-forecast .daily-forecast-cards").innerHTML=dom
}