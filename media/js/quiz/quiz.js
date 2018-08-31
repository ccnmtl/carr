/*eslint no-unused-vars: ["error", {
  "varsIgnorePattern":
  "cheat|number_of_questions_to_answer|retakeQuiz" }]*/
/* global student_quiz: true, CARE: true, required_questions: true */
/* global optional_questions: true */

function randomly() {
    return 0.5 - Math.random();
}

var all_quizzes_info = {};

var post_test = window.location.href.match(/post_test/) !== null;
var pre_test = window.location.href.match(/pretest/) !== null;

var kill_this_quiz_flag = false;
var hide_retake = false;

function disable_all_sidenav_items_after_current_one() {
    var all_sidenav_items =  $$('#sidebar_left ul li');
    var selected_sidenav_item =  $$('#sidebar_left ul li.selected')[0];
    all_sidenav_items.slice(
        all_sidenav_items.indexOf(selected_sidenav_item) + 1);
    var sidenav_items_to_disable = all_sidenav_items.slice(
        all_sidenav_items.indexOf(selected_sidenav_item) + 1);
    forEach(sidenav_items_to_disable, disable_sidenav_item);
}

function disable_sidenav_item(item) {
    forEach(getElementsByTagAndClassName('a', null, item), hideElement);
    forEach(getElementsByTagAndClassName('span', null, item), showElement);
}

function maybeEnableNext() {
    var gonext = false;

    if (all_done_with_quiz()) {
        gonext = true;
    }

    if (gonext) {
        if ($('next') !== null) {
            setStyle('next', {'display': 'inline'});
        }
    } else {
        if ($('next') !== null) {
            setStyle('next', {'display': 'none'});
        }
        disable_all_sidenav_items_after_current_one();
    }
}

function all_done_with_quiz() {
    if (post_test) {
        return hide_retake;
    }
    return filter(function(f) {
        return (f.style.display === 'block');
    }, $$('.answer')).length > 0;
}

function show_previous_answers_to_quiz(quiz_info) {
    var question_ids_as_loaded = map(function(a) {
        return parseInt(a.id.split('_')[1]);
    }, $$('.cases.really'));
    var question_ids_as_needed = map(parseInt, map(itemgetter('id'),
        quiz_info));
    var order = map(function(a) {
        return findValue(question_ids_as_loaded, a);
    }, question_ids_as_needed);
    forEach(quiz_info,
        function(question) {
            if ($(question.id + '_' + question.answer)) {
                $(question.id + '_' + question.answer).checked = true;
            }
        });
    reorder_questions(order);
}

var initialScoreKey = 'initial_score';
var answersGivenKey = 'answers_given';
var allCorrectKey = 'all_correct';

function show_initial_score(this_quiz, quiz_key) {
    // only show initial results for the post-test.
    return (
        // we have the answers
        this_quiz[initialScoreKey] &&
            this_quiz[initialScoreKey][answersGivenKey] &&
            this_quiz[allCorrectKey] === 't' &&
            quiz_key === 'quiz_3'
    );
}

function loadStateSuccess(doc) {

    if (!post_test) {
        // post test is the only test you are allowed to retake.
        hide_retake = true;
    }

    all_quizzes_info = doc;
    hideElement($('initially'));

    var quiz_key = 'quiz_' + $('quiz_id').value;
    var this_quiz = doc[quiz_key];

    var test_already_taken = (this_quiz && this_quiz.question &&
                              this_quiz.question.length > 0);

    logDebug('test already taken is ' + test_already_taken);

    var order;
    if (test_already_taken) {
        var the_answers;
        if (show_initial_score(this_quiz, quiz_key)) {
            the_answers = this_quiz[initialScoreKey][answersGivenKey];
            setDisplayForElement('inline', $('initially'));
            hide_retake = true;
        } else {
            the_answers = this_quiz.question;
        }
        show_previous_answers_to_quiz(the_answers);
        show_score();
        freeze_buttons();
    } else {
        order = calculate_order();
        forEach($$('input.question'), function(a) {
            a.checked = false;
        });
        thaw_buttons();
        reorder_questions(order);
    }
    if (order.length === 1) {
        map(hideElement, $$('.casetitle'));
        $('show_score_link').innerHTML = 'Submit Your Response';
    }
    maybeEnableNext();
    if (hide_retake) {
        hideElement($('retake_quiz_div'));
    }
}

function freeze_buttons() {
    logDebug('freezing buttons');
    forEach($$('input.question'), function(i) {
        i.disabled = true;
    });
}

function thaw_buttons() {
    forEach($$('input.question'), function(i) {i.disabled = false;});
}

