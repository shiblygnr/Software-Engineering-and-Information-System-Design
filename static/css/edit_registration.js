document.addEventListener('DOMContentLoaded', () => {
    var flag = 0;

    document.querySelectorAll('button').forEach(button => {
        button.onclick = () => {
            const request = new XMLHttpRequest();
            const selection = button.dataset.course;
            console.log(selection);
            request.open('POST', '/studentuser/edit_registered_courses');
            const data = new FormData();
            data.append('selection', selection);

            // Send request
            request.send(data);
            request.onload = () => {

                // Extract JSON data from request
                const data = JSON.parse(request.responseText);

                // Update the result div
                if (data.success) {

                    document.querySelector('#result').innerHTML = '<span class="glyphicon glyphicon-trash" ></span> Course removed!';
                }
                else {
                    document.querySelector('#result').innerHTML = 'Error!';
                }
            }

            return false;
        };

    });

});
