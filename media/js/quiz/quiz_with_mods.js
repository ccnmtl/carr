function randomly(){ return 0.5 - Math.random();}

var all_quizzes_info = {}

post_test = window.location.href.match(/post_test/) != null;
pre_test = window.location.href.match(/pretest/) != null;
faculty_view = window.location.href.match(/studentquiz/) != null;

var kill_state_flag = false;
var kill_this_quiz_flag = false;
var hide_retake = false;

function disable_all_sidenav_items_after_current_one() {
    all_sidenav_items =  $$('#sidebar_left ul li')
    selected_sidenav_item =  $$('#sidebar_left ul li.selected')[0]
    all_sidenav_items.slice(all_sidenav_items.indexOf(selected_sidenav_item) + 1)
    sidenav_items_to_disable = all_sidenav_items.slice(all_sidenav_items.indexOf(selected_sidenav_item) + 1)
    forEach (sidenav_items_to_disable, disable_sidenav_item);
}

function disable_sidenav_item (item) {
    forEach(getElementsByTagAndClassName('a', null, item), hideElement)
    forEach(getElementsByTagAndClassName('span', null, item), showElement)
}


function maybeEnableNext()
{
   gonext = false
 
   if (all_done_with_quiz()) {
    gonext = true;
   }
   
   if (gonext){
      if ($('next') != null) {
         setStyle('next', {'display': 'inline'});
      }
  }
  else  {
    if ($('next') != null ) {
      setStyle('next', {'display': 'none'});
    }
    disable_all_sidenav_items_after_current_one();
  }
}

function all_done_with_quiz() {  
    if (post_test) {
      return hide_retake;
   }
  return filter (function(f) { return (f.style.display == 'block') }, $$('.answer')).length > 0;
}

function show_previous_answers_to_quiz( quiz_info) {
  question_ids_as_loaded = map (function (a) { return parseInt(a.id.split('_')[1]) }, $$('.cases.really'));
  question_ids_as_needed = map (parseInt, map (itemgetter('id'), quiz_info));
  order = map (function(a) { return findValue (question_ids_as_loaded, a) }, question_ids_as_needed);
  forEach(quiz_info ,
     function(question)
     {  
        //debug (serializeJSON(question));
        if ($(question.id + "_" + question.answer)) {
          //logDebug ("setting a question");
          $(question.id + "_" + question.answer).checked = true
        }
     });
  reorder_questions(order);
}

function show_initial_score(this_quiz, quiz_key) {
  // only show initial results for the post-test.
  return (
        // we have the answers
        this_quiz['initial_score'] &&
        this_quiz['initial_score']['answers_given'] && 
        // the post test has been completed with perfect answers, therefore training is complete
        this_quiz['all_correct'] == 't' &&
        quiz_key == 'quiz_3'
      ) ;
}


function loadStateSuccess(doc)
{

   if (!post_test) {
        // post test is the only test you are allowed to retake.
        hide_retake = true;
   }
   
   all_quizzes_info = doc;
   hideElement($('initially'));
   
   quiz_key = 'quiz_' + $('quiz_id').value;
   this_quiz = doc[quiz_key];
   
   
   test_already_taken = (this_quiz && this_quiz['question'] &&  this_quiz['question'].length > 0)
   
   logDebug ("test already taken is " + test_already_taken);
   
   
   if (test_already_taken) {
      if (show_initial_score(this_quiz, quiz_key)) {
        //logDebug ('show_initial_score');
        the_answers = this_quiz['initial_score']['answers_given'];
        setDisplayForElement('inline', $('initially'));
        hide_retake = true;
      } else {
       the_answers = this_quiz['question'];
      }
      show_previous_answers_to_quiz (the_answers);
      show_score(false);
      freeze_buttons();
   }
   else {
      //logDebug ("starting from scratch as no quiz found.");
      order = calculate_order();
      forEach ( $$('input.question'), function (a) {a.checked = false})
      thaw_buttons();
      reorder_questions(order);
   }
   
   
   
   if (order.length == 1) {
        map (hideElement, $$('.casetitle'));
        $('show_score_link').innerHTML = 'Submit Your Response';
   }
   
   maybeEnableNext();
   
   if (hide_retake) {
      hideElement ($('retake_quiz_div'));
   }
}


function freeze_buttons() {
  logDebug ('freezing buttons');
  forEach($$('input.question'), function (i) {i.disabled = true});
}

function thaw_buttons() {
  forEach($$('input.question'), function (i) {i.disabled = false});
}