function calculate_order() {
    // Returns a list of database ID's of questions
    // in the order this quiz should display them.
    // required_questions & optional_questions are rendered
    // via the quiz block

    if (post_test) {
        if (CARE.isSocialWork) {
            // SSW adds 10 random questions to the required questions

            // shuffle the randomly picked questions:
            optional_questions.sort(randomly);

            // ok, pick a certain number out of the urn --
            // assign length in order to pick.
            optional_questions.length = 10;

            required_questions = required_questions.concat(
                optional_questions);
        }

        // reshuffle all questions together:
        required_questions.sort(randomly);

        var question_ids_as_loaded = map(function(a) {
            return parseInt(a.id.split('_')[1]);
        },  $$('.cases.really'));

        var order = map(function(a) {
            return findValue(question_ids_as_loaded, a);
        }, required_questions);
        return order;
    } else {
        return list(range($$('.cases.really').length)).sort(randomly);
    }
}

function reorder_questions(order) {
    var nums = list(range(order.length));

    //create placeholders for the sorted questions
    $('sorted_questions').appendChild(DIV({id: 'sorted_questions_div'},
        map(DIV, nums)));

    var existing_case_divs = $$('.cases.really');

    // source_divs is a new ordering of the existing, currently hidden divs.
    var source_divs = map(function(a) {
        return existing_case_divs[a];
    }, order);

    //destination_divs is a bunch of empty placeholder divs:
    var destination_divs = $('sorted_questions_div').childNodes;

    // swap the questions and the placeholders:
    map(function f(a) {
        swapDOM(a[0], a[1]);
    }, zip(destination_divs, source_divs));

    // show the resulting sorted divs, leaving the un-chosen
    // ones hidden as per the CSS file.
    map(function f(a) {
        setStyle(a, {'display': 'block'});
    }, $$('#sorted_questions_div div.cases'));

    // number the questions according to their new position:
    /* eslint-disable no-unsafe-innerhtml/no-unsafe-innerhtml */
    map(function f(a) {
        a[0].innerHTML = a[1] + 1;
    }, zip($$('#sorted_questions_div .question_order'), nums));
    /* eslint-enable no-unsafe-innerhtml/no-unsafe-innerhtml */
}

function cheat()  {
    var right_answers = filter(function f(a) {
        return getNodeAttribute(a, 'right_answer') === 'True';
    },  $$('#sorted_questions_div .question'));
    forEach(right_answers, function f(a)  {
        a.checked = true;
    });
}

function debug(string) {
    log('DEBUG ' + string);
}

function show_score() {
    // all visible answers:
    var all_answers = $$('#sorted_questions_div input.question');
    var quiz_key =  'quiz_' + $('quiz_id').value;

    // all chosen answers:
    var chosen_answers = filter(function f(a) {
        return a.checked;
    }, all_answers);

    var number_of_questions_to_answer = $$('#sorted_questions_div .cases')
        .length;

    // show all the correct answers:
    map(showElement, $$('.answer'));
    hideElement('show_score');
    var max_score = chosen_answers.length;
    var actual_score = filter(function f(a) {
        return getNodeAttribute(a, 'right_answer') === 'True';
    }, chosen_answers).length;

    if (actual_score === max_score) {
        hide_retake = true;
        // used in the final quiz to determine whether
        // you can advance to the next page.
    }

    var make_these_green = filter(function f(a) {
        return getNodeAttribute(a, 'right_answer') === 'True';
    }, $$('.question'));

    forEach(make_these_green, function(a) {
        addElementClass(a.parentNode, 'correct_answer');
    });

    /* eslint-disable no-unsafe-innerhtml/no-unsafe-innerhtml */
    if (max_score > 1) {
        $('quiz_score').innerHTML = actual_score;
        $('quiz_max_score').innerHTML = max_score;
        showElement('show_quiz_results');
    }
    /* eslint-enable no-unsafe-innerhtml/no-unsafe-innerhtml */

    // store the first score; for diagnostic tests that
    // might be taken several times:
    if (typeof(all_quizzes_info[quiz_key]) === 'undefined') {
        all_quizzes_info [quiz_key] = {};
    }
    if (typeof(all_quizzes_info[quiz_key][initialScoreKey])
            === 'undefined') {
        logDebug('Initial score not found; saving:');
        all_quizzes_info [quiz_key][initialScoreKey] = {
            'quiz_score': actual_score,
            'quiz_max_score': max_score,
            // store the answers:
            'answers_given': collect_question_info()
        };
    }

    if (actual_score > 0 && actual_score === max_score) {
        all_quizzes_info [quiz_key][allCorrectKey] = 't';
        // You got all the answers right; no need to retake the test.
        hideElement('retake_quiz_div');
    } else {
        all_quizzes_info [quiz_key][allCorrectKey] = 'f';
    }

    if (!pre_test) {
        if (!hide_retake)  {
            showElement('retake_quiz_div');
        } else {
            // set this to true to indicate that the training is complete.
            all_quizzes_info [quiz_key][allCorrectKey] = 't';
        }
    }
    var submitTimeKey = 'submit_time';
    /// adding this:
    if (typeof(all_quizzes_info [quiz_key][submitTimeKey])
            === 'undefined') {
        all_quizzes_info [quiz_key][submitTimeKey] = [Date()];
    } else {
        all_quizzes_info [quiz_key][submitTimeKey].push(Date());
    }

    if (post_test && (!hide_retake)) {
        alert(
            'You must score 100% on the post-test to receive credit ' +
            'for this training. Please click "Retake Quiz" and try again. ');
    }

    freeze_buttons();
}

