function post_message(){
    let msgForm = document.getElementById("msg_form");
    msgForm.action = "/message";
    msgForm.submit();
}

function ask_question(){
    let msgForm = document.getElementById("msg_form");
    msgForm.action = "/question";
    msgForm.submit();
}

