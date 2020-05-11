document.addEventListener('DOMContentLoaded', () => {
    var flag = 0;

    document.querySelector('#registered').onclick = () => {

        // Initialize new request
        const x = 10
        const request = new XMLHttpRequest();
        //const email = document.querySelector('#email').value;

        request.open('POST', '/studentuser/show_registered_courses');

        // Callback function for when request completes
        request.onload = () => {
            document.getElementById('t1').innerHTML = "";

            if (flag == 0) {
                // Extract JSON data from request
                const data = JSON.parse(request.responseText);

                // Update the result div
                if (data.situation) {
                    /*var style = document.createElement('style');
                    style.innerHTML = `
                    table {
                        border: 2px solid blue;
                        border-collapse: collapse;
                        background-color: lightgrey;
                        width: 30%;
                        height: 40%;
                        text-align: center;
                    }`;
                    document.head.appendChild(style);*/
                    //document.querySelector("#report1").innerHTML = "Hi!"
                    //document.getElementById('#t1').innerHTML = "";
                    var details = data.details;
                    //let table = document.querySelector("#t1");
                    const t = document.createElement('table');
                    const tr1 = document.createElement('tr');
                    const th1 = document.createElement('th');
                    th1.innerHTML = "Course Code";
                    const th2 = document.createElement('th');
                    th2.innerHTML = "Course Title";
                    const th3 = document.createElement('th');
                    th3.innerHTML = "Credit";
                    const th4 = document.createElement('th');
                    th4.innerHTML = "Section";
                    const th5 = document.createElement('th');
                    th5.innerHTML = "Days";
                    const th6 = document.createElement('th');
                    th6.innerHTML = "Time";
                    tr1.append(th1, th2, th3, th4, th5, th6);
                    t.append(tr1);
                    document.querySelector('#t1').append(t);
                    for (var i = 0; i < details.length; i++) {
                        const tr1 = document.createElement('tr');
                        const td1 = document.createElement('td');
                        td1.innerHTML = details[i].course_code;
                        const td2 = document.createElement('td');
                        td2.innerHTML = details[i].course_title;
                        const td3 = document.createElement('td');
                        td3.innerHTML = details[i].credit;
                        const td4 = document.createElement('td');
                        td4.innerHTML = details[i].section_no;
                        const td5 = document.createElement('td');
                        td5.innerHTML = details[i].days;
                        const td6 = document.createElement('td');
                        td6.innerHTML = details[i].time;
                        tr1.append(td1, td2, td3, td4, td5, td6);
                        t.append(tr1);
                    }
                    document.querySelector('#t1').append(t);
                    /*let data1 = Object.keys(details[0]);

                    let thead = table.createTHead();
                    let row = thead.insertRow();
                    for (let key of data1) {
                        let th = document.createElement("th");
                        let text = document.createTextNode(key);
                        th.appendChild(text);
                        row.appendChild(th);
                    }

                    for (let element of details) {
                        let row = table.insertRow();
                        for (key in element) {
                            let cell = row.insertCell();
                            let text = document.createTextNode(element[key]);
                            cell.appendChild(text);
                        }
                    }*/
                    //generateTable(table, details);
                    /*for (var i = 0; i < details.length; i++) {
                        const contents = `${details[i].course_code}(${details[i].section_no}) - ${details[i].course_title}  `;
                        const p = document.createElement('p');
                        p.innerHTML = contents;
                        //alert(`${data.course_code}`);
                        document.querySelector('#report1').append(p);
                    }*/

                }
                else {
                    document.querySelector('#t1').innerHTML = "No course found!";
                }
                //flag = 1;
            }
        }

        // Add data to send with request
        const data = new FormData();
        //data.append('email', email);

        // Send request
        request.send(data);
        return false;
    };

});