function loadStateError() {
    debug('loadStateError');
    // @todo: Find a spot to display an error or decide
    // just to fail gracefully
}

function loadState() {
    debug('loadState');
    if (typeof student_quiz !== 'undefined') {
        hide_retake = true; // do not show to faculty
        loadStateSuccess(student_quiz);
        return;
    }

    var url = '/activity/quiz/load/';
    var deferred = loadJSONDoc(url);
    deferred.addCallbacks(loadStateSuccess, loadStateError);
}

function collect_question_info() {
    var question_info = [];
    forEach(getElementsByTagAndClassName('*', 'question'),
        function(question) {
            if (question.checked) {
                var a = question.id.split('_');
                var q = {};
                q.id = a[0];
                q.answer = a[1];
                question_info.push(q);
            }
        });
    return question_info;
}

function onSaveStateComplete() {
    removeElementClass(document.body, 'busy');
    maybeEnableNext();
    document.body.scrollTop = document.documentElement.scrollTop = 0;

    if (kill_this_quiz_flag) {
        window.location.reload();
    }
}

function onSaveStateFailed() {
    removeElementClass(document.body, 'busy');
    alert('An error occurred while saving your results. ' +
          'Please refresh the page and try again.');
}

function saveState(validate) {
    if (typeof student_response !== 'undefined') {
        return;
    }

    var what_to_send = all_quizzes_info;
    var url = '/activity/quiz/save/';
    var quiz_key =  'quiz_' + $('quiz_id').value;

    var all_answers = $$('#sorted_questions_div input.question');
    var chosen_answers = filter(function f(a) {
        return a.checked;
    }, all_answers);
    var number_of_questions_to_answer = $$('#sorted_questions_div .cases')
        .length;

    if (validate) {
        if (chosen_answers.length < number_of_questions_to_answer) {
            alert('Please answer all the questions.');
            return;
        }
        if (!confirm('Are you done?')) {
            return;
        }

        show_score();
    }

    // don't delete initial score:
    var initial_score_found = null;

    if (all_quizzes_info !== undefined &&
       all_quizzes_info [quiz_key] !== undefined &&
       all_quizzes_info [quiz_key][initialScoreKey] !== undefined) {
        initial_score_found = all_quizzes_info [quiz_key][initialScoreKey];
    }

    if (show_initial_score(all_quizzes_info [quiz_key], quiz_key)) {
        // do not overwrite state with the displayed initial answers:
        what_to_send [quiz_key].question = collect_question_info();

        // keep everything as is and save.
    } else {
        if (kill_this_quiz_flag) {
            logDebug('Do save the initial results, but delete all ' +
                     'question and answer info.');
            delete what_to_send[quiz_key].question;
        } else {
            if (what_to_send [quiz_key] !== undefined) {
                logDebug('Deleting all info for quiz, so it can be ' +
                         'replaced with the quiz you just took.');
                delete what_to_send[quiz_key].question;
            } else {
                logDebug('No info found on this quiz.');
                what_to_send[quiz_key] = {};
            }
            if (initial_score_found !== null) {
                logDebug('Found an initial score, so preserving it.');
                what_to_send[quiz_key][initialScoreKey] =
                    initial_score_found;
            }
            what_to_send[quiz_key].question = collect_question_info();
        }
    }

    addElementClass(document.body, 'busy');
    var deferred = MochiKit.Async.doXHR(
        url,
        {
            'method': 'POST',
            'sendContent': queryString({
                'json': serializeJSON(what_to_send)}),
            'headers': {'Content-Type': 'application/x-www-form-urlencoded'}
        });
    deferred.addCallback(onSaveStateComplete);
    deferred.addErrback(onSaveStateFailed);
}

function retakeQuiz() {
    if (!confirm('Are you sure you want to start the quiz again? ' +
                 'This will erase your answers.'))  {
        return;
    }
    kill_this_quiz_flag = true;
    saveState(false);
}

// eslint-disable-next-line scanjs-rules/call_connect
MochiKit.Signal.connect(window, 'onload', loadState);

