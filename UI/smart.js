$(document).ready(function () {

  $('#btn1').click(function (e) {
    // Your event handler
    console.log("change")
    console.log(e.target.selectedIndex)
    x = $("select[id='items'] option:selected").index()
    y = $("select[id='images'] option:selected").index()

    if (x == 0 || y == 0) {
      alert('Please select a value')
    }
    else {
      $.ajax({
        url: "http://localhost:5000/stg/items/" + x + "/" + y,
        cache: false,
        type: "GET",

        success: function (html) {
          image_source_1 = html.item.address_1
          image_source_2 = html.item.address_2
          image_source_3 = html.item.bounding_box_img
          //$("#div1").html('<img src="' + image_source_1 + '" alt="Image 1">')
          //$("#div2").html('<img src="' + image_source_2 + '" alt="Image 2">')
          $("#bounding_box_img").html('<b>Image with Detections: </b><br><img src="' + image_source_3 + '" alt="Bounding Box Image" >')
          //$("#current_product_affinity").html('<div style="vertical-align:top" > <h3> ' + html.item.current_product_affinity + '% </h3> </div>')
          //$("#heading1").html('<h3> Product Affinity Current:')

          //console.log(html.item.pie_chart_1)


          google.charts.load('current', { 'packages': ['corechart'] });
          google.charts.setOnLoadCallback(drawChart);
          google.charts.setOnLoadCallback(drawChart_1);
          google.charts.setOnLoadCallback(drawChart_2);

          var options = {legend: {position: 'right', alignment:'center'}, chartArea:{left:20, top:0,width:'80%',height:'80%'}};


          // Draw the chart and set the chart values
          function drawChart() {
            var data = google.visualization.arrayToDataTable(html.item.pie_chart_1);
            //var options = { title: 'Item Vs Competitors', legend: {position: 'bottom'}};
            var chart = new google.visualization.PieChart(document.getElementById('piechart_1'));
            chart.draw(data, options);
          }

          function drawChart_1() {
            var data = google.visualization.arrayToDataTable(html.item.pie_chart_2);
            var chart = new google.visualization.PieChart(document.getElementById('piechart_2'));
            chart.draw(data, options);
          }

          function drawChart_2() {
            var data = google.visualization.arrayToDataTable(html.item.pie_chart_3);
            //var options = { title: 'Brand Coverage', legend: {position: 'bottom'}};
            var chart = new google.visualization.PieChart(document.getElementById('piechart_3'));
            chart.draw(data, options);
          }




        },
        error: function (error) {
          console.log(error)
        }
      });
    }

  });

  // And now fire change event when the DOM is ready
  $('#countrylist').trigger('change');
});