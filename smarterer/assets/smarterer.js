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

    $('#questions').on('click', '.edit-question', function(event){
        $.get('questions/' +  $(event.target.offsetParent).find('.question-id').val(), function(data){
            var question = data.question
            var id = data.id
            var answers = []
            //Put the correct answer first
            $.each(data.correct_answer, function(id, item){
                answers.push(item)
            });
            $.each(data.wrong_answers, function(id, item){
                answers.push(item)
            });
            reset_edit()
            populate_edit(id, question, answers, 0)
            $('#edit_wrapper').fadeIn()
        });
    });

    $('#save_answer').click(function(){

        var correct_index = -1;
        var answers = [];

        $('#answer_list .answer_wrap').each(function(index){
            var val = $(this).children('.answer').val().trim()
            if(!!val)
                answers.push(val)

            if($(this).children('.a_correct').is(':checked'))
                correct_index = index;
        })

        data = {
            question: $('#a_question').val(),
            answers: answers,
            correct: correct_index,
            csrfmiddlewaretoken: csrf(),
            id: $('#a_id').val()
        }

        if(data.correct_index == -1 || data.question.trim().length < 3)
            return false;

        var url = (data.id == '-1') ? 'questions/new' : 'questions/' + data.id + '/edit'

        $.post(url, data, function(data){
            console.log(data)
        });

        return false;
    });


    $('#window_close').click(function(){
        $(this).parents('#edit_wrapper').fadeOut();
    });

    $('#i_new').click(function(){
        reset_edit();
        $('#edit_wrapper').fadeIn();
    });

    $('#add_answer').click(function(){
        add_answer('', false)
        return false;
    });
});

function reset_edit()
{
    $('#a_question').val('');
    $('#a_id').val('-1');
    $('#answer_list').children().remove()
}

var delete_answer_row = function(item)
{
    $(this).parent().fadeOut(function(){
        $(this).remove()
    });
    return false;
}

function populate_edit(qid, question, answers, correct_id)
{
    $('#a_id').val(qid)
    $('#a_question').val(question)
    console.log(answers)
    var item
    for(index in answers)
    {
        add_answer(answers[index], correct_id == index)
    }
}

function add_answer(item, is_correct)
{
        var answer_clone = $('#answer_clone').children('.answer_wrap').clone()
        answer_clone.children('.answer').val(item)
        answer_clone.children('.a_correct').attr("checked", is_correct);
        answer_clone.children('.delete_ans').click(delete_answer_row)
        $('#answer_list').append(answer_clone)
}

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
         row.append($('<div>').addClass('edit-question'));
         $('#questions').append(row)
    }
    $('#questions').fadeIn()
}

function csrf()
{
    return jQuery("input[name='csrfmiddlewaretoken']").val()
}