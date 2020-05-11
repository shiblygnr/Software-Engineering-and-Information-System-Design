document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {


        document.querySelectorAll('button').forEach(button => {
            button.onclick = () => {
                const selection = button.dataset.course;
                socket.emit('add course', { 'selection': selection });
            };
        });
    });


    socket.on('course registered', data => {
        if (data.situation == "good") {
            console.log(data.section)
            document.querySelectorAll('td').forEach(td => {
                if (td.dataset.id == data.section) {
                    td.innerHTML = data.capacity;
                }

            });
            document.querySelector('#result').innerHTML = "<span class='newco'>Course is added successfully!</span>";
            const p = document.createElement('p');
            content = `${data.course_code}(${data.section_no}) - ${data.course_title}   ${data.days}(${data.time})`;
            p.innerHTML = content;
            //document.querySelector('#report').append(p);
            /*const p = document.createElement('p');
            content = `${data.course_code} `;
            p.innerHTML = content;
            document.querySelectorAll('#report').append(p);*/
        }
        else {
            if (data.error == "size") {
                document.querySelector('#result').innerHTML = "Section is full!";
            }
            else if (data.error == "taken") {
              
              //  document.querySelector('#result').innerHTML = "<span style='font-size:30px' >Course is already taken!</span>";
              document.querySelector('#result').innerHTML = '<span class="glyphicon glyphicon-warning-sign" ></span> Course is already taken!';

            }
            else if (data.error == "conflict") {
                document.querySelector('#result').innerHTML = "Timing conflicts with another registered course!";
            }
            //const h = document.createElement('h2');
            //h.innerHTML = "";
            //h.innerHTML = "Course already taken!";
        }

    });
});