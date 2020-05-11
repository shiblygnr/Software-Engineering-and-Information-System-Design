document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('button').forEach(button => {
        button.onclick = () => {
            const request = new XMLHttpRequest();
            //const email = document.querySelector('#email').value;

            request.open('POST', '/studentuser/added_courses');

            request.onload = () => {
                const data = JSON.parse(request.responseText);

                for (var i = 0; i < data.length; i++) {
                    const contents = `${data[i].course_code} ${data[i].section_no} ${data[i].capacity}`
                    const p = document.createElement('p');
                    p.innerHTML = contents;
                    document.querySelector('#result').append(p);

                }






            }
            const data = new FormData();
            const selection = button.dataset.course;
            data.append('selection', selection);

            // Send request
            request.send(data);
            return false;
            //const selection = button.dataset.course;
            //socket.emit('add course', {'selection': selection});
        };
    });

});