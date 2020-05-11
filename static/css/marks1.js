document.addEventListener('DOMContentLoaded', () => {
    var flag = 0;

    document.querySelectorAll('button').onclick = () => {

        // Initialize new request
        const x = 10
        const request = new XMLHttpRequest();
        //const email = document.querySelector('#email').value;

        request.open('POST', '/instructoruser/add_marks');

        // Callback function for when request completes
        request.onload = () => {
            document.getElementById('result').innerHTML = "";

            if (flag == 0) {
                // Extract JSON data from request
                const data = JSON.parse(request.responseText);

                if(data.success){
                    document.querySelector('#result').innerHTML = "Added";
                }
                else{
                    document.querySelector('#result').innerHTML = "Added";
                }

                // Update the result div
                // if (data.situation) {
                //     /*var style = document.createElement('style');
                //     style.innerHTML = `
                //     table {
                //         border: 2px solid blue;
                //         border-collapse: collapse;
                //         background-color: lightgrey;
                //         width: 30%;
                //         height: 40%;
                //         text-align: center;
                //     }`;
                //     document.head.appendChild(style);*/
                //     //document.querySelector("#report1").innerHTML = "Hi!"
                //     //document.getElementById('#t1').innerHTML = "";
                //     var details = data.details;
                //     //let table = document.querySelector("#t1");
                //     const t = document.createElement('table');
                //     const tr1 = document.createElement('tr');
                //     const th1 = document.createElement('th');
                //     th1.innerHTML = "Student ID";
                //     const th2 = document.createElement('th');
                //     th2.innerHTML = "Name";
                //     const th3 = document.createElement('th');
                //     th3.innerHTML = "Attendance Status";

                //     tr1.append(th1, th2, th3);
                //     t.append(tr1);
                //     // document.querySelector('#status').append(t);
                //     for (var i = 0; i < details.length; i++) {
                //         const tr1 = document.createElement('tr');
                //         const td1 = document.createElement('td');
                //         td1.innerHTML = details[i].student_id;
                //         const td2 = document.createElement('td');
                //         td2.innerHTML = details[i].student_name;
                //         const td3 = document.createElement('td');
                //         td3.innerHTML = details[i].attendance;
                //         tr1.append(td1, td2, td3);
                //         t.append(tr1);
                //     }
                //     document.querySelector('#status').append(t);
                //     /*let data1 = Object.keys(details[0]);

                //     let thead = table.createTHead();
                //     let row = thead.insertRow();
                //     for (let key of data1) {
                //         let th = document.createElement("th");
                //         let text = document.createTextNode(key);
                //         th.appendChild(text);
                //         row.appendChild(th);
                //     }

                //     for (let element of details) {
                //         let row = table.insertRow();
                //         for (key in element) {
                //             let cell = row.insertCell();
                //             let text = document.createTextNode(element[key]);
                //             cell.appendChild(text);
                //         }
                //     }*/
                //     //generateTable(table, details);
                //     /*for (var i = 0; i < details.length; i++) {
                //         const contents = `${details[i].course_code}(${details[i].section_no}) - ${details[i].course_title}  `;
                //         const p = document.createElement('p');
                //         p.innerHTML = contents;
                //         //alert(`${data.course_code}`);
                //         document.querySelector('#report1').append(p);
                //     }*/

                // }
                // else {
                //     document.querySelector('#status').innerHTML = "No record found!";
                // }
                // //flag = 1;
            }
        }

        // Add data to send with request
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
            var data = new FormData();
            data.append('section', section);
            data.append('sid', sid);
            data.append('mid1', mid1);
            data.append('mid2', mid2);
            data.append('final', final);
            data.append('quiz', quiz);
            data.append('project', project);
            data.append('section', attendance);
            request.send(data);
        }
        return false;
    };

});
