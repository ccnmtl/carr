function randomly(){ return 0.5 - Math.random();}

post_test = window.location.href.match(/post_test/);

function calculate_order () {
 
    // Show a some required questions, and some questions picked at random out of a hat, in a random order..
     if (post_test) {
        
        //TODO move this functionality out of this file so Anders can use the quiz:
        
        
        
        //These questions *will* be on the quiz regardless of the order the questions are presented in:
        required_questions = [13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 , 22 ];

        // These questions are questions that *might* be on the quiz:
        randomly_picked_questions = [23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 42, 43, 44, 45, 46, 47, 48, 49, 51, 52];
     
        // How many of the questions that *might* be on the quiz should we add to the ones that *will* be?
        how_many_randomly_picked_questions = 10;
        
        // shuffle the randomly picked questions:
        randomly_picked_questions.sort(randomly);

        // ok, pick a certain number out of the urn-- assign length in order to pick.        
        randomly_picked_questions.length = how_many_randomly_picked_questions;
        
        final_list_of_questions = required_questions.concat ( randomly_picked_questions);
        
        // reshuffle all questions together:
        final_list_of_questions.sort(randomly)
        
        return final_list_of_questions;
     }
     else {
        return list(range($$('.cases').length)).sort(randomly)
     }
     
     
    //Show all questions:
    //return list(range($$('.cases').length))
    
    //Show all questions in a random order:
    // return list(range($$('.cases').length)).sort(randomly)
}

function shuffle_questions(order) {
    // ORDER is an array of database ID's of questions. It is assumed that all questions we need are on the page.
    nums = list(range(order.length))
    
    //create placeholders for the sorted questions
    $('sorted_questions').appendChild (DIV ({id : "sorted_questions_div"}, map (DIV, nums)));
    
    existing_case_divs = $$('.cases');
    
    // source_divs is a new ordering of the existing, currently hidden divs.
    source_divs = map (function(a) { return existing_case_divs[a]}, order)

    //destination_divs is a bunch of empty placeholder divs:
    destination_divs = $('sorted_questions_div').childNodes;

    // swap the questions and the placeholders:
    map (function f (a) { swapDOM (a[0], a[1])}, zip (destination_divs, source_divs));
    
    // show the resulting sorted divs, leaving the un-chosen ones hidden as per the CSS file.
    map (function f (a) { setStyle (a, {'display':'block'}) }, $$('#sorted_questions_div div.cases'))

    // number the questions according to their new position:
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
   
   if (order.length == 1) {
    // don't bother showing certain elements if the quiz only contains one question)
    map (hideElement, $$('.casetitle'));
   }
   
   forEach(doc.question,
           function(question)
           {  
              //debug (serializeJSON(question));
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
    
    //TODO make sure that on "show score" all answers are ready. prompt for remaining unanaswered questions.
    
    max_score = chosen_answers.length
   
    actual_score = filter (function f(a) {return getNodeAttribute (a, 'right_answer') == 'True'}, chosen_answers).length
   
     //You scored <span ="quiz_score"> </span> out of a possible <span ="quiz_max_score"> </span>
    
    if (max_score > 1) {
        
        $('quiz_score').innerHTML = actual_score;
        
        $('quiz_max_score').innerHTML = max_score;
        
        showElement('show_quiz_results');
    
    }
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
