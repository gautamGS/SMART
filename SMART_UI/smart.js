$(document).ready(function () {
  product_store = {}
  $.ajax({
    url: "http://127.0.0.1:5000/smart/products",
    cache: false,
    type: "GET",
    timeout: 120000,
    success: function (resp) {
        console.log('response'+ resp)
        brands_products = $.parseJSON(resp)
        populate_brands(brands_products)
        console.log('json_resp ' + brands_products)
    },
    error: function (XMLHttpRequest, textStatus, errorThrown) {
        console.log('textStatus' + textStatus + ' errorThrown' +errorThrown)
    }
  });

  function populate_brands(brands_products){
    product_store = brands_products;
    let dropdown = $('#brand-dropdown');
    dropdown.empty();
    dropdown.append('<option selected="true" disabled>Select Brand</option>');
    dropdown.prop('selectedIndex', 0);
    $.each(brands_products, function (key, entry) {
      console.log('key ' + key + ' entry ' + entry)
      dropdown.append($('<option></option>').attr('value', key).text(key));
    });
  }
  populate_brands();

  $("#brand-dropdown").change(function() {
    var selectedVal = $(this).find(':selected').val();
    let dropdown = $('#prd-dropdown');
    dropdown.empty();
    dropdown.append('<option selected="true" disabled>Select Brand</option>');
    dropdown.prop('selectedIndex', 0);
    prd_items = product_store[selectedVal]
    $.each(prd_items, function (key, val) {
      console.log('Product Item ' + val)
      dropdown.append($('<option></option>').attr('value', val).text(val));
    });
  });

  $('#submit_form').click(function() {
    ais_img = $("input[id='ais_img']").val()
    brand = $("select[id='brand-dropdown']").find(':selected').val();
    item = $("select[id='prd-dropdown']").find(':selected').val();
    if (ais_img == 0 || brand == 0 || item ==0) {
      alert('Please select a value')
    }
    else {
      req_data = {'AIS_IMG': ais_img, 'BRAND':brand, 'ITEM':item};
      $(".gif").show();
      $.ajax({
        url: "http://127.0.0.1:5000/smart/analyze",
        cache: false,
        type: "POST",
        data: req_data,
        timeout: 120000,
        success: function (resp) {
          console.log('response'+ resp)
          json_resp = $.parseJSON(resp)
          console.log('json_resp' + json_resp)
          console.log('prd_cvg_pc'+ JSON.stringify(json_resp['prd_cvg_pc']))
          json_recomm = json_resp['max_aff_bg']
          console.log(JSON.stringify(json_recomm))
          recomm_str = 'Recommended product is ' + JSON.stringify(json_recomm[0][0]) +' with affinity score of ' + JSON.stringify(json_recomm[0][1]) + '%'
          process_resp(json_resp)
          $('.recomm').html(recomm_str);
          $(".gif").hide();
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
          console.log('textStatus' + textStatus + ' errorThrown' +errorThrown)
          $(".gif").show();
        }
      });
    }
  });

  function process_resp(data){ 
    $('#top_panel_x').slideUp();
    $("#icon_id").removeClass("fa-chevron-up");
    $("#icon_id").addClass("fa-chevron-down");
    $('.analysis').show();
    $('.recomm').html('');
     
    chart_data = data['brn_cvg_pc']
    get_chart("brandCoverage", "brandCoverage_table", chart_data, typeC="doughnut", inPercentage=false);
    
    chart_data = data['prd_cvg_pc'];
    get_chart("productcvg", "productcvg_table", chart_data);
    
    chart_data = data['cmp_cvg_pc'];
    get_chart("brand3", "brand3_table", chart_data);
    
    chart_data = data['afn_cvg_bg'];
    chart_generation_bar("affinity", "affinity_table", chart_data, 'horizontalBar');
  }

  function get_chart(canvas_id, canvas_table_id, chart_data, typeC="doughnut", inPercentage=true){
    data = extract_labs_vals(chart_data)
    color_pallete = ['rgb(255, 99, 132)','rgb(54, 162, 235)','rgb(255, 206, 86)','rgb(75, 192, 192)','rgb(153, 102, 255)','rgb(255, 159, 64)'];
    $('#'+canvas_id).html("")
    var ctx = document.getElementById(canvas_id).getContext("2d");
    var myChart = new Chart(ctx, {
        type: typeC,
        data: {
            labels: data[0],
            datasets: [{
                label: '# of Votes',
                data: data[1],
                backgroundColor: color_pallete,
            }]
        },
        options:{
          scales: {
            // yAxes: [{
            //   barPercentage: 0.20,
            //   barThickness:0.15
            // }]
          }

        }
    });
    endChar = '%';
    if (inPercentage == false){
        endChar = '';
    };
    $('#'+canvas_table_id).html("")
    for(i = 0; i < data[0].length; i++){
      content = '<tr><td><p style="width:135px;"><i class="fa fa-square" style="color:' + color_pallete[i] + ';text-overflow: ellipsis;width: 20px;overflow:hidden;"></i>' + data[0][i] + '</p></td><td>'+ data[1][i] +endChar+'</td></tr>';
      $('#'+canvas_table_id).append(content);
    }
  }

  function chart_generation_bar(canvas_id, canvas_table_id, chart_data, typeC="doughnut"){
    color_pallete = ['rgb(255, 99, 132)','rgb(54, 162, 235)','rgb(255, 206, 86)','rgb(75, 192, 192)','rgb(153, 102, 255)','rgb(255, 159, 64)'];
    data = extract_labs_vals(chart_data)
    var ctx = document.getElementById(canvas_id).getContext("2d");
    var myChart = new Chart(ctx, {
        type: typeC,
        data: {
            labels: data[0],
            datasets: [{
                label: '# of Votes',
                data: data[1],
                backgroundColor: color_pallete,
            }]
        },
        options:{
          maintainAspectRatio: false,
          scales: {
            xAxes: [{
              gridLines: {
                display:false
                },
                ticks: {
                  beginAtZero:true, suggestedMin: 0
              }
            }],
            yAxes: [{
              gridLines: {
                display:false
              },
              barPercentage: 0.80,
              barThickness:0.15,
              ticks: {
                  beginAtZero:true, suggestedMin: 0
              }
            }]
          }
          ,elements: {
            rectangle: {
              borderWidth: 2,
            }
                    }
        }
    });

  }

  function mapFunction(value){ return value[0]; }
  function mapFunction_2(value){ return value[1]; }
  function extract_labs_vals(data){
    labels = data.map(mapFunction);
    vals = data.map(mapFunction_2);
    return [labels,vals]
  }
});