
let $SCRIPT_ROOT = ""
$(document).ready(function () {
  // when user selects a specific card, grab its attributes to populate the modal
  $(".card").click(function () {
    let card = $(this)
    // get contents of clicked shoe
    let shoeName= card.find("h3.shoeName").text();
    let shoeImage = card.find("img.shoeImage").attr("src");

    console.log(shoeName, shoeImage);

    // populate modal 
    let modal = $(".modal-content");
    modal.find(".modal-shoeName").text(shoeName);
    modal.find(".modal-shoeImage").attr("href", shoeImage);
    
  });

  // rendering template for a card
  // will need to handle which mode we're in
  let render_card = (shoe) => {
    console.log("Rendering template data");
    let card_template =
    `
    <div class="card" data-toggle="modal" data-target="#exampleModalCenter">
      <figure>
        <img class="shoeImage" src="${shoe.shoeImage}">
      </figure>
      <div class="card-caption">
        <h3 class="shoeName"> ${shoe.shoeName}</h3>
      </div>
    </div>
    `
    $(".shoes-grid").append(card_template);
  }

  // Conducts the ajax request and renders the results
  let ajax_retrieve = (query) => {
    $.getJSON($SCRIPT_ROOT + '/retrieve', {
      search: query,
    }, function (data) {
      console.log("AJAX RETURNED DATA: ")
      console.log(data);
      data.map(render_card);
    });

  };

  // wrapper, clears the data and fetches results
  let clear_and_search = (query) => {
    $(".shoes-grid").empty();
    ajax_retrieve(query);
  }

  // Click handler, TODO: modify for press of enter
  $('#go').bind('click', function () {
    let inputted_value = $('input[name="search"]').val();
    clear_and_search(inputted_value);
    return false;
  });

  // generate amazon link dynamically from name, allows us to handle if we want to filter by gender or size
  let amazonGenderSizeAdjuster = (amzURL, gender="", size="") => {
    let gender_adjusted = (gender == "") ? gender : `+${gender}`;
    let size_adjusted = (size == "") ? size : `+${size}`;
    return `https://www.amazon.com/s?k=${amzURL}${gender_adjusted}${size_adjusted}`;
  }

  // Onpage load a shoe:
  ajax_retrieve("Nike Air Zoom Pegasus 35");

  
});


    