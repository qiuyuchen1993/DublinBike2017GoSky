window.alert("TEST");
    jQuery.getJSON("http://127.0.0.1:5000/all",null,function(data){
        if('all' in data){
            var stations = data.stations;
            console.log('stations',stations);
            _.forEach(stations,function(station){
                window.alert(station.Address);
                var marker = new google.maps.Marker({
                    position:{
                        lat:station.Position_lat,
                        lng:station.Position_lng
                    },
                    map:map,
                    title:station.Name,
                    station_number:station.Number
                });
                marker.addListener("click",function(){
                    //drawStationCharts(this);
                    drawStationChartsWeekly(this);
                });
            })
        }
    });
