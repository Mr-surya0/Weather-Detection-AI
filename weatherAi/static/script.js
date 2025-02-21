document.getElementById('weatherForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  // Get the city input from the form
  const city = document.getElementById('cityInput').value;

  // Send POST request to Flask server
  const response = await fetch('http://127.0.0.1:5000/weather', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ intent: 'GetCurrentWeather', city })
  });
  

  // Parse the response JSON
  const data = await response.json();

  if (data.error) {
    alert(data.error);  // Show error if any
    return;
  }

  // Display weather information
  document.getElementById('cityName').textContent = data.city;
  document.getElementById('temperature').textContent = `Temperature: ${data.temperature}`;
  document.getElementById('weatherDescription').textContent = `Weather: ${data.current_weather}`;

  // Update weather animation based on the weather description
  const weatherAnimation = document.getElementById('weatherAnimation');
  weatherAnimation.innerHTML = '';  // Clear previous animation

  if (data.current_weather.includes('rain')) {
    weatherAnimation.classList.add('rain');
    for (let i = 0; i < 50; i++) {
      const drop = document.createElement('div');
      drop.className = 'rain-drop';
      drop.style.left = `${Math.random() * 100}%`;
      drop.style.animationDelay = `${Math.random()}s`;
      weatherAnimation.appendChild(drop);
    }
  } else if (data.current_weather.includes('clear')) {
    weatherAnimation.classList.add('sun');
    const sun = document.createElement('div');
    sun.className = 'sun';
    weatherAnimation.appendChild(sun);
  } else {
    weatherAnimation.classList.add('spring');
    for (let i = 0; i < 10; i++) {
      const leaf = document.createElement('div');
      leaf.className = 'leaf';
      leaf.style.left = `${Math.random() * 100}%`;
      leaf.style.animationDelay = `${Math.random()}s`;
      weatherAnimation.appendChild(leaf);
    }
  }
});
