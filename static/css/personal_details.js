document.addEventListener('DOMContentLoaded', () => {
    var flag = 0;

    document.querySelector('#details').onclick = () => {

        // Initialize new request
        const x = 10
        const request = new XMLHttpRequest();
        //const email = document.querySelector('#email').value;

        request.open('POST', '/studentuser/personal_details');

        // Callback function for when request completes
        request.onload = () => {

            if (flag == 0) {
                // Extract JSON data from request
                const data = JSON.parse(request.responseText);

                // Update the result div
                if (data.success == false) {
                    document.querySelector('#result1').innerHTML = 'There was an error!';
                }
                else {

                    const contents = `${data.first_name} ${data.last_name} ${data.cgpa} `
                    const p = document.createElement('p');
                    p.innerHTML = contents;

                    //alert(`${data.course_code}`);
                    document.querySelector('#result1').append(p);



                }
                flag = 1;

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
