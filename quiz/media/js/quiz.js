function randomly(){    return (Math.round(Math.random())-0.5);}

function calculate_order () {
    //Show all questions:
    //return list(range($$('.cases').length))
    
    //Show all questions in a random order:
    // return list(range($$('.cases').length)).sort(randomly)
 
    // Show a certain number of required questions, then a certain number of random questions.
 
     if (window.location.href.match(/post_test/)) {
        normal_order_questions = [1];
        
        random_order_questions = [2];
        
        how_many_random_order_questions = 1;
        
        random_order_questions.sort(randomly)
        
        random_order_questions.length = how_many_random_order_questions;
        
        tmp = normal_order_questions.concat ( random_order_questions)
        
        return  tmp.sort(randomly)
     }
     else {
        return list(range($$('.cases').length)).sort(randomly)
     }
}

function shuffle_questions(order) {

    nums = list(range(order.length))
    if ($("sorted_questions_div")) {
        removeElement ($("sorted_questions_div"));
    }
    
    //create placeholders for the sorted questions
    $('sorted_questions').appendChild (DIV ({id : "sorted_questions_div"}, map (DIV, nums)));
    
    destination_divs = $('sorted_questions_div').childNodes;

    source_divs = $$('.cases')

    // swap the questions and the placeholders:
    map (function f (a) { swapDOM (a[0], a[1])}, zip (destination_divs, source_divs));
    
    // show the resulting sorted divs, leaving the others hidden as per the CSS file.
    map (function f (a) { setStyle (a, {'display':'block'}) }, $$('#sorted_questions_div div.cases'))

    // number the questions:
    map (function f (a) { a[0].innerHTML = a[1] + 1}, zip ($$('#sorted_questions_div .question_order'), nums));

}

function debug(string)
{
   if (true)
      log("DEBUG " + string)
}

function retakeQuiz()
{

    if (!confirm ('Are you sure you want to start the quiz again? This will erase your answers.')) {
        return;
    }
    hideElement ('show_quiz_results')
    map (function f(q){ q.checked = false},$$('input.question'))
    saveState()
    window.location.reload()
}


function onChooseAnswer(ctrl)
{
   a = ctrl.id.split('_')
   // set rhetorical questions to display:
   //if ($(a[0] + "_answer")) {
   // setStyle(a[0] + "_answer", {'display':'block'})
   // }
}

function loadStateSuccess(doc)
{  
   
   
   order = calculate_order();
   shuffle_questions(order);
   forEach(doc.question,
           function(question)
           {  
              debug (serializeJSON(question));
              if ($(question.id + "_" + question.answer)) {
                $(question.id + "_" + question.answer).checked = true
              }
           })
   //maybeEnableNext()
}

function showScore()
{
   
   // TODO consider wiping all answers on retake test.
   // makes sense. Otherwise, if you answer wrong, you only have a chance to right the wrong if you're lucky enough to randomly see the question again.
   
    
    // all visible answers:
    all_answers = $$('#sorted_questions_div input.question')
    
    // all chosen answers:
    chosen_answers = filter (function f(a) {return a.checked}, all_answers) 
    
    number_of_questions_to_answer = $$('#sorted_questions_div .cases').length
    
    
    if (chosen_answers.length < number_of_questions_to_answer) {
        alert ('Please answer all the questions.');
        return;
    }
    
    if (!confirm ('Are you done?')) {
        return;
    }
    
    // show all the correct answers:
    map (showElement , $$('.answer'))
    
    hideElement ('show_score');
    
    //TODO make sure that on "show score" all answers are ready. propmt for remaining unanaswered questions.
    
    max_score = chosen_answers.length
   
    actual_score = filter (function f(a) {return getNodeAttribute (a, 'right_answer') == 'True'}, chosen_answers).length
   
     //You scored <span ="quiz_score"> </span> out of a possible <span ="quiz_max_score"> </span>
    
    $('quiz_score').innerHTML = actual_score;
    
    $('quiz_max_score').innerHTML = max_score;
    
    
    showElement('show_quiz_results');
    
    showElement ('retake_quiz_div');
}

function loadStateError(err)
{
   debug("loadStateError")
   // @todo: Find a spot to display an error or decide just to fail gracefully
   // $('errorMsg').innerHTML = "An error occurred loading your state (" + err + "). Please start again."
}

function loadState()
{
   debug("loadState")
   url = 'http://' + location.hostname + ':' + location.port + "/activity/quiz/load/"
   deferred = loadJSONDoc(url)
   deferred.addCallbacks(loadStateSuccess, loadStateError)
}

MochiKit.Signal.connect(window, "onload", loadState)

function saveState()
{   url = 'http://' + location.hostname + ':' + location.port + "/activity/quiz/save/"
 
   doc = 
   {
      'question': []
   }
   
   questions = getElementsByTagAndClassName('*', 'question')
              
   forEach(questions,
           function(question) {
              if (question.checked)
              {
                 a = question.id.split('_')
                 q = {}
                 
                 
                 q['id'] = a[0]
                 q['answer'] = a[1]
                 doc['question'].push(q)
              }
           })
    debug (JSON.stringify(doc, null))
    
    
   // save state via a synchronous request. 
   var sync_req = new XMLHttpRequest();  
   sync_req.onreadystatechange= function() { if (sync_req.readyState!=4) return false; }         
   sync_req.open("POST", url, false);
   sync_req.send(queryString({'json':JSON.stringify(doc, null)}));
}

MochiKit.Signal.connect(window, "onbeforeunload", saveState)
