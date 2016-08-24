/* global hasElementClass: true, addElementClass: true, connect: true */
/* global student_response: true, partial: true, removeElementClass: true */
/* global toggleElementClass: true, disconnectAll: true */

function validate() {
    // make sure either yes or no is selected.
    return (hasElementClass($('answer_yes'), 'button_selected') ||
            hasElementClass($('answer_no'), 'button_selected'));
}

function maybeEnableNext() {
    var gonext = false;

    if (validate()) {
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

function disable_all_sidenav_items_after_current_one() {
    var all_sidenav_items = $$('#sidebar_left ul li');
    var selected_sidenav_item = $$('#sidebar_left ul li.selected')[0];
    all_sidenav_items
            .slice(all_sidenav_items.indexOf(selected_sidenav_item) + 1);
    var sidenav_items_to_disable = all_sidenav_items.slice(all_sidenav_items
            .indexOf(selected_sidenav_item) + 1);
    forEach(sidenav_items_to_disable, disable_sidenav_item);
}

function disable_sidenav_item(item) {
    forEach(getElementsByTagAndClassName('a', null, item), hideElement);
    forEach(getElementsByTagAndClassName('span', null, item), showElement);
}

function loadStateSuccess(doc) {
    // NOTE: Correct answers for these, including correct button ID's,
    // are in the database and editable via django admin.
    // See: /admin/activity_bruise_recon/case/
    var case_name = $('case_name').innerHTML.trim();
    var state_for_this_page;

    if (doc && doc[case_name]) {
        state_for_this_page = doc[case_name];
        // if state is already saved you can't change your answers.
        if (typeof (state_for_this_page.answered) !== 'undefined') {
            lock_down_answer_buttons();
        }
    } else {
        state_for_this_page = {};
    }
    if (state_for_this_page.answered) {
        if (state_for_this_page.answered === 'yes') {
            addElementClass($('answer_yes'), 'button_selected');
        } else if (state_for_this_page.answered === 'no') {
            addElementClass($('answer_no'), 'button_selected');
        }
    }

    var factors_as_string = 'undefined';
    if (state_for_this_page.factors) {
        factors_as_string = state_for_this_page.factors.join(',');
    }
    if (typeof (factors_as_string) !== 'undefined') {
        if (factors_as_string.match(/patterns/) !== null) {
            addElementClass($('patterns'), 'button_selected');
        }
        if (factors_as_string.match(/severity/) !== null) {
            addElementClass($('severity'), 'button_selected');
        }
        if (factors_as_string.match(/body location/) !== null) {
            addElementClass($('body location'), 'button_selected');
        }
        if (factors_as_string.match(/explanation/) !== null) {
            addElementClass($('explanation'), 'button_selected');
        }
    }
    // adding this: show correct answer for completed quizzes.
    if (validate()) {
        show_answer();
    }
    maybeEnableNext();
}

function loadStateError(err) {
    // @todo: Find a spot to display an error or decide just to fail gracefully
    // $('errorMsg').innerHTML = 'An error occurred loading your state (' + err
    // + '). Please start again.'
}

function loadState() {
    if (typeof student_response !== 'undefined') {
        loadStateSuccess(student_response);
        if (validate()) {
            show_answer();
        }
        return;
    }

    var url = '/activity/bruise_recon/load/';
    var deferred = loadJSONDoc(url);
    deferred.addCallbacks(loadStateSuccess, loadStateError);

    hide_answer();

    // yes/no behaves like a set of radio buttons
    connect('answer_yes', 'onclick', partial(like_radio, 'button_selected',
            'answer_button', 'answer_yes'));
    connect('answer_no', 'onclick', partial(like_radio, 'button_selected',
            'answer_button', 'answer_no'));

    // factors behaves like a set of checkboxes.
    connect('patterns', 'onclick', partial(like_checkbox, 'button_selected',
            'bruise_recon_checkbox_div', 'patterns'));
    connect('severity', 'onclick', partial(like_checkbox, 'button_selected',
            'bruise_recon_checkbox_div', 'severity'));
    connect('body location', 'onclick', partial(like_checkbox,
            'button_selected', 'bruise_recon_checkbox_div', 'body location'));
    connect('explanation', 'onclick', partial(like_checkbox, 'button_selected',
            'bruise_recon_checkbox_div', 'explanation'));

    connect('submit_div', 'onclick', saveState);

    maybeEnableNext();

}

function like_radio(selected_class, all_button_class, the_element) {
    map(function(a) {
        removeElementClass(a, selected_class);
    }, $$('.' + all_button_class));
    addElementClass($(the_element), selected_class);
}

function like_checkbox(selected_class, all_button_class, the_element) {
    toggleElementClass(selected_class, $(the_element));
}

function lock_down_answer_buttons() {
    forEach($$('.answer_button'), disconnectAll);
    forEach($$('.bruise_recon_checkbox_div'), disconnectAll);
    forEach($$('#submit_div'), disconnectAll);
}

function hide_answer() {
    hideElement('feedback_div');
}

function numeric(field) {
    var regExpr = new RegExp('^[0-9]$');
    if (!regExpr.test(field.value)) {
        // Case of error
        field.value = '';
    }
}

function answer_is_correct() {

    var answer_is_yes = $('correct_answer').innerHTML
        .toLowerCase().match(/yes/);

    var factors_include_severity = ($('correct_factors').innerHTML
        .toLowerCase().match(/severity/)) !== null;
    var factors_include_location = ($('correct_factors').innerHTML
        .toLowerCase().match(/body location/)) !== null;
    var factors_include_patterns = ($('correct_factors').innerHTML
        .toLowerCase().match(/patterns/)) !== null;
    var factors_include_explanation = ($('correct_factors').innerHTML
        .toLowerCase().match(/explanation/)) !== null;

    var answer_includes_severity = hasElementClass($('severity'),
        'button_selected');
    var answer_includes_location = hasElementClass($('body location'),
        'button_selected');
    var answer_includes_patterns = hasElementClass($('patterns'),
        'button_selected');
    var answer_includes_explanation = hasElementClass($('explanation'),
        'button_selected');

    if (answer_is_yes) {
        if (hasElementClass($('answer_no'), 'button_selected')) {
            return false;
        }
    } else {
        if (hasElementClass($('answer_yes'), 'button_selected')) {
            return false;
        }
    }

    if (factors_include_severity !== answer_includes_severity) {
        return false;
    }

    if (factors_include_location !== answer_includes_location) {
        return false;
    }

    if (factors_include_patterns !== answer_includes_patterns) {
        return false;
    }

    if (factors_include_explanation !== answer_includes_explanation) {
        return false;
    }
    return true;

}

function show_answer() {
    if (!validate()) {
        alert('Please choose yes or no.');
        return;
    }
    hideElement('submit_div');
    if (answer_is_correct()) {
        $('your_answer_was').innerHTML = 'Your answers are correct';
        addElementClass($('your_answer_was'), 'alert-success');
    } else {
        $('your_answer_was').innerHTML = 'Your answers are incorrect';
        addElementClass($('your_answer_was'), 'alert-danger');

    }
    showElement('your_answer_was');
    showElement('feedback_div');
    lock_down_answer_buttons();
}

MochiKit.Signal.connect(window, 'onload', loadState);

function onSaveStateComplete() {
    removeElementClass(document.body, 'busy');
    maybeEnableNext();
}

function onSaveStateFailed() {
    removeElementClass(document.body, 'busy');
    alert('An error occurred while saving your results. ' +
          'Please refresh the page and try again.');
}

function saveState() {
    if (typeof student_response !== 'undefined') {
        return;
    }

    show_answer();

    var case_name = $('case_name').innerHTML.trim();

    var url = '/activity/bruise_recon/save/';

    var doc = {};

    if (hasElementClass($('answer_yes'), 'button_selected')) {
        doc.answered = 'yes';
    }

    if (hasElementClass($('answer_no'), 'button_selected')) {
        doc.answered = 'no';
    }

    doc.factors = [];
    if (hasElementClass($('severity'), 'button_selected')) {
        doc.factors.push('severity');
    }

    if (hasElementClass($('body location'), 'button_selected')) {
        doc.factors.push('body location');
    }

    if (hasElementClass($('patterns'), 'button_selected')) {
        doc.factors.push('patterns');
    }

    if (hasElementClass($('explanation'), 'button_selected')) {
        doc.factors.push('explanation');
    }

    if (answer_is_correct()) {
        doc.score = 1;
    } else {
        doc.score = 0;
    }

    var what_to_send = {};
    what_to_send[case_name] = doc;

    addElementClass(document.body, 'busy');
    var deferred = MochiKit.Async.doXHR(
        url,
        {'method': 'POST',
         'sendContent': queryString({'json': serializeJSON(what_to_send)}),
         'headers': {'Content-Type': 'application/x-www-form-urlencoded'}
        });
    deferred.addCallback(onSaveStateComplete);
    deferred.addErrback(onSaveStateFailed);
}

