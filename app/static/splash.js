
let $SCRIPT_ROOT = ""

$(document).on("click", '.card', function () {
  // when user selects a specific card, grab its attributes to populate the modal
  let card = $(this);
  console.log("CLICKED");
  // get contents of clicked shoe
  let shoeName = card.find(".card-shoeName").text();
  let shoeImage = card.find(".card-shoeImage").attr("src");
  let similarShoes = card.find(".card-similarShoes").text();
  let corescore = card.find(".card-corescore").text();
  let similarity = card.find(".card-similarity").text();
  let relevantTerms = card.find(".card-relevantTerms").text();
  let terrain = card.find(".card-terrain").text();
  let arch_support = card.find(".card-arch_support").text();
  let men_weight = card.find(".card-men_weight").text();
  let women_weight = card.find(".card-women_weight").text();

  console.log(shoeName, shoeImage, similarShoes, corescore, similarity, relevantTerms);

  // populate modal 
  let modal = $(".modal-content");
  modal.find(".modal-shoeImage").html("<b>shoeImage</b> "+shoeImage);
  modal.find(".modal-shoeName").html("<b>shoeName</b> "+shoeName);
  modal.find(".modal-similarShoes").html("<b>similarShoes</b> "+similarShoes);
  modal.find(".modal-corescore").html("<b>corescore</b> "+corescore);
  modal.find(".modal-similarity").html("<b>similarity</b> "+similarity);
  modal.find(".modal-relevantTerms").html("<b>relevantTerms</b> "+relevantTerms);
  modal.find(".modal-amazonLink").html("<b>amazonLink</b> " + amazonLink);
  modal.find(".modal-terrain").html("<b>terrain</b> " + terrain);
  modal.find(".modal-arch_support").html("<b>arch_support</b> " + arch_support);
  modal.find(".modal-men_weight").html("<b>men_weight</b> " + men_weight);
  modal.find(".modal-women_weight").html("<b>women_weight</b> " + women_weight);
});
  

$(document).ready(function () {
  // rendering template for a card
  // will need to handle which mode we're in
  let render_card = (shoe) => {
    // console.log("Rendering template data");
    let card_template =
    `
    <div class="card" data-toggle="modal" data-target="#exampleModalCenter">
      <figure>
        <img class="card-shoeImage" src="${shoe.shoeImage}">
      </figure>
      <div class="card-caption">
        <h3 class="card-shoeName"> ${shoe.shoeName}</h3>
      </div>
      <div class="additional-data">
        <p class="card-similarShoes"> ${shoe.similarShoes}</p>
        <p class="card-corescore"> ${shoe.corescore}</p>
        <p class="card-similarity"> ${shoe.similarity}</p>
        <p class="card-relevantTerms"> ${shoe.relevantTerms}</p>
        <p class="card-amazonLink"> ${shoe.amazonLink}</p>
        <p class="card-terrain"> ${shoe.terrain}</p>
        <p class="card-arch_support"> ${shoe.arch_support}</p>
        <p class="card-men_weight"> ${shoe.men_weight}</p>
        <p class="card-women_weight"> ${shoe.women_weight}</p>
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

  // grab and perform input
  let input_handler = () => {
    let inputted_value = $('input[name="search"]').val();
    clear_and_search(inputted_value);
    return false;
  }

  // Click handler, TODO: modify for press of enter
  $('#go').bind('click', function () {
    input_handler();
  });
  // Handle for click of enter
  $("#input").on('keypress', function (e) {
    if (e.which == 13) {
      input_handler();
    }
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


    