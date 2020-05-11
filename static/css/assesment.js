document.addEventListener('DOMContentLoaded', () => {
    var flag = 0;
    var f = 0;

    document.querySelector('#attendancecheck').onclick = () => {

        // Initialize new request
        const x = 10
        const request = new XMLHttpRequest();

        //const email = document.querySelector('#email').value;

        request.open('POST', '/instructoruser/attendance_check');

        // Callback function for when request completes
        request.onload = () => {

            if (flag % 2 == 0) {

                // document.getElementById('attendanceinfo').innerHTML = "";

                // Extract JSON data from request
                const data = JSON.parse(request.responseText);
                const content = `Attentivity: ${data.attentivity}%`;
                const p = document.createElement('p');
                p.innerHTML = content;
                document.querySelector('#attendanceinfo').append(p);
                flag++;
            }
            else {
                document.getElementById('attendanceinfo').innerHTML = "";
                flag++;
            }


        }

        // Add data to send with request
        var section = document.querySelector('#section').innerHTML;
        console.log(section);
        var sid = document.querySelector('#sid').innerHTML;


        const data = new FormData();
        // const data_to_send = {'section':section, 'date':date};
        data.append('section', section);
        data.append('sid', sid);

        request.send(data);

        return false;
    };
    var is_add = 0;
    document.querySelector('#addmarks').onclick = () => {
        const request = new XMLHttpRequest();

        //const email = document.querySelector('#email').value;

        request.open('POST', '/instructoruser/is_added');

        request.onload = () => {

            var is_added = JSON.parse(request.responseText);
            if (is_added.success) {
                if (f % 2 == 0) {
                    f++;
                    var input1 = document.createElement('input');
                    input1.type = "number";
                    input1.placeholder = "out of 25";
                    input1.id = "mid1";
                    var label1 = document.createElement('label');
                    label1.for = "mid1";
                    label1.innerHTML = "Mid1:  ";
                    document.querySelector('#addmarksinfo').append(label1);
                    document.querySelector('#addmarksinfo').append(input1);
                    document.querySelector('#addmarksinfo').append(document.createElement('br'));
                    // document.querySelector('#addmarksinfo').append(document.createElement('br'));
                    var input2 = document.createElement('input');
                    input2.type = "number";
                    input2.placeholder = "out of 25";
                    input2.id = "mid2";
                    var label2 = document.createElement('label');
                    label2.for = "mid2";
                    label2.innerHTML = "Mid2: ";
                    document.querySelector('#addmarksinfo').append(label2);
                    document.querySelector('#addmarksinfo').append(input2);
                    document.querySelector('#addmarksinfo').append(document.createElement('br'));
                    var input3 = document.createElement('input');
                    input3.type = "number";
                    input3.placeholder = "out of 25";
                    input3.id = "final";
                    var label3 = document.createElement('label');
                    label3.for = "final";
                    label3.innerHTML = "Final:  ";
                    document.querySelector('#addmarksinfo').append(label3);
                    document.querySelector('#addmarksinfo').append(input3);
                    document.querySelector('#addmarksinfo').append(document.createElement('br'));
                    var input4 = document.createElement('input');
                    input4.type = "number";
                    input4.placeholder = "out of 10";
                    input4.id = "quiz";
                    var label4 = document.createElement('label');
                    label4.for = "quiz";
                    label4.innerHTML = "Quiz:  ";
                    document.querySelector('#addmarksinfo').append(label4);
                    document.querySelector('#addmarksinfo').append(input4);
                    document.querySelector('#addmarksinfo').append(document.createElement('br'));
                    var input5 = document.createElement('input');
                    input5.type = "number";
                    input5.placeholder = "out of 10";
                    input5.id = "project";
                    var label5 = document.createElement('label');
                    label5.for = "project";
                    label5.innerHTML = "Project:  ";
                    document.querySelector('#addmarksinfo').append(label5);
                    document.querySelector('#addmarksinfo').append(input5);
                    var attendance = document.createElement('div');
                    attendance.innerHTML = document.querySelector('#attentivity').innerHTML;
                    var p = document.createElement('p');
                    p.innerHTML = "Attendance: " + attendance.innerHTML;
                    // p.append(attendance);
                    document.querySelector('#addmarksinfo').append(p);
                    var btn = document.createElement('button');
                    btn.innerHTML = "Add";
                    btn.id = "add";
                    // document.querySelector('#addmarksinfo').append(document.createElement('br'));
                    document.querySelector('#addmarksinfo').append(btn);
                    // var msg = document.createElement('div');
                    // msg.id = "msg";
                    // f = 1;

                    document.querySelector('#add').onclick = () => {

                        const request = new XMLHttpRequest();

                        //const email = document.querySelector('#email').value;

                        request.open('POST', '/instructoruser/add_marks');

                        // Callback function for when request completes
                        request.onload = () => {
                            const data = JSON.parse(request.responseText);

                            if (data.success == "good") {

                                document.querySelector('#msg').innerHTML = "Marks added!";
                            }
                            else if (data.success == "bad") {
                                document.querySelector('#msg').innerHTML = "Marks already added! Try update marks!!";
                            }
                            else {
                                document.querySelector('#msg').innerHTML = "Fields can not be empty!";
                            }


                        }

                        const section = document.querySelector('#section').innerHTML;
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
                        const attendance = document.querySelector('#attentivity').innerHTML;
                        console.log(attendance);
                        const sid = document.querySelector('#sid').innerHTML;
                        console.log(sid);
                        const data = new FormData();
                        data.append('section', section);
                        data.append('sid', sid);
                        data.append('mid1', mid1);
                        data.append('mid2', mid2);
                        data.append('final', final);
                        data.append('quiz', quiz);
                        data.append('project', project);
                        data.append('attendance', attendance);
                        request.send(data);
                        return false;
                    };

                }
                else {
                    document.getElementById('addmarksinfo').innerHTML = "";
                    document.getElementById('msg').innerHTML = "";
                    f++;

                }

            }
            else {
                if (is_add % 2 == 0) {
                    document.getElementById('addmarksinfo').innerHTML = "";
                    document.querySelector('#msg').innerHTML = "Marks already added! Try update marks!!";
                    is_add++;
                }
                else {
                    document.getElementById('addmarksinfo').innerHTML = "";
                    document.querySelector('#msg').innerHTML = "";
                    is_add++;
                }

            }
        };

        const sid2 = document.querySelector('#sid').innerHTML;
        const sec = document.querySelector('#section').innerHTML;
        console.log(sid2);
        const data3 = new FormData();
        data3.append('sid', sid2);
        data3.append('section', sec);
        request.send(data3);
        return false;
    };

    var f1 = 0;
    document.querySelector('#resultcheck').onclick = () => {
        if (f1 % 2 == 0) {
            const credit = document.createElement('p');
            credit.innerHTML = "Credits completed: " + document.getElementById('credit').innerHTML;
            const cgpa = document.createElement('p');
            cgpa.innerHTML = "CGPA: " + document.getElementById('cgpa').innerHTML;
            document.querySelector('#resultinfo').append(credit);
            document.querySelector('#resultinfo').append(cgpa);
            f1++;

        }
        else {
            document.querySelector('#resultinfo').innerHTML = "";
            f1++;
        }


    };

    var f2 = 0;
    document.querySelector("#gradecheck").onclick = () => {

        if (f2 % 2 == 0) {
            f2++;
            const request = new XMLHttpRequest();

            //const email = document.querySelector('#email').value;

            request.open('POST', '/instructoruser/get_grades');

            request.onload = () => {
                document.querySelector('#gradeinfo').innerHTML = "";
                grade_details = JSON.parse(request.responseText);
                if (grade_details.success) {
                    details = grade_details.details;
                    const t = document.createElement('table');
                    const tr1 = document.createElement('tr');
                    const th1 = document.createElement('th');
                    th1.innerHTML = "Course Code";
                    const th2 = document.createElement('th');
                    th2.innerHTML = "Grade";
                    tr1.append(th1, th2);
                    t.append(tr1);
                    console.log(details.length);
                    for (var i = 0; i < details.length; i++) {
                        const tr1 = document.createElement('tr');
                        const td1 = document.createElement('td');
                        td1.innerHTML = details[i].course_code;
                        const td2 = document.createElement('td');
                        td2.innerHTML = details[i].grade;
                        tr1.append(td1, td2);
                        t.append(tr1);

                    }
                    document.querySelector('#gradeinfo').append(t);

                }
                else {
                    document.querySelector('#gradeinfo').innerHTML = "No course found!";
                }

            };

            const sid1 = document.querySelector('#sid').innerHTML;
            console.log(sid);
            const data2 = new FormData();
            data2.append('sid', sid1);
            request.send(data2);
            return false;

        }
        else {
            document.querySelector('#gradeinfo').innerHTML = "";
            f2++;
        }

    };
    var x = 0, y = 0;
    document.querySelector('#updatemarks').onclick = () => {
        const request = new XMLHttpRequest();

        //const email = document.querySelector('#email').value;

        request.open('POST', '/instructoruser/is_added');

        request.onload = () => {
            document.querySelector('#updatemarksinfo').innerHTML = "";
            const is_added = JSON.parse(request.responseText);
            if (!is_added.success) {
                // const request = new XMLHttpRequest();
                // request.open('POST', '/instructoruser/get_marks');
                if (x % 2 == 0) {
                    x++;
                    const unordered = document.createElement('ul');
                    const m1 = document.createElement('div');
                    m1.id = "infomid1";
                    const mid1msg = document.createElement('div');
                    mid1msg.id = "mid1msg";
                    const l1 = document.createElement('li');
                    const a1 = document.createElement('a');
                    a1.innerHTML = "Mid1";
                    a1.href = "#";
                    a1.id = "updatemid1";
                    l1.appendChild(a1);
                    unordered.append(l1);
                    unordered.append(m1);
                    unordered.append(mid1msg);
                    const l2 = document.createElement('li');
                    const a2 = document.createElement('a');
                    a2.innerHTML = "Mid2";
                    a2.href = "#";
                    a2.id = "updatemid2";
                    l2.appendChild(a2);
                    const m2 = document.createElement('div');
                    m2.id = "infomid2";
                    const mid2msg = document.createElement('div');
                    mid2msg.id = "mid2msg";
                    unordered.append(l2);
                    unordered.append(m2);
                    unordered.append(mid2msg);
                    const l3 = document.createElement('li');
                    const a3 = document.createElement('a');
                    a3.innerHTML = "Final";
                    a3.href = "#";
                    a3.id = "updatefinal";
                    l3.appendChild(a3);
                    const finalinfo = document.createElement('div');
                    finalinfo.id = "infofinal";
                    const finalmsg = document.createElement('div');
                    finalmsg.id = "finalmsg";
                    
                    unordered.append(l3);
                    unordered.append(finalinfo);
                    unordered.append(finalmsg);
                    const l4 = document.createElement('li');
                    const a4 = document.createElement('a');
                    a4.innerHTML = "Quiz";
                    a4.href = "#";
                    a4.id = "updatequiz";
                    l4.appendChild(a4);
                    const quizinfo = document.createElement('div');
                    quizinfo.id = "infoquiz";
                    const quizmsg = document.createElement('div');
                    quizmsg.id = "quizmsg";
                    unordered.append(l4);
                    unordered.append(quizinfo);
                    unordered.append(quizmsg);
                    const l5 = document.createElement('li');
                    const a5 = document.createElement('a');
                    a5.innerHTML = "Project";
                    a5.href = "#";
                    a5.id = "updateproject";
                    l5.appendChild(a5);
                    const projectinfo = document.createElement('div');
                    projectinfo.id = "infoproject";
                    const projectmsg = document.createElement('div');
                    projectmsg.id = "projectmsg";
                    unordered.append(l5);
                    unordered.append(projectinfo);
                    unordered.append(projectmsg);

                    document.querySelector('#updatemarksinfo').append(unordered);
                    var flag = 0;
                    document.querySelector('#updatemid1').onclick = () => {
                        const request = new XMLHttpRequest();
                        request.open('POST', '/instructoruser/get_mid1_marks');

                        request.onload = () => {
                            const mark = JSON.parse(request.responseText);
                            if (flag % 2 == 0) {
                                const t = document.createElement('table');
                                const tr1 = document.createElement('tr');
                                const th1 = document.createElement('th');
                                const th2 = document.createElement('th');
                                const th3 = document.createElement('th');
                                th1.innerHTML = "Given mark";
                                th2.innerHTML = "Updated mark";
                                tr1.append(th1, th2, th3);
                                const tr2 = document.createElement('tr');
                                const td1 = document.createElement('td');
                                td1.innerHTML = mark.mid1;
                                const td2 = document.createElement('td');
                                const input = document.createElement('input');
                                input.type = "number";
                                input.id = "updatedmid1";
                                input.placeholder = "out of 25";
                                td2.appendChild(input);
                                const td3 = document.createElement('td');
                                const btn = document.createElement('button');
                                btn.innerHTML = "Update";
                                btn.id = "updatemid1mark";
                                td3.appendChild(btn)

                                // td2.innerHTML = "Updated mark";
                                tr2.append(td1, td2, td3);
                                t.append(tr1, tr2);
                                document.querySelector('#infomid1').append(t);
                                flag++;
                                document.querySelector('#updatemid1mark').onclick = () => {

                                    const request = new XMLHttpRequest();

                                    //const email = document.querySelector('#email').value;

                                    request.open('POST', '/instructoruser/update_mid1');

                                    // Callback function for when request completes
                                    request.onload = () => {
                                        const data = JSON.parse(request.responseText);

                                        if (data.success) {

                                            document.querySelector('#mid1msg').innerHTML = "Marks updated!";
                                        }
                                        else {
                                            document.querySelector('#mid1msg').innerHTML = "Marks not updated!";
                                        }


                                    }

                                    const section = document.querySelector('#section').innerHTML;
                                    console.log(section);
                                    const mid1 = document.querySelector('#updatedmid1').value;
                                    console.log(mid1);
                                    const sid = document.querySelector('#sid').innerHTML;
                                    console.log(sid);
                                    const data = new FormData();
                                    data.append('section', section);
                                    data.append('sid', sid);
                                    data.append('mid1', mid1);
                                    request.send(data);
                                    return false;
                                };


                            }
                            else {
                                document.querySelector('#infomid1').innerHTML = "";
                                document.querySelector('#mid1msg').innerHTML = "";
                                flag++;
                            }

                        }
                        const sid2 = document.querySelector('#sid').innerHTML;
                        const sec = document.querySelector('#section').innerHTML;
                        console.log(sid2);
                        const data3 = new FormData();
                        data3.append('sid', sid2);
                        data3.append('section', sec);
                        request.send(data3);
                        return false;

                    };
                    var flag1 = 0;
                    document.querySelector('#updatemid2').onclick = () => {
                        const request = new XMLHttpRequest();
                        request.open('POST', '/instructoruser/get_mid2_marks');

                        request.onload = () => {
                            const mark = JSON.parse(request.responseText);
                            if (flag1 % 2 == 0) {
                                const t = document.createElement('table');
                                const tr1 = document.createElement('tr');
                                const th1 = document.createElement('th');
                                const th2 = document.createElement('th');
                                const th3 = document.createElement('th');
                                th1.innerHTML = "Given mark";
                                th2.innerHTML = "Updated mark";
                                tr1.append(th1, th2, th3);
                                const tr2 = document.createElement('tr');
                                const td1 = document.createElement('td');
                                td1.innerHTML = mark.mid2;
                                const td2 = document.createElement('td');
                                const input = document.createElement('input');
                                input.type = "number";
                                input.id = "updatedmid2";
                                input.placeholder = "out of 25";
                                td2.appendChild(input);
                                const td3 = document.createElement('td');
                                const btn = document.createElement('button');
                                btn.innerHTML = "Update";
                                btn.id = "updatemid2mark";
                                td3.appendChild(btn)

                                // td2.innerHTML = "Updated mark";
                                tr2.append(td1, td2, td3);
                                t.append(tr1, tr2);
                                document.querySelector('#infomid2').append(t);
                                flag1++;
                                document.querySelector('#updatemid2mark').onclick = () => {

                                    const request = new XMLHttpRequest();

                                    //const email = document.querySelector('#email').value;

                                    request.open('POST', '/instructoruser/update_mid2');

                                    // Callback function for when request completes
                                    request.onload = () => {
                                        const data = JSON.parse(request.responseText);

                                        if (data.success) {

                                            document.querySelector('#mid2msg').innerHTML = "Marks updated!";
                                        }
                                        else {
                                            document.querySelector('#mid2msg').innerHTML = "Marks not updated!";
                                        }


                                    }

                                    const section = document.querySelector('#section').innerHTML;
                                    console.log(section);
                                    const mid2 = document.querySelector('#updatedmid2').value;
                                    console.log(mid2);
                                    const sid = document.querySelector('#sid').innerHTML;
                                    console.log(sid);
                                    const data = new FormData();
                                    data.append('section', section);
                                    data.append('sid', sid);
                                    data.append('mid2', mid2);
                                    request.send(data);
                                    return false;
                                };


                            }
                            else {
                                document.querySelector('#infomid2').innerHTML = "";
                                document.querySelector('#mid2msg').innerHTML = "";
                                flag1++;
                            }

                        }
                        const sid2 = document.querySelector('#sid').innerHTML;
                        const sec = document.querySelector('#section').innerHTML;
                        console.log(sid2);
                        const data3 = new FormData();
                        data3.append('sid', sid2);
                        data3.append('section', sec);
                        request.send(data3);
                        return false;

                    };

                    var flag2 = 0;
                    document.querySelector('#updatefinal').onclick = () => {
                        const request = new XMLHttpRequest();
                        request.open('POST', '/instructoruser/get_final_marks');

                        request.onload = () => {
                            const mark = JSON.parse(request.responseText);
                            if (flag2 % 2 == 0) {
                                const t = document.createElement('table');
                                const tr1 = document.createElement('tr');
                                const th1 = document.createElement('th');
                                const th2 = document.createElement('th');
                                const th3 = document.createElement('th');
                                th1.innerHTML = "Given mark";
                                th2.innerHTML = "Updated mark";
                                tr1.append(th1, th2, th3);
                                const tr2 = document.createElement('tr');
                                const td1 = document.createElement('td');
                                td1.innerHTML = mark.final;
                                const td2 = document.createElement('td');
                                const input = document.createElement('input');
                                input.type = "number";
                                input.id = "updatedfinal";
                                input.placeholder = "out of 25";
                                td2.appendChild(input);
                                const td3 = document.createElement('td');
                                const btn = document.createElement('button');
                                btn.innerHTML = "Update";
                                btn.id = "updatefinalmark";
                                td3.appendChild(btn)

                                // td2.innerHTML = "Updated mark";
                                tr2.append(td1, td2, td3);
                                t.append(tr1, tr2);
                                document.querySelector('#infofinal').append(t);
                                flag2++;
                                document.querySelector('#updatefinalmark').onclick = () => {

                                    const request = new XMLHttpRequest();

                                    //const email = document.querySelector('#email').value;

                                    request.open('POST', '/instructoruser/update_final');

                                    // Callback function for when request completes
                                    request.onload = () => {
                                        const data = JSON.parse(request.responseText);

                                        if (data.success) {

                                            document.querySelector('#finalmsg').innerHTML = "Marks updated!";
                                        }
                                        else {
                                            document.querySelector('#finalmsg').innerHTML = "Marks not updated!";
                                        }


                                    }

                                    const section = document.querySelector('#section').innerHTML;
                                    console.log(section);
                                    const final = document.querySelector('#updatedfinal').value;
                                    console.log(final);
                                    const sid = document.querySelector('#sid').innerHTML;
                                    console.log(sid);
                                    const data = new FormData();
                                    data.append('section', section);
                                    data.append('sid', sid);
                                    data.append('final', final);
                                    request.send(data);
                                    return false;
                                };


                            }
                            else {
                                document.querySelector('#infofinal').innerHTML = "";
                                document.querySelector('#finalmsg').innerHTML = "";
                                flag2++;
                            }

                        }
                        const sid2 = document.querySelector('#sid').innerHTML;
                        const sec = document.querySelector('#section').innerHTML;
                        console.log(sid2);
                        const data3 = new FormData();
                        data3.append('sid', sid2);
                        data3.append('section', sec);
                        request.send(data3);
                        return false;

                    };

                    var flag3 = 0;
                    document.querySelector('#updatequiz').onclick = () => {
                        const request = new XMLHttpRequest();
                        request.open('POST', '/instructoruser/get_quiz_marks');

                        request.onload = () => {
                            const mark = JSON.parse(request.responseText);
                            if (flag3 % 2 == 0) {
                                const t = document.createElement('table');
                                const tr1 = document.createElement('tr');
                                const th1 = document.createElement('th');
                                const th2 = document.createElement('th');
                                const th3 = document.createElement('th');
                                th1.innerHTML = "Given mark";
                                th2.innerHTML = "Updated mark";
                                tr1.append(th1, th2, th3);
                                const tr2 = document.createElement('tr');
                                const td1 = document.createElement('td');
                                td1.innerHTML = mark.quiz;
                                const td2 = document.createElement('td');
                                const input = document.createElement('input');
                                input.type = "number";
                                input.id = "updatedquiz";
                                input.placeholder = "out of 10";
                                td2.appendChild(input);
                                const td3 = document.createElement('td');
                                const btn = document.createElement('button');
                                btn.innerHTML = "Update";
                                btn.id = "updatequizmark";
                                td3.appendChild(btn)

                                // td2.innerHTML = "Updated mark";
                                tr2.append(td1, td2, td3);
                                t.append(tr1, tr2);
                                document.querySelector('#infoquiz').append(t);
                                flag3++;
                                document.querySelector('#updatequizmark').onclick = () => {

                                    const request = new XMLHttpRequest();

                                    //const email = document.querySelector('#email').value;

                                    request.open('POST', '/instructoruser/update_quiz');

                                    // Callback function for when request completes
                                    request.onload = () => {
                                        const data = JSON.parse(request.responseText);

                                        if (data.success) {

                                            document.querySelector('#quizmsg').innerHTML = "Marks updated!";
                                        }
                                        else {
                                            document.querySelector('#quizmsg').innerHTML = "Marks not updated!";
                                        }


                                    }

                                    const section = document.querySelector('#section').innerHTML;
                                    console.log(section);
                                    const quiz = document.querySelector('#updatedquiz').value;
                                    console.log(quiz);
                                    const sid = document.querySelector('#sid').innerHTML;
                                    console.log(sid);
                                    const data = new FormData();
                                    data.append('section', section);
                                    data.append('sid', sid);
                                    data.append('quiz', quiz);
                                    request.send(data);
                                    return false;
                                };


                            }
                            else {
                                document.querySelector('#infoquiz').innerHTML = "";
                                document.querySelector('#quizmsg').innerHTML = "";
                                flag3++;
                            }

                        }
                        const sid2 = document.querySelector('#sid').innerHTML;
                        const sec = document.querySelector('#section').innerHTML;
                        console.log(sid2);
                        const data3 = new FormData();
                        data3.append('sid', sid2);
                        data3.append('section', sec);
                        request.send(data3);
                        return false;

                    };

                    var flag4 = 0;
                    document.querySelector('#updateproject').onclick = () => {
                        const request = new XMLHttpRequest();
                        request.open('POST', '/instructoruser/get_project_marks');

                        request.onload = () => {
                            const mark = JSON.parse(request.responseText);
                            if (flag4 % 2 == 0) {
                                const t = document.createElement('table');
                                const tr1 = document.createElement('tr');
                                const th1 = document.createElement('th');
                                const th2 = document.createElement('th');
                                const th3 = document.createElement('th');
                                th1.innerHTML = "Given mark";
                                th2.innerHTML = "Updated mark";
                                tr1.append(th1, th2, th3);
                                const tr2 = document.createElement('tr');
                                const td1 = document.createElement('td');
                                td1.innerHTML = mark.project;
                                const td2 = document.createElement('td');
                                const input = document.createElement('input');
                                input.type = "number";
                                input.id = "updatedproject";
                                input.placeholder = "out of 10";
                                td2.appendChild(input);
                                const td3 = document.createElement('td');
                                const btn = document.createElement('button');
                                btn.innerHTML = "Update";
                                btn.id = "updateprojectmark";
                                td3.appendChild(btn)

                                // td2.innerHTML = "Updated mark";
                                tr2.append(td1, td2, td3);
                                t.append(tr1, tr2);
                                document.querySelector('#infoproject').append(t);
                                flag4++;
                                document.querySelector('#updateprojectmark').onclick = () => {

                                    const request = new XMLHttpRequest();

                                    //const email = document.querySelector('#email').value;

                                    request.open('POST', '/instructoruser/update_project');

                                    // Callback function for when request completes
                                    request.onload = () => {
                                        const data = JSON.parse(request.responseText);

                                        if (data.success) {

                                            document.querySelector('#projectmsg').innerHTML = "Marks updated!";
                                        }
                                        else {
                                            document.querySelector('#projectmsg').innerHTML = "Marks not updated!";
                                        }


                                    }

                                    const section = document.querySelector('#section').innerHTML;
                                    console.log(section);
                                    const project = document.querySelector('#updatedproject').value;
                                    console.log(project);
                                    const sid = document.querySelector('#sid').innerHTML;
                                    console.log(sid);
                                    const data = new FormData();
                                    data.append('section', section);
                                    data.append('sid', sid);
                                    data.append('project', project);
                                    request.send(data);
                                    return false;
                                };


                            }
                            else {
                                document.querySelector('#infoproject').innerHTML = "";
                                document.querySelector('#projectmsg').innerHTML = "";
                                flag4++;
                            }

                        }
                        const sid2 = document.querySelector('#sid').innerHTML;
                        const sec = document.querySelector('#section').innerHTML;
                        console.log(sid2);
                        const data3 = new FormData();
                        data3.append('sid', sid2);
                        data3.append('section', sec);
                        request.send(data3);
                        return false;

                    };
                    // request.onload = () => {
                    //     const mark = JSON.parse(request.responseText);
                    //     const t = document.createElement('table');
                    //     const tr1 = document.createElement('tr');
                    //     const th1 = document.createElement('th');
                    //     const td1 = document.createElement('td');
                    //     th1.innerHTML = "Mid1";
                    //     td1.innerHTML = mark.mid1;
                    //     tr1.append(th1, td1);

                    //     t.append(tr1);
                    //     document.querySelector('#updatemarksinfo').append(t);

                    // };
                    // // if(x%2==0){


                    // // }
                    // // else{
                    // //     document.querySelector('#msg1').innerHTML = "";
                    // //     x++;
                    // // }
                    // const sid2 = document.querySelector('#sid').innerHTML;
                    // const sec = document.querySelector('#section').innerHTML;
                    // console.log(sid2);
                    // const data3 = new FormData();
                    // data3.append('sid', sid2);
                    // data3.append('section', sec);
                    // request.send(data3);
                    // return false;

                }
                else {
                    document.querySelector('#updatemarksinfo').innerHTML = "";
                    document.querySelector('#msg1').innerHTML = "";
                    x++;
                }


            }
            else {
                if (y % 2 == 0) {
                    document.querySelector('#msg1').innerHTML = "Marks not added! Try add marks!!";
                    y++;
                }
                else {
                    document.querySelector('#msg1').innerHTML = "";
                    y++;
                }

            }

        };
        const sid2 = document.querySelector('#sid').innerHTML;
        const sec = document.querySelector('#section').innerHTML;
        console.log(sid2);
        const data3 = new FormData();
        data3.append('sid', sid2);
        data3.append('section', sec);
        request.send(data3);
        return false;


    };








});

