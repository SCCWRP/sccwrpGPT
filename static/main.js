$(document).ready(function(){
    $('#submit').click(function(){
        var question = $('#question').val();
        $.ajax({
            url: '/submit', // The endpoint on your Flask server
            type: 'POST',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({'question': question}),
            success: function(response){
                console.log(response);
                console.log("failing");
		//$('#response').html(response.message);
		$('#response').text(response.message || 'No message received');
            },
            error: function(error){
                console.log(error);
		$('#response').html('Error: ' + error);
            }
        });
    });
});