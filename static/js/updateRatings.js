const button=document.querySelector("#rating-edit-button");

button.addEventListener('click', ()=>{
    document.querySelector("#edit-rating-div").style.display=""
})


function updateRatings(evt) {
    evt.preventDefault();
    const formInputs = {
      rating_score: document.querySelector('#restaurant-score').value,
      rating_comment: document.querySelector('#comment').value,
      unique_restaurant_id: document.querySelector('#unique-restaurant-id').value,
    };
    fetch('/update_ratings', {
      method: 'POST',
      body: JSON.stringify(formInputs),
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((response) => response.json())
      .then((response) => {
        document.querySelector("#rating-score").innerHTML = `Rating: ${response.score} out of 5`;
        document.querySelector("#rating-comment").innerHTML = response.comment;
        document.querySelector("#edit-rating-div").style.display="none"
      });
        
    
  }
  
  document.querySelector('#edit-rating-form').addEventListener('submit', updateRatings);
  