function calculate_order () {
    // Returns a list of database ID's of questions in the order this quiz should display them.
 	 
     console.log( $$('.cases.really') );  
     ten_exactly = post_test ||  (pre_test && window.location.href.match(/cdm/)!= null)

     if (ten_exactly) {
	//console.log ('hey ten exactly');
        // Show some required questions, and some questions picked at random out of a hat, in a random order.
        //TODO move this functionality out of this file so Anders can use the quiz:
        //These questions *will* be on the quiz regardless of the order the questions are presented in:
        required_questions = [13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 , 22 ];
        
        // Questions that *might* be on the quiz:
        randomly_picked_questions = [23, 24, 25, 26, 27, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 51, 52];
     
        // How many of the questions that *might* be on the quiz should we add to the ones that *will* be?
         if (window.location.href.match(/cdm/)== null) {
            // last-minute change: the dental school professor wants to remove the randomly-picked questions:
            how_many_randomly_picked_questions = 10;
        
        } else {
            how_many_randomly_picked_questions = 0;   
        
        }
	//console.log( 'made it here 2 ');  
     
        //console.log( how_many_randomly_picked_questions);
        // shuffle the randomly picked questions:
        randomly_picked_questions.sort(randomly);

        // ok, pick a certain number out of the urn-- assign length in order to pick.        
        randomly_picked_questions.length = how_many_randomly_picked_questions;
        
        final_list_of_questions = required_questions.concat ( randomly_picked_questions);
        
        // reshuffle all questions together:
        final_list_of_questions.sort(randomly)
         
        question_ids_as_loaded = map (function (a) { return parseInt(a.id.split('_')[1]) },  $$('.cases.really'))
        
        question_ids_as_needed = final_list_of_questions;

        order = map (function(a) { return findValue (question_ids_as_loaded, a) }, question_ids_as_needed);
        return order;
     }
     else {
        return list(range( $$('.cases.really').length)).sort(randomly)
     }
}

function reorder_questions(order) {
    
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
    
    
    //console.log( 'done');
    
    console.log( $$('#sorted_questions_div .cases.really'));
}


function cheat()  {
  right_answers = filter (function f(a) { return getNodeAttribute (a, 'right_answer') == 'True'},  $$('#sorted_questions_div .question'));
  forEach(right_answers, function f(a)  { a.checked = true; });
}


function debug(string)
{
   if (true)
      log("DEBUG " + string)
}

// default behavior, called from the show score button when the user first submits the quiz.
function showScore() {
    show_score(true)
}

function show_score(fresh_answers)
{
    // all visible answers:
    all_answers = $$('#sorted_questions_div input.question')
    quiz_key =  'quiz_' + $('quiz_id').value;    

    // all chosen answers:
    chosen_answers = filter (function f(a) {return a.checked}, all_answers) 
    
    number_of_questions_to_answer = $$('#sorted_questions_div .cases').length
    
    // If the user just took the quiz, do basic_validation before scoring.
    if (fresh_answers) {
        if (chosen_answers.length < number_of_questions_to_answer) {
            alert ('Please answer all the questions.');
            return;
        }
        
        if (!confirm ('Are you done?')) {
            return;
        }
    }
    
    // show all the correct answers:
    map (showElement , $$('.answer'));
    hideElement ('show_score');
    max_score = chosen_answers.length   
    actual_score = filter (function f(a) {return getNodeAttribute (a, 'right_answer') == 'True'}, chosen_answers).length
    
    if (actual_score == max_score) {
      hide_retake = true;
      // used in the final quiz to determine whether you can advance to the next page.
    }
   
    make_these_green = filter (function f(a) {return getNodeAttribute (a, 'right_answer') == 'True'}, $$('.question'));
    
    forEach (make_these_green, function(a) { addElementClass (a.parentNode, 'correct_answer')});
    
    if (max_score > 1) {
        $('quiz_score').innerHTML = actual_score;
        $('quiz_max_score').innerHTML = max_score;
        showElement('show_quiz_results');
    }
    
    //store the first score; for diagnostic tests that might be taken several times:
    //quiz_id = $('quiz_id').value;
    if (  typeof(all_quizzes_info [quiz_key]) == 'undefined') {
        all_quizzes_info [quiz_key] = {}
    }
    if ( typeof(all_quizzes_info [quiz_key]['initial_score'] ) == 'undefined') {
       logDebug ("Initial score not found; saving:");
        all_quizzes_info [quiz_key]['initial_score']  = { 
            'quiz_score': actual_score, 
            'quiz_max_score': max_score, 
            // store the answers:
            'answers_given' : collect_question_info()
        };
        //logDebug (all_quizzes_info);
    }
    
    if  (actual_score > 0 && actual_score == max_score) {
        all_quizzes_info [quiz_key]['all_correct'] = 't';
        // You got all the answers right; no need to retake the test.
        hideElement ('retake_quiz_div');
        
    } else {
        all_quizzes_info [quiz_key]['all_correct'] = 'f';
    }
    
    if ( typeof(all_quizzes_info [quiz_key]['submit_time'] ) == 'undefined') {
        all_quizzes_info [quiz_key]['submit_time'] = [Date()];
    }
    else {
        all_quizzes_info [quiz_key]['submit_time'].push (Date());
    }
    
    //logDebug ("all correct is:");
    //logDebug (all_quizzes_info [quiz_key]['all_correct']);

    if (!pre_test) {
        if (!hide_retake)  {
            showElement ('retake_quiz_div');
        } else {
            // set this to true to indicate that the training is complete.
            all_quizzes_info [quiz_key]['all_correct'] = 't';
        }
    }
    
    if (post_test && (!hide_retake)) {
      alert ('You must score 100% on the post-test to receive credit for this training. Please click "Retake Quiz" and try again. ');
    }
    
   freeze_buttons();
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
        hide_retake = true; // no reason for a faculty member to be interested in the "retake quiz" link.
        loadStateSuccess(student_quiz);
        return;
    }

   url = "/activity/quiz/load/"
   deferred = loadJSONDoc(url)
   deferred.addCallbacks(loadStateSuccess, loadStateError);
}


