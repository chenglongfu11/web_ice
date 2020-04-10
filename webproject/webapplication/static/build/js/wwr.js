$("#btnSubmit").click(function(){
       var value1 =$("#simu_time").val();
       var value2 = $("#largest_width").val();
       // var csrf=$('[name="csrfmiddlewaretoken"]').val();
       // var csrftoken = Cookies.get('csrftoken');
       var formData = new FormData();
       formData.append("simu_time",value1);
      formData.append("largest_width",value2);
      // formData.append("csrfmiddlewaretoken", csrftoken);

        document.getElementById('spinner').style.visibility = "visible";    //loading spinner
// post form data and get response from backend
       $.ajax({
           url:'',
           type:'post',
           data: formData,
           processData:false,
           contentType:false,
           success:function (res) {
                       console.log('get res',res);
                       var jList = res['power_values'];
                       var legendList = res['power_legends'];
                       console.log('On success response');
                       $('#res_power').css("height","350px");
                       $('#graph_name').html('Peak Power graph');       //title of graph
                       echart_res(jList,legendList);       //graph
                       document.getElementById('spinner').style.visibility = "hidden";    //remove loading spinner
           },
           error: function (jqXHR, textStatus, err) {
                        console.log(arguments);
                    },
       });
    });

      //Power bar graph
function echart_res(jList,legendList){
        var echartBar = echarts.init(document.getElementById('res_power'));
// parse json data to readable arrays
        jList = JSON.parse(jList);
        legendList = JSON.parse(legendList);
        var seriesList = new Array();
// Form series arrays
        for ( var i=0; i<jList.length;i++) {
          var obj1 = {
            name: legendList[i], type: 'bar', data: jList[i],
            marPoint: {
              data: [{type: 'max', nmae: 'max'}, {type: 'average', name: 'average'},
                {type: 'min', name: 'min'}, {type: 'sum', name: 'sum'}]
            }
          };
          seriesList.push(obj1);
        }

        echartBar.setOption({
            title: {text: '',},
            tooltip: {trigger: 'axis'},
            legend: {data: legendList},            //legendList from backend
            toolbox: {show: false},
            calculable: true,
            xAxis: [{
                type: 'category',
                data: ['Electric Cooling','Equipment, Tenant','Lighting Facility','Fuel Heating','Domestic Hot Water','HVAC',
                  'Sum of All']
            }],
            yAxis: [{
                type: 'value'
            }],
            series: seriesList,     //series list from backend
        });

    }
