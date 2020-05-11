document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {


        document.querySelectorAll('input[type=radio]').forEach(input => {
            input.onclick = () => {
                console.log("hello");
                var section = document.querySelector('#hide1').innerHTML;
                console.log(section);
                var date  = document.querySelector('#date').value;
                console.log(date)
                var sid = input.dataset.id;
                var ele = document.getElementsByName(sid);
                
                for(i = 0; i < ele.length; i++) { 
                    if(ele[i].checked) {
                        var attendance = ele[i].value;
                    }
                }
                
                if(date == ""){
                    document.querySelector('#result').innerHTML = "Choose date!";
                }
                else{
                    document.querySelectorAll('td').forEach(td => {
                        if (td.dataset.attendance == sid) {
                            td.innerHTML = attendance;
                        }
        
                    });
                    socket.emit('record attendance', { 'section': section, "sid":sid, "date":date, "attendance":attendance });

                }
                
            };
        });
    });

    socket.on('attendance recorded', data => {
        document.querySelector('#result').innerHTML = "";
        document.querySelector('#result1').innerHTML = "";
        if (data.situation == "added") {
            document.querySelector('#result').innerHTML = `Attendance recorded for ${data.name} !`;
            
        }
        else {
            document.querySelector('#result1').innerHTML = `Attendance updated for ${data.name}!`;
        }

    });

});