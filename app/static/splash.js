$(document).ready(function () {
  // when user selects a specific card, grab its attributes to populate the modal
  $(".card").click(function () {
    let card = $(this)
    // get contents of clicked shoe
    let shoeURL = card.find("a.shoeURL").attr("href");
    let shoeName= card.find("h3.shoeName").text();
    let shoeImage = card.find("img.shoeImage").attr("src");

    console.log(shoeURL, shoeName, shoeImage);

    // populate modal 
    let modal = $(".modal-content");
    modal.find(".modal-shoeURL").attr("href", shoeURL);
    modal.find(".modal-shoeImage").attr("href", shoeImage);
    modal.find(".modal-shoeName").text(shoeName);
    
  });

});