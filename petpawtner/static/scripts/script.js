const factContainer = document.getElementById('dog-facts');

async function fetchDogFact() {
   try {
      const response = await fetch('https://dog-api.kinduff.com/api/facts?number=2');
      const data = await response.json();
      return data.facts[0];
   } catch (error) {
      return 'Failed to fetch a dog fact. Please try again later.';
   }
}

async function displayDogFact() {
   const fact = await fetchDogFact();
   factContainer.textContent = fact;

   // Set the next fact to display after 5 seconds
   setTimeout(displayDogFact, 10000);
}

// Start the loop
displayDogFact();

// Function to fetch dog breeds and populate the select element
function fetchBreeds() {
   const breedSelect = document.getElementById('breed-select');

   fetch('https://dog.ceo/api/breeds/list/all')
      .then(response => response.json())
      .then(data => {
         const breeds = data.message; // Breeds are returned in the message property

         for (const breed in breeds) {
            const option = document.createElement('option');
            option.value = breed;
            option.textContent = breed.charAt(0).toUpperCase() + breed.slice(1); // Capitalize breed name
            breedSelect.appendChild(option);
         }
      })
      .catch(error => {
         console.error('Error fetching dog breeds:', error);
      });
}

// Call the fetchBreeds function when the page loads
window.onload = fetchBreeds;