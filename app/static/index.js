
let $SCRIPT_ROOT = ""

// wrapper, clears the data and fetches results
let clear_and_search = (query, endpoint) => {
  $(".shoes-grid").empty();
  ajax_retrieve(query, endpoint);
}

// grab and perform input
let input_handler = (endpoint) => {
  let inputted_value = $('input[name="search"]').val();
  clear_and_search(inputted_value, endpoint);
  return false;
}

// Conducts the ajax request and renders the results
let ajax_retrieve = (query, endpoint) => {
  $.getJSON($SCRIPT_ROOT + endpoint, {
    search: query,
  }, function (data) {
    console.log("AJAX RETURNED DATA: ")
    console.log(data);
    // NEED TO ADD A CATCH FOR THE SERVER NOT TO FAIL
    (data.length > 0) ? data.map(render_card) : render_empty();
  });
};

let reload_page = () => location.reload();

// rendering template for a card
// will need to handle which mode we're in
let render_card = (shoe) => {
  console.log("Rendering template data");
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

let render_empty = () => {
  let empty = 
  `
  <div class="empty">
    <h3> No results found :( </h3>
  </div>
  `
  $(".shoes-grid").append(empty);
}

$(document).on("click", '.card', function () {
  // when user selects a specific card, grab its attributes to populate the modal
  let card = $(this);
  console.log("CLICKED");
  // get contents of clicked shoe
  let shoeName = card.find(".card-shoeName").text();
  let similarShoes = card.find(".card-similarShoes").text();
  let corescore = card.find(".card-corescore").text();
  let similarity = card.find(".card-similarity").text();
  let relevantTerms = card.find(".card-relevantTerms").text();
  let amazonLink = card.find(".card-amazonLink").text();
  let terrain = card.find(".card-terrain").text();
  let arch_support = card.find(".card-arch_support").text();
  let men_weight = card.find(".card-men_weight").text();
  let women_weight = card.find(".card-women_weight").text();

  console.log(shoeName, similarShoes, corescore, similarity, relevantTerms, terrain, arch_support, men_weight, women_weight);

  // populate modal 
  let modal = $(".modal-content");
  modal.find(".modal-shoeName").html("<b>shoeName</b> " + shoeName);
  modal.find(".modal-similarShoes").html("<b>similarShoes</b> " + similarShoes);
  modal.find(".modal-corescore").html("<b>corescore</b> " + corescore);
  modal.find(".modal-similarity").html("<b>similarity</b> " + similarity);
  modal.find(".modal-relevantTerms").html("<b>relevantTerms</b> " + relevantTerms);
  modal.find(".modal-amazonLink").html("<b>amazonLink</b> " + amazonLink);
  modal.find(".modal-terrain").html("<b>terrain</b> " + terrain);
  modal.find(".modal-arch_support").html("<b>arch_support</b> " + arch_support);
  modal.find(".modal-men_weight").html("<b>men_weight</b> " + men_weight);
  modal.find(".modal-women_weight").html("<b>women_weight</b> " + women_weight);
});


$(document).ready(function () {

  $('#go').bind('click', function () {
    input_handler("/custom_search");
  });
  // Handle for click of enter
  $("#input").on('keypress', function (e) {
    if (e.which == 13) {
      input_handler("/custom_search");
    }
  });

  $(".header h1").bind('click', function () {
    reload_page();
  })

  let render_search_section = (search_content_id) => {
    $(".landing-cards").fadeOut("slow", function () {
      $(search_content_id).fadeIn("slow");
    });
  }

  $("#similar-search").on("click", function (){
    render_search_section("#similar-search-content");
  });

  $("#custom-search").on("click", function () {
    render_search_section("#custom-search-content");
  });

  
  


  //generate bar chart
  // function create_bar_chart(key, chart_data_raw) {

  //   const margin = { top: 30, right: 30, bottom: 30, left: 30 };

  //   let svg = d3.select("#bar_chart");
  //   let height = svg.attr("height");
  //   let width = svg.attr("width");
  //   let plotHeight = height - margin.top - margin.bottom;
  //   let plotWidth = width - margin.right - margin.left;

  //   let chart_data_keys = keys.splice(0, 5);
  //   let chart_data = chart_data_raw.splice(0, 5);

  //   let max_count = d3.max(chart_data_raw, function (key) {
  //     return key;
  //   });

  //   let bar_width = (plotWidth - margin.left) / 5;
  //   let padding = 10;

  //   let range = [...Array(5).keys()].map(d => d * (plotWidth - margin.left) / 5);

  //   let xScale = d3.scaleOrdinal()
  //     .domain(chart_data_keys)
  //     .range(range);

  //   let yScale = d3.scaleLinear()
  //     .domain([0, max_count])
  //     .range([plotHeight, margin.bottom]);

  //   let plot = svg.append("g")
  //     .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  //   //create bar chart
  //   plot.selectAll("rect")
  //     .data(chart_data_keys)
  //     .enter()
  //     .append("rect")
  //     .attr("class", "chart_rect")
  //     .attr("x", function (d) {
  //       return xScale(d);
  //     })
  //     .attr("y", function (d) {
  //       return yScale(chart_data[d]) + 10;
  //     })
  //     .attr("stroke", function (d) {
  //       return "black";
  //     })
  //     .attr("width", bar_width)
  //     .attr("height", function (d) {
  //       return plotHeight - yScale(chart_data[d]);
  //     })
  //     .attr("fill", "orange")
  //     .style("stroke", "white")
  //     .style("stroke-width", 4);

  //   //create Y-labels
  //   plot.selectAll("text")
  //     .data(chart_data_keys)
  //     .enter()
  //     .append("text")
  //     .attr("class", "chart_text_y")
  //     .text(function (d) {
  //       return chart_data[d];
  //     })
  //     .attr("x", function (d) {
  //       return xScale(d) + bar_width / 2;
  //     })
  //     .attr("y", function (d) {
  //       return yScale(chart_data[d]) + 30;
  //     })
  //     .attr("alignment-baseline", "middle")
  //     .attr('text-anchor', "middle")
  //     .attr("fill", "white");

  //   //create x-labels
  //   let xLabels = svg.append("g")
  //     .attr("transform", "translate(" + margin.left + "," + (margin.top + plotHeight) + ")");

  //   xLabels.selectAll("text.xAxis")
  //     .data(chart_data_keys)
  //     .enter()
  //     .append("text")
  //     .attr("class", "xAxis")
  //     .text(function (d) {
  //       return d;
  //     })
  //     .attr("font-size", "13px")
  //     .attr("text-anchor", "middle")
  //     .attr("x", function (d) {
  //       return xScale(d) + bar_width / 2;
  //     })
  //     .attr("y", 25);

  //   //Create Title
  //   svg.append("text")
  //     .attr("id", "chart_title")
  //     .attr("x", (plotWidth + 50) / 2)
  //     .attr("y", 30)
  //     .attr("class", "title")
  //     .attr("text-anchor", "middle")
  //     .attr("alignment-baseline", "middle")
  //     .text("Cosine Similarity Scores for the Top 5 Words");
  // }

  // Onpage load a shoe:
  // ajax_retrieve("Nike Air Zoom Pegasus 35");

});


$(document).on("click", '.card-example', function () {
  let card = $(this);
  let shoeName = card.find("div > .shoeName").text().trim();
  console.log(shoeName);
  $("#input").val(shoeName);
  input_handler("/custom_search");
});


