
let $SCRIPT_ROOT = ""

// reload for click on header
let reload_page = () => location.reload();

// returns whether a checkbox is checked or not
let is_checked = (selector) => {
  if ($(selector).prop("checked") == true) {
    return true;
  }
  else {
    return false;
  }
}

// no results found
let render_empty = () => {
  let empty =
    `
  <div class="empty">
    <h3> No results found :( </h3>
  </div>
  `
  $(".shoes-grid").append(empty);
}

// Results HTML
const results_text =
  `
  <div class="header" >
    <h1 style="cursor:initial">
      <img class="logo" src="/static/logo.png">
        Your Solemates
      <img class="logo" src="/static/logo.png">
    </h1>
  </div>
  `

// template generator for shoes found under the EXACT NAME MATCHING SECTION
const similar_shoe_template = (shoe) => {
  return `
    <div class="card" data-toggle="modal" data-target="#shoe-modal">
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
        <p class="card-graph"> ${shoe.term_and_score.splice(0, 5).map(function (d) { return d.toString() }).join(",")} </p>
      </div>
    </div>
  `
};

// template generator for shoes found under the MULTI PART INPUT section
const custom_shoe_template = (shoe) => {
  return `
    <div class="card" data-toggle="modal" data-target="#shoe-modal">
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
};
  

// rendering template for a card
let render_card = (endpoint, shoe) => {
  console.log("Rendering template data");
  // determines which shoe to use by endpoint
  let rendering_card = (endpoint == "/custom_search") ? custom_shoe_template(shoe) : similar_shoe_template(shoe);
  $(".shoes-grid").append(rendering_card);
}

// Conducts the ajax request and renders the results
let ajax_retrieve = (endpoint, search_dictionary) => {
  // retrieve data via GET request
  $.getJSON($SCRIPT_ROOT + endpoint, 
    search_dictionary
    , function (data) {
    console.log("AJAX RETURNED DATA: ")
    console.log(data);
    // if no results display none, else display some card
    (data.length > 0) ? data.map(c => render_card(endpoint, c)) : render_empty();
  });
};

// wrapper, clears the data and fetches results
let clear_and_search = (endpoint, search_dictionary) => {
  $(".shoes-grid").empty();
  $(".results_text").empty();
  $(".results_text").append(results_text);
  // something to append the query shoe?
  ajax_retrieve(endpoint, search_dictionary);
}


// grab and perform input
let input_handler = (inputbox, endpoint, search_dictionary = {}) => {
  console.log("IN INPUT HANDLER");
  let inputted_value = $(inputbox).val();
  
  // GET ALL VALUES HERE
  if (!("search" in search_dictionary)) { 
    search_dictionary["search"] = inputted_value;
  }
  
  if (endpoint == "/custom_search"){
    // find more values and add to dictionary here...
    search_dictionary["trail"] = is_checked("#trail");
    search_dictionary["road"] = is_checked ("#road");
    search_dictionary["neutral"] = is_checked ("#neutral");
    search_dictionary["stability"] = is_checked ("#stability");
    search_dictionary["motion_control"] = is_checked ("#motion_control");
    search_dictionary["gender"] = $(".weight :selected").val();
    search_dictionary["weight"] = $("#weight-range").val();
  }
  console.log(inputbox, endpoint, search_dictionary); 
  clear_and_search(endpoint, search_dictionary);
  scrollToResults();
  return false;
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
  let graph_text = card.find(".card-graph").text();

  console.log(shoeName, similarShoes, corescore, similarity, relevantTerms, terrain, arch_support, men_weight, women_weight);
  console.log(graph_text);

  //create input for creating bar chart from graph text
  let input = [];
  let counter = 0;
  let accum = [];
  graph_text.split(",").forEach(d=>{
    if (counter === 0) {
      accum.push(d);
      counter += 1;
    } else if (counter === 1) {
      accum.push(parseFloat(d));
      input.push(accum);
      accum = [];
      counter = 0;
    }
  });

  //empty element before drawing
  $("#modal_graph").empty();
  
  //create bar chart
  create_bar_chart(input);

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

let scrollToResults = () => {
  console.log("scrolling to results...");
  $("html, body").animate({
     scrollTop: ($(".results_text").offset().top - 50)
    }, 1100);
};


$(document).ready(function () {

  // on click of header, go back to splash
  $(".header h1").bind('click', function () {
    reload_page();
  })

  // Handle for click of enter for similar shoe
  $("#similar-search-text").on('keypress', function (e) {
    if (e.which == 13) {
      console.log("enter was pressed for similar");
      input_handler("#similar-search-text", "/similar_search");
    }
  });

  // should we have a button?
  // $('#go').bind('click', function () {
  //   input_handler("/custom_search");
  // });

  // Handle for click of enter for custom searched shoe
  $("#custom-search-text").on('keypress', function (e) {
    if (e.which == 13) {
      console.log("enter was pressed for custom");
      input_handler("#custom-search-text", "/custom_search");
    }
  });

  // transition between modes from splash
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

  // live render slider values from custom
  $(document).on("input change", "#weight-range", function (){
    $("#current_weight").text(this.value);
  });

});

// for similar, handle on click of any card and load it's data
$(document).on("click", '.card-example', function () {
  let card = $(this);
  let shoeName = card.find("div > .shoeName").text().trim();
  $("#input").val(shoeName);
  input_handler("#input-text", "/similar_search", { search: shoeName });
});


//generate bar chart
function create_bar_chart(chart_data_raw) {
  //chart_data_raw is a 2-d array with [shoe name, score]

  const margin = { top: 30, right: 30, bottom: 30, left: 30 };

  let svg = d3.select("#modal_graph");
  let height = svg.attr("height");
  let width = svg.attr("width");
  let plotHeight = height - margin.top - margin.bottom;
  let plotWidth = width - margin.right - margin.left;

  //get keys 
  let chart_data = chart_data_raw.splice(0,5);

  let chart_data_keys = []
  chart_data.forEach(function(d){
    chart_data_keys.push(d[0]);
  });

  let max_count = d3.max(chart_data, function (d) {
    return d[1];
  });

  let bar_width = (plotWidth - margin.left) / 5;

  let range = [...Array(5).keys()].map(d => d * (plotWidth - margin.left) / 5);

  let xScale = d3.scaleOrdinal()
    .domain(chart_data_keys)
    .range(range);

  let yScale = d3.scaleLinear()
    .domain([0, max_count])
    .range([plotHeight, margin.bottom]);

  let plot = svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  //create bar chart
  plot.selectAll("rect")
    .data(chart_data)
    .enter()
    .append("rect")
    .attr("class", "chart_rect")
    .attr("x", function (d) {
      return xScale(d[0]);
    })
    .attr("y", function (d) {
      return yScale(d[1]) + 20;
    })
    .attr("stroke", function (d) {
      return "black";
    })
    .attr("width", bar_width)
    .attr("height", function (d) {
      return plotHeight - yScale(d[1]);
    })
    .attr("fill", "orange")
    .style("stroke", "white")
    .style("stroke-width", 4);

  //create Y-labels
  plot.selectAll("text")
    .data(chart_data)
    .enter()
    .append("text")
    .attr("class", "chart_text_y")
    .text(function (d) {
      return d[1].toFixed(4);
    })
    .attr("x", function (d) {
      return xScale(d[0]) + bar_width / 2;
    })
    .attr("y", function (d) {
      return yScale(d[1]) + 40;
    })
    .attr("alignment-baseline", "middle")
    .attr('text-anchor', "middle")
    .attr("fill", "white");

  //create x-labels
  let xLabels = svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + (margin.top + plotHeight) + ")");

  xLabels.selectAll("text.xAxis")
    .data(chart_data)
    .enter()
    .append("text")
    .attr("class", "xAxis")
    .text(function (d) {
      return d[0];
    })
    .attr("font-size", "13px")
    .attr("text-anchor", "middle")
    .attr("x", function (d) {
      return xScale(d[0]) + bar_width / 2;
    })
    .attr("y", 30);

  //Create Title
  svg.append("text")
    .attr("id", "chart_title")
    .attr("x", plotWidth / 2 + 20)
    .attr("y", 10)
    .attr("class", "title")
    .attr("text-anchor", "middle")
    .attr("alignment-baseline", "middle")
    .text("Cosine Similarity Scores for the Top 5 Words");

}