document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#gradesubmitted').onclick = () => {
        var len = document.querySelectorAll('.grade').length;
        
        
        
        var section = document.querySelector('#hide1').innerHTML;
        var count = 0;
        document.querySelectorAll('.grade').forEach(grade => {
            const request = new XMLHttpRequest();
            var flag = 0;
            //const email = document.querySelector('#email').value;
            request.open('POST', '/instructoruser/add_grade');
            
            request.onload = () => {
                console.log("yes");
                var d = JSON.parse(request.responseText);
                if(d.success){
                    console.log("yes");
                    document.querySelector('#msg').innerHTML = "Grade submitted!";
                }
            }
            sid = grade.dataset.id;
            g = grade.value;
            console.log(sid);
            console.log(g);
            console.log(section);
            const data = new FormData();
            data.append('sid', sid);
            data.append('grade', g);
            data.append('section', section);
            request.send(data);
            flag = 1;
            // return false;

        });
        
            
        




        // var sids = grades.dataset.id;

        // for( var i = 0; i<sids.length; i++){
        //     console.log(sids[i]);
        // }

        // for( var i = 0; i<grades.length; i++){
        //     console.log(grades[i].value);
        // }
        

    }

});