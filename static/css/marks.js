document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {


        document.querySelectorAll('button').forEach(button => {
            button.onclick = () => {
                const section = document.querySelector('#hide1').innerHTML;
                console.log(section);
                const mid1 = document.querySelector('#mid1').value;
                console.log(mid1);
                const mid2 = document.querySelector('#mid2').value;
                console.log(mid2);
                const final = document.querySelector('#final').value;
                console.log(final);
                const quiz = document.querySelector('#quiz').value;
                console.log(quiz);
                const project = document.querySelector('#project').value;
                console.log(project);
                const attendance = document.querySelector('#attendance').innerHTML;
                console.log(attendance);
                const sid = document.querySelector('#sid').innerHTML;
                console.log(sid);
                if (mid1 == "" || mid2 == "" || final == "" || project == "" || quiz == "" ){
                    document.querySelector("#result").innerHTML = "Fields can not be empty!";
                }
                else if( mid1 > 25 || mid1 < 0 || mid2 >25 || mid2 <0 || final>25 || final <0){
                    document.querySelector("#result").innerHTML = "Some of your inputs are out of range, check again!";
                }
                else if(project > 10 || project < 0 || quiz > 10 || quiz < 0){
                    document.querySelector("#result").innerHTML = "Some of your inputs are out of range, check again!";
                }
                else{
                socket.emit('add mark', { 'section': section, 'sid':sid, 'mid1':mid1, 'mid2':mid2, 'final':final, 'quiz':quiz, 'attendance':attendance, 'project':project});
                }
               
            };
        });
    });
    socket.on('mark added', data => {
        if(data.success){
            document.querySelector("#result").innerHTML = "Marks added!";
        }
        else{
            document.querySelector("#result").innerHTML = "Marks not added! Try update marks!!";
        }
        // if (data.situation == "good") {
        //     console.log(data.section)
        //     document.querySelectorAll('td').forEach(td => {
        //         if (td.dataset.id == data.section) {
        //             td.innerHTML = data.capacity;
        //         }

        //     });
        //     document.querySelector('#result').innerHTML = "<span class='newco'>Course is added successfully!</span>";
        //     const p = document.createElement('p');
        //     content = `${data.course_code}(${data.section_no}) - ${data.course_title}   ${data.days}(${data.time})`;
        //     p.innerHTML = content;
        //     //document.querySelector('#report').append(p);
        //     /*const p = document.createElement('p');
        //     content = `${data.course_code} `;
        //     p.innerHTML = content;
        //     document.querySelectorAll('#report').append(p);*/
        // }
        // else {
        //     if (data.error == "size") {
        //         document.querySelector('#result').innerHTML = "Section is full!";
        //     }
        //     else if (data.error == "taken") {
              
        //       //  document.querySelector('#result').innerHTML = "<span style='font-size:30px' >Course is already taken!</span>";
        //       document.querySelector('#result').innerHTML = '<span class="glyphicon glyphicon-warning-sign" ></span> Course is already taken!';

        //     }
        //     else if (data.error == "conflict") {
        //         document.querySelector('#result').innerHTML = "Timing conflicts with another registered course!";
        //     }
        //     //const h = document.createElement('h2');
        //     //h.innerHTML = "";
        //     //h.innerHTML = "Course already taken!";
        // }

    });



});