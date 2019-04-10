
let $SCRIPT_ROOT = ""
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

  let render_card = (shoe) => {
    let card_template =
    `
    <div class="card" data-toggle="modal" data-target="#exampleModalCenter">
      <figure>
        <img class="shoeImage" src="${shoe.shoeImage}">
      </figure>
      <div class="card-caption">
        <h3 class="shoeName"> ${shoe.shoeName}</h3>
        <a class="shoeURL" target="_blank" href="${shoe.shoeURL}">Shoe Link</a>
      </div>
    </div>
    `
    console.log(typeof(card_template));
    $(".shoes-grid").append(card_template);
  }

  // AJAX
  $('#go').bind('click', function () {
    $.getJSON($SCRIPT_ROOT + '/retrieve', {
      search: $('input[name="search"]').val(),
    }, function (data) {
      console.log("AJAX RETURNED DATA: ")
      console.log(data);
      // remove old recommendations
      $(".shoes-grid").empty();

      data.map (shoe => render_card (shoe))
    });
    return false;
  });
});


    