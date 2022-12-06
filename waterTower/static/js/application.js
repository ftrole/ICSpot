

$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

    //receive details from server
    socket.on('newnumber', function(msg) {
        number = msg.number;
        value = "80";
        max_volume=1.5*1.2 //tank capacity in m^3

        if (number/max_volume > 0.1 && number/max_volume < 0.2){
            value = "20";
        }else if (number/max_volume > 0.2 && number/max_volume < 0.3){
            value = "30";
        }else if (number/max_volume  > 0.3 && number/max_volume < 0.4){
            value = "40";
        }else if (number/max_volume > 0.4 && number/max_volume < 0.5){
            value = "50";
        }else if (number/max_volume > 0.5 && number/max_volume < 0.6){
            value = "60";
        }else if (number/max_volume > 0.6 && number/max_volume < 0.7){
            value = "70";
        }else if (number/max_volume > 0.7 && number/max_volume < 0.8){
            value = "80";
        }else if (number/max_volume > 0.9 && number/max_volume <= 1){
            value = "90";
        }else if (number/max_volume > 1 && number/max_volume <= 1.09){
            value = "90";
        }else if (number/max_volume >= 1.1){ //Water Tank Limit
            style = `style="background-image: url('/static/imgs/water100.png')"`;
        }else if (number/max_volume < 0.1){
            style = `style="background-image: url('/static/imgs/water0.png')"`;
        }

        if (msg.MV001 == 2){
            MV001 = "off";
        }else if (msg.MV001 == 1){
            MV001 = "on";
        }
        console.log(MV001);

        if (msg.P201 == 2){
            P201 = "off";
        }else if (msg.P201 == 1){
            P201 = "on";
        }
        console.log(P201);

        number = Math.trunc(msg.number * 1000); 
        css = `
            <div id="tank" >
                <img src="static/imgs/water` + value.toString() + `.png" width="100%" >
            </div>
            <div id="pump1" >
                <img src="static/imgs/pump_` + MV001.toString() + `.png" width="100%" >
            </div>
            <div id="pump2" >
                <img src="static/imgs/pump_` + P201.toString() + `.png" width="100%" >
            </div>
            <div id="waterLevel" >   
                <h3> Volume: ` +  number.toString() +  " liters</h3> </div>";
        if (msg.MV001 == 1){
            css+=`<div id="inflow" >   
                <h3> Inflow: ` +  (msg.FIT101*16.67 + ((Math.random() * (0.1 - 1.0) + 0.1))).toFixed(2).toString() +  ` l/min</h3> </div>`;
        }
        if (msg.P201 == 1){
            css+=`<div id="outflow" >   
                <h3> Outflow: ` +  (msg.FIT201*16.67).toFixed(2).toString() +  ` l/min</h3> </div>`;
        }
        if (msg.MV001 == 2){
            css+=`<div id="inflow" >   
                <h3> Inflow: 0 l/min</h3> </div>`;
        }
        if (msg.P201 == 2){
            css+=`<div id="outflow" >   
                <h3> Outflow: 0 l/min</h3> </div>`;
        }


            
        $('#log').html(css);
    });

});