function collect_question_info() {
  var question_info = [];
  forEach(getElementsByTagAndClassName('*', 'question'),
    function(question) {
      if (question.checked)
      {
         a = question.id.split('_');
         q = {};
         q['id'] = a[0];
         q['answer'] = a[1];
         question_info.push(q);
      }
    });
  return question_info;
}


function saveState()
{   
    if (typeof student_response != "undefined") {
      return;
    }

    what_to_send = all_quizzes_info;
    url = "/activity/quiz/save/"
    //quiz_id = $('quiz_id').value;
   quiz_key =  'quiz_' + $('quiz_id').value;
   
   all_answers = $$('#sorted_questions_div input.question')
   chosen_answers = filter (function f(a) {return a.checked}, all_answers) 
   number_of_questions_to_answer = $$('#sorted_questions_div .cases').length
   
   
   // don't delete initial score:
   initial_score_found = null;
   
   if (all_quizzes_info != undefined &&
       all_quizzes_info [quiz_key] != undefined
       && all_quizzes_info [quiz_key]['initial_score'] != undefined) {
      initial_score_found = all_quizzes_info [quiz_key]['initial_score'];
   }
   
   
   if (chosen_answers.length < number_of_questions_to_answer) {
      // only saving state if all the questions are answered.
      return;
   }
   
   
   if (show_initial_score(all_quizzes_info [quiz_key], quiz_key)) {
      // do not overwrite state with the displayed initial answers:
      //logDebug (JSON.stringify ( what_to_send [quiz_key ]));
      
      //alert ('keeping existing state.');
      what_to_send [quiz_key ]['question'] = collect_question_info();
      
      // keep everything as is and save.
   }
   else {
             if  (kill_this_quiz_flag) {
                logDebug ("Do save the initial results, but delete all question and answer info.");
                delete what_to_send [quiz_key]['question'];
             }
             else {
                 if (what_to_send [quiz_key] != undefined) {
                   logDebug ("Deleting all info for quiz, so it can be replaced with the quiz you just took.");
                   delete what_to_send [quiz_key]['question']
                 }else {
                   logDebug ("No info found on this quiz.");
                   what_to_send [quiz_key] = {};
                 }
                 if (initial_score_found != null) {
                    logDebug ("Found an initial score, so preserving it.");
                    what_to_send  [quiz_key]['initial_score'] = initial_score_found;
                 }
                 what_to_send [quiz_key ]['question'] = collect_question_info();
             }
   }
    var xmlhttp;
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    } else {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.open("POST", url, false);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xmlhttp.send(queryString({'json':serializeJSON(what_to_send)}));
}

function retakeQuiz()
{
    if (!confirm ('Are you sure you want to start the quiz again? This will erase your answers.'))  {
        return;
    }
    hideElement ('show_quiz_results');
    
    kill_this_quiz();
    window.location.reload();
}

function kill_state()  {   
    kill_state_flag = true;
   
}

function kill_this_quiz()  {   
    kill_this_quiz_flag = true;
}

MochiKit.Signal.connect(window, "onload", loadState);
MochiKit.Signal.connect(window, "onbeforeunload", saveState)
