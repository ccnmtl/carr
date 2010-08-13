function randomly(){ return 0.5 - Math.random();}

var all_quizzes_info = {}

post_test = window.location.href.match(/post_test/) != null;
pre_test = window.location.href.match(/pretest/) != null;

var kill_state_flag = false;
var kill_this_quiz_flag = false;
var perfect_score = false;


function maybeEnableNext()
{
   gonext = false
 
   if (all_done_with_quiz()) {
    gonext = true;
   }
   
   if (gonext){
         setStyle('next', {'display': 'inline'}) 
   }
  else
  {
     setStyle('next', {'display': 'none'}) 
  }
  
}

function all_done_with_quiz() {  
    if (post_test) {
      return perfect_score;
   }
  return filter (function(f) { return (f.style.display == 'block') }, $$('.answer')).length > 0;
}




function loadStateSuccess(doc)
{   
    logDebug ("loadStateSuccess");
   if (pre_test) {
        hideElement ($('retake_quiz_div'));
   }
   
   all_quizzes_info = doc;
   the_key = 'quiz_' + $('quiz_id').value
   
   test_already_taken = (doc[the_key] && doc[the_key]['question'].length > 0)
   
   if (test_already_taken){
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
   }
   else {
        logDebug ("starting from scratch as no quiz found.");
        order = calculate_order();
        
        
        forEach ( $$('input.question'), function (a) {a.checked = false})
   }
   
   shuffle_questions(order);
   
   // adding this:
   if (test_already_taken) {
         show_score(false);
   }
   
   if (order.length == 1) {
        // adjust a couple things if the quiz only contains one question:
        map (hideElement, $$('.casetitle'));
        $('show_score_link').innerHTML = 'Submit Your Response';
   }
   
   maybeEnableNext();
    
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
         if (window.location.href.match(/cdm/)== null) {
            // last-minute change: the dental school professor wants to remove these:
            how_many_randomly_picked_questions = 10;
        
        } else {
            how_many_randomly_picked_questions = 0;   
        
        }


        
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
    //logDebug ("Order is : " + order);
    //logDebug ("Length of order is : " + order.length);
    
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
    
    
    var cheat == false;
    
    if (cheat) {
      right_answers = filter (function f(a) { return getNodeAttribute (a, 'right_answer') == 'True'}, $$('.question'))
      forEach(right_answers, function f(a)  { a.checked = true; });
    }
    
}

/*

delete from carr_main_sitestate;
delete from quiz_activitystate;
insert into carr_main_sitestate (user_id, last_location, visited) values (
          5,
          '/carr/conclusion/post_test/',
          '{"622": "Abuse or Accident 3 (ssw)", "621": "Abuse or Accident 2 (ssw)", "620": "Abuse or Accident 1 (ssw)", "259": "CARR", "239": "Introduction", "252": "Activity: Abuse or Accident?", "253": "Reporting Process", "250": "Signs of Abuse", "251": "Activity: Cases", "256": "Post-Test", "254": "Video Assignment", "255": "Activity: When and How to Take Action", "1": "Root", "618": "case_3", "619": "Intro: Abuse or Accident?", "616": "case_1", "617": "case_2", "245": "NY State Statistics", "244": "Overview and Objectives", "247": "Relevant Legislation", "246": "Pre-test", "241": "Recognizing Abuse", "240": "The Law", "243": "Conclusion", "242": "Reporting Abuse", "249": "Types of Abuse", "248": "The Mandated Reporter"}'
);


*/



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
   // logDebug ("show score");
    
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
    
    
    //TODO make sure that on "show score" all answers are ready. prompt for remaining unanaswered questions.
    
    max_score = chosen_answers.length
   
    actual_score = filter (function f(a) {return getNodeAttribute (a, 'right_answer') == 'True'}, chosen_answers).length
    
    
    if (actual_score == max_score) {
      perfect_score = true;
      // used in the final quiz to determine whether you can advance to the next page.
    }
   
    make_these_green = filter (function f(a) {return getNodeAttribute (a, 'right_answer') == 'True'}, $$('.question'));
    //make_these_red   = filter (function f(a) {return getNodeAttribute (a, 'right_answer') != 'True'}, $$('.question'));
    
    forEach (make_these_green, function(a) { addElementClass (a.parentNode, 'correct_answer')});
    //forEach (make_these_red,   function(a) { addElementClass (a.parentNode, 'incorrect_answer')});
    
    
     //You scored <span ="quiz_score"> </span> out of a possible <span ="quiz_max_score"> </span>
    
    if (max_score > 1) {
        
        $('quiz_score').innerHTML = actual_score;
        
        $('quiz_max_score').innerHTML = max_score;
        
        showElement('show_quiz_results');
    
    }
    
    //store the first score; for diagnostic tests that might be taken several times:
        quiz_id = $('quiz_id').value;
        if (  typeof(all_quizzes_info ['quiz_' + quiz_id]) == 'undefined') {
            all_quizzes_info ['quiz_' + quiz_id] = {}
        }
        if ( typeof(all_quizzes_info ['quiz_' + quiz_id]['initial_score'] ) == 'undefined') {
           logDebug ("Initial score not found; saving:");
            
            all_quizzes_info ['quiz_' + quiz_id]['initial_score']  = { 
                'quiz_score': actual_score, 
                'quiz_max_score': max_score 
            };
            logDebug (all_quizzes_info);
        }
        else {
           // logDebug ("Initial score found:");
           // logDebug (serializeJSON(all_quizzes_info ['quiz_' + quiz_id]['initial_score']));
        }
        if  (actual_score > 0 && actual_score == max_score) {
            all_quizzes_info ['quiz_' + quiz_id]['all_correct'] = 't';
        } else {
            all_quizzes_info ['quiz_' + quiz_id]['all_correct'] = 'f';
        }
        //logDebug ("all correct is:");
        //logDebug (all_quizzes_info ['quiz_' + quiz_id]['all_correct']);
    
    if (!pre_test) {
        showElement ('retake_quiz_div');
    }
    
    
    if (post_test && (actual_score != max_score)) {
      alert ('You must score 100% on the post-test to receive credit for this training. Please click "Retake Quiz" and try again. ');
    }


   maybeEnableNext();
   
   
   
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
    if (typeof student_quiz != "undefined") {
        //alert ("A");
        loadStateSuccess(student_quiz);
        return;
    }

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
       question_info = []
       delete what_to_send ['quiz_' + quiz_id]['question']
       questions = getElementsByTagAndClassName('*', 'question')
       forEach(questions,
               function(question) {
                  if (question.checked)
                  {
                     a = question.id.split('_')
                     q = {}
                     q['id'] = a[0]
                     q['answer'] = a[1]
                     question_info.push(q)
                  }
               })
           // save state via a synchronous request.
           what_to_send ['quiz_' + quiz_id ]['question'] = question_info;
   }
   
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
