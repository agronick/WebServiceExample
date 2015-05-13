$(document).ready(function(){
    $.get('questions/list', function(data){
        populate_data(data)
    });

    $('#i_reload').click(function(){
        input = {
            per_page: $('#i_perpage').val(),
            start_page: $('#i_start_page').val(),
            sort: $('#i_sort').val(),
            search: $('#i_search').val(),
            csrfmiddlewaretoken: csrf()
        }
        $.post('questions/list', input, function(data){
            populate_data(data);
        });
    });

    $('#questions').on('click', '.delete-question', function(event){
        data = {
            id:  $(event.target.offsetParent).find('.question-id').val(),
            csrfmiddlewaretoken: csrf()
        }

        $.post('questions/delete', data, function(data, textStatus, xhr) {
            switch(xhr.status){
                case 200:
                    $('#i_reload').click()
                break;
                default:
                    alert('There was an error deleting the question')
            }
        });
    });

});

function populate_data(data)
{
    $('#questions').hide().html('')
    for(i in data)
    {
         answers = $('<ul>').addClass('answer');
         $.each(data[i].correct_answer, function(key, value) {
             answers.append($('<li>').text(value).addClass('correct'))
         });
         $.each(data[i].wrong_answers, function(key, value) {
            answers.append($('<li>').text(value).addClass('wrong'))
         });
         row = $('<div>');
         row.append($('<div>').addClass('question-text').text(data[i].question)).addClass('question').append(answers);
         row.append($('<input>').addClass('question-id').attr('type','hidden').attr('name', 'id').val(data[i].id))
         row.append($('<div>').addClass('delete-question'));
         $('#questions').append(row)
    }
    $('#questions').fadeIn()
}

function csrf()
{
    return jQuery("input[name='csrfmiddlewaretoken']").val()
}