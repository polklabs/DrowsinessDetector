<%@ Page Title="" Language="C#" MasterPageFile="~/Site.Master" AutoEventWireup="true" CodeBehind="ChartExample.aspx.cs" Inherits="WebAppEx.ChartExample" %>

<asp:Content ID="Content2" ContentPlaceHolderID="MainContent" runat="server">

<table class="table">
        <thead>
            <tr>
                <th>
                    <font color="#303030" size="5"><span class="glyphicon glyphicon-stats"></span>
                        &nbsp;&nbsp;Statistics</font>
                </th>
            </tr>
        </thead>
    </table>
    
    <div class="row">
    <div id="chart_div" class="col-lg-8" style="height: 300px; padding:0px;"></div>

    <div id="donut_single" class="col-lg-4" style="height: 300px; padding:0px;"></div>
    </div>
    <br /><br />
    <div class="row">
    <div id="chart_div2" class="col-lg-8" style="height: 300px; padding:0px;"></div>

    <div id="Div1" class="col-lg-4" style="height: 300px; padding:0px;">
    
    <div class="table-responsive" style="padding: 10px 50px 0 50px">
    
        <h4 style="font-weight:bold; padding-left:10%">Settings on Hold</h4>
        <div class="span3">
        <table class="table table-striped">
            <thead>
            <tr>
                <th>#</th>
                <th>File</th>
                <th>Time</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <th scope="row">1</th>
                <td>AJ150203001</td>
                <td>5 days</td>
            </tr>
            <tr>
                <th scope="row">2</th>
                <td>AJ150203002</td>
                <td>3 days</td>
            </tr>
            <tr>
                <th scope="row">3</th>
                <td>AJ150203003</td>
                <td>2 days</td>
            </tr>
            <tr>
                <th scope="row">4</th>
                <td>AJ150203003</td>
                <td>2 days</td>
            </tr>
            <tr>
                <th scope="row">5</th>
                <td>AJ150203003</td>
                <td>2 days</td>
            </tr>
            </tbody>
        </table>
      </div>
    </div>
    </div>

    </div>

    <script src="assets/js/jquery.js"></script>
    <script type="text/javascript" src="https://www.google.com/jsapi?autoload={'modules':[{'name':'visualization','version':'1','packages':['corechart']}]}"></script>

    <script>

google.setOnLoadCallback(drawVisualization);

var data;
var options;
var chart;

window.onresize = function() {
    resizeChart();
}

function resizeChart(){
    chart.draw(data, options);
}

function drawVisualization() {
  // Some raw data (not necessarily accurate)
  data = google.visualization.arrayToDataTable([
    ['Week', 'Accuracy', 'Average Accuracy', 'Goal'],
    ['25',  .86,           .82,      .97],
    ['26',  .78,          .82,      .97],
    ['27',  .87,           .83,      .97],
    ['28',  .80,           .87,      .97],
    ['29',  .95,          .90,      .97],
    ['30',  .85,          .91,      .97],
    ['31',  .97,          .96,      .97],
    ['32',  .95,          .965,      .97],
    ['33',  .98,          .925,      .97],
    ['34',  .87,          .91,      .97],
    ['35',  .95,          .9,      .97],
    ['36',  .88,          .93,      .97],
    ['37',  .98,          .94,      .97],
    ['38',  .90,          .93,      .97],
    ['39',  .96,          .91,      .97],
    ['40',  .86,          .915,      .97],
    ['41',  .97,          .92,      .97]
  ]);

  options = {
    title : 'Inventory Accuracy Record',
    titleTextStyle: {color: 'black', fontName: 'Arial', fontSize: '18', fontWidth: 'normal'},
    vAxis: { 
        minValue: .6,
        maxValue: 1,
        title: 
            "Cups", textStyle: {
                color: 'green',           
            }},
    hAxis: {title: "Weeks", textStyle: {
                    color: 'black',           
                }},
    seriesType: "line",
    vAxes: {0: {format:"#%",
                title: "Accuracy", textStyle: {
                    color: 'black'},
                }
                  },
    series: {0: {color: '#F8A600', lineWidth: 5},
             1: {color: 'gray'},
             2: {color: 'green'}
            }
  };

  chart = new google.visualization.ComboChart(document.getElementById('chart_div'));
  chart.draw(data, options);
}


      google.setOnLoadCallback(drawChart);

      function drawChart() {

          var data = google.visualization.arrayToDataTable([
              ['Effort', 'Amount given'],
              ['Discrepencies', 20],
              ['Accuracy', 80]]);

          var options = {
              title : 'General Accuracy',
              titleTextStyle: {color: 'black', fontName: 'Arial', fontSize: '18', fontWidth: 'normal'},
              pieHole: 0.5,
              legend: 'none',
              pieSliceTextStyle: {
            color: 'black', fontSize: '14'
          },
              slices: {
                  0: {
                          color: '#F2F2F2', textStyle: {color: 'transparent'}
                      },
                  1: {
                      color: '#F8A600',
                      lineWidth: 5
                  }
              }
          };

          var chart = new google.visualization.PieChart(document.getElementById('donut_single'));
          chart.draw(data, options);
      }


            google.setOnLoadCallback(drawChart2);
      function drawChart2() {
         var data = google.visualization.arrayToDataTable([
        ['Genre', 'Actual Progress', 'Missing', { role: 'annotation' } ],
        ['General', 60, 40,''],
        ['B&S', 70, 30, ''],
        ['IC', 50, 50, '']
      ]);

      var options = {
        title : 'Progress of Formulas',
        titleTextStyle: {color: 'black', fontName: 'Arial', fontSize: '18', fontWidth: 'normal'},
        colors: ['#F8A600','#F2F2F2'],
        legend: { position: 'rigth', maxLines: 3 },
        bar: { groupWidth: '35%' },
        isStacked: true
      }; 
          
       

        var chart = new google.visualization.BarChart(document.getElementById('chart_div2'));

        chart.draw(data, options);
      }

</script>

</asp:Content>
