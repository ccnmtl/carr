function randomly(){ return 0.5 - Math.random();}

var all_quizzes_info = {}

post_test = window.location.href.match(/post_test/) != null;
pre_test = window.location.href.match(/pretest/) != null;

var kill_state_flag = false;
var kill_this_quiz_flag = false;

function loadStateSuccess(doc)
{  

     if (pre_test) {
        hideElement ($('retake_quiz_div'));
     }
     

   all_quizzes_info = doc;
   the_key = 'quiz_' + $('quiz_id').value
   
   if (doc[the_key] && doc[the_key]['question'].length > 0){
        logDebug ("found info for this quiz.");
        this_quiz_info = doc[the_key]
        question_ids_as_loaded = map (function (a) { return parseInt(a.id.split('_')[1]) }, $$('.cases.really'))
        
        question_ids_as_needed = map (parseInt, map (itemgetter('id'), doc[the_key]['question']))
        order  = map (function (a) { return question_ids_as_loaded.indexOf(a)  },  question_ids_as_needed)
        
        forEach(this_quiz_info.question,
               function(question)
               {  
                  //debug (serializeJSON(question));
                  if ($(question.id + "_" + question.answer)) {
                    //logDebug ("setting a question");
                    $(question.id + "_" + question.answer).checked = true
                  }
               });
               
         show_score(false);
   }
   else {
        logDebug ("starting from scratch as no quiz found.");
        order = calculate_order();
        
        
        forEach ( $$('input.question'), function (a) {a.checked = false})
   }
   
   
   shuffle_questions(order);
   
   if (order.length == 1) {
        // don't bother showing certain elements if the quiz only contains one question)
        map (hideElement, $$('.casetitle'));
   }
   
   //maybeEnableNext()
    
}


function calculate_order () {
    // Returns a list of database ID's of questions in the order this quiz should display them.

    
     if (post_test) {
        
        // Show a some required questions, and some questions picked at random out of a hat, in a random order.
        
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
         
        question_ids_as_loaded = map (function (a) { return parseInt(a.id.split('_')[1]) },  $$('.cases.really'))
        
        question_ids_as_needed = final_list_of_questions;
        
        order  = map (function (a) { return question_ids_as_loaded.indexOf(a)  },  question_ids_as_needed)
        
        return order;
        
     }
     else {
        return list(range( $$('.cases.really').length)).sort(randomly)
     }
     
     
    //Show all questions:
    //return list(range($$('.cases').length))
    
    //Show all questions in a random order:
    // return list(range($$('.cases').length)).sort(randomly)
}

function shuffle_questions(order) {


    // ORDER is a new ordering of the existing questions in $$(.'cases')
    logDebug ("Order is : " + order);
    logDebug ("Length of order is : " + order.length);
    
    nums = list(range(order.length))
    
    //create placeholders for the sorted questions
    $('sorted_questions').appendChild (DIV ({id : "sorted_questions_div"}, map (DIV, nums)));
    
    existing_case_divs =  $$('.cases.really');
    
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



// default behavior: do validate.
function showScore() {
    show_score(true)
}



function show_score(validate)
{
   // TODO consider wiping all answers on retake test.
   // makes sense. Otherwise, if you answer wrong, you only have a chance to right the wrong if you're lucky enough to randomly see the question again.
   
    
    // all visible answers:
    all_answers = $$('#sorted_questions_div input.question')
    
    // all chosen answers:
    chosen_answers = filter (function f(a) {return a.checked}, all_answers) 
    
    number_of_questions_to_answer = $$('#sorted_questions_div .cases').length
    
    
    if (validate) {
        
        if (chosen_answers.length < number_of_questions_to_answer) {
            alert ('Please answer all the questions.');
            return;
        }
        
        if (!confirm ('Are you done?')) {
            return;
        }
    }
    // show all the correct answers:
    map (showElement , $$('.answer'))
    
    hideElement ('show_score');
    
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
    
    if (!pre_test) {
        showElement ('retake_quiz_div');
    }
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
{   

    url = 'http://' + location.hostname + ':' + location.port + "/activity/quiz/save/"
    quiz_id = $('quiz_id').value;
   
   
   if (kill_state_flag) {
        // kill all state info for this user.
        what_to_send = {}
   } 
   
   else if  (kill_this_quiz_flag) {
   
        what_to_send = all_quizzes_info;
        delete what_to_send ['quiz_' + quiz_id]
   
   }
   else {
       
       what_to_send = all_quizzes_info
       question_info = 
       {
          'question': []
       }
       delete what_to_send ['quiz_' + quiz_id]
       questions = getElementsByTagAndClassName('*', 'question')
       forEach(questions,
               function(question) {
                  if (question.checked)
                  {
                     a = question.id.split('_')
                     q = {}
                     
                     
                     q['id'] = a[0]
                     q['answer'] = a[1]
                     question_info['question'].push(q)
                  }
               })
               
        
        
           // save state via a synchronous request.
           //what_to_send =  all_quizzes_info;
           what_to_send ['quiz_' + quiz_id ] = question_info;
   }
   
   
   debug (what_to_send)

   var sync_req = new XMLHttpRequest();  
   sync_req.onreadystatechange= function() { if (sync_req.readyState!=4) return false; }         
   sync_req.open("POST", url, false);
   
   sync_req.send(queryString({'json':JSON.stringify(what_to_send, null)}));
}


function retakeQuiz()
{
    if (!confirm ('Are you sure you want to start the quiz again? This will erase your answers.'))  {
        return;
    }
    hideElement ('show_quiz_results');
    kill_this_quiz()
    window.location.reload()
}


function kill_state()  {   
    kill_state_flag = true;
   

}


function kill_this_quiz()  {   
    kill_this_quiz_flag = true;

}



MochiKit.Signal.connect(window, "onbeforeunload", saveState)
