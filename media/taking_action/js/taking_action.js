/* global steps: true, game_state: true, nav_ready: true */
/* global removeElementClass: true, connect: true, keys: true */
/* global disconnectAll: true, setNodeAttribute: true, array_of_steps: true */
/* global findChildElements: true, partial: true */
/* global which_of_these_css_classes: true */
/* global first_round_action_css_classes: true */
/* global second_round_action_css_classes: true */
/* global observation_checkbox_connect: true */
/* global criteria_checkbox_connect: true */
/* global other_observations_textfield_connect: true */

var current_step;
var step_to_show_first;
var student_response;

function maybeEnableNext() {
    setStyle('next', {
        'display': 'inline'
    });
    showElement($('conclusion'));
    hideElement($('span_conclusion'));
}

function validate() {
    // we have stored form info for this user:
    if (filter(function(a) {
        return a.substring(0, 16) === '.ldss_form_input';
    }, keys(game_state)).length > 0) {
        return true;
    }
    // OR the user has typed info into the form although it's not yet stored:
    if (filter(function(a) {
        return (a.value.trim() !== '');
    }, $$('.form_fields_are_editable .ldss_form_input')).length > 0) {
        return true;
    }
    return false;
}

function loadStateSuccess(doc) {
    init_taking_action();
    game_state = doc;

    if (game_state.current_step === undefined) {
        current_step = step_to_show_first;
    } else {
        current_step = game_state.current_step;
    }
    load_step(current_step);
}

function loadStateError(err) {
    // @todo: Find a spot to display an error or decide just to fail gracefully
    // $('errorMsg').innerHTML = 'An error occurred loading your state (' + err
    // + '). Please start again.'
}

function loadState() {
    if (typeof student_response !== 'undefined') {
        game_state = student_response;
        current_step = 'complete_report';
        load_step('complete_report');
        return;
    }
    var url = '/activity/taking_action/load/';
    var deferred = loadJSONDoc(url);
    deferred.addCallbacks(loadStateSuccess, loadStateError);

    maybeEnableNext();
}

function like_checkbox(selected_class, all_button_class, the_element) {
    map(function(a) {
        removeElementClass(a, selected_class);
    }, $$('.' + all_button_class));
    addElementClass($(the_element), selected_class);
}

function show_answer() {
    maybeEnableNext();
}

MochiKit.Signal.connect(window, 'onload', loadState);

function new_ldss_form_fields_to_save() {
    var results = {};
    var filled_out_fields = filter(function(a) {
        return a.value !== '';
    }, $$('.form_fields_are_editable .ldss_form_input'));
    map(function(a) {
        results[the_classlist(a)] = a.value;
    }, filled_out_fields);
    return results;
}

function deprecated_ldss_form_fields_to_save() {
    var results = {};
    var filled_out_fields = filter(function(a) {
        return a.innerHTML !== '';
    }, $$('.magic_form'));

    map(function(a) {
        results[a.id] = a.innerHTML;
    }, filled_out_fields);
    return results;
}

function saveState(nextStep) {
    if (typeof student_response !== 'undefined') {
        return;
    }
    var url = '/activity/taking_action/save/';

    var doc = new_ldss_form_fields_to_save();

    if (validate()) {
        doc.complete = 'true';
    }

    doc.current_step = current_step;

    addElementClass(document.body, 'busy');
    var deferred = MochiKit.Async.doXHR(
        url,
        {
            'method': 'POST',
            'sendContent': queryString({'json': JSON.stringify(doc, null)}),
            'headers': {'Content-Type': 'application/x-www-form-urlencoded'}
        });
    deferred.addCallback(function() {
        removeElementClass(document.body, 'busy');
        load_step(nextStep);
    });
    deferred.addErrback(function() {
        removeElementClass(document.body, 'busy');
        alert('An error occurred while saving your results. ' +
              'Please refresh the page and try again.');
    });
}

function set_up_all_form_fields() {
    // Get all the fields on the Nice Work page:
    var new_form_fields_top =
        $$('#complete_report_top_of_form .ldss_form_input');
    var new_form_fields_middle =
        $$('#complete_report_middle_of_form .ldss_form_input');
    var new_form_fields_bottom =
        $$('#complete_report_bottom_of_form .ldss_form_input');

    forEach(new_form_fields_top, set_up_form_field);
    forEach(new_form_fields_middle, set_up_form_field);
    forEach(new_form_fields_bottom, set_up_form_field);

    // For faculty reviewing student response to form:
    var student_response_form_fields =
        $$('#student_response_form .ldss_form_input');
    forEach(student_response_form_fields, set_up_form_field);
}

function nice_work_set_up_toggle() {
    connect('print_version_on', 'onclick', set_print_version_on);
    connect('print_version_off', 'onclick', set_print_version_off);
    set_print_version_off();
}

function set_print_version_on() {
    showElement('print_version_off');
    hideElement('print_version_on');
    hideElement('sidebar_left');
    hideElement('header');
    hideElement('subnav');
    hideElement($$('h2')[0]);
    hideElement('nice_work_blurb');
    hideElement($$('.content-nav')[0]);

    hideElement(
        $$('#complete_report_nice_work .taking_action_prev_button')[0]);
    hideElement(
        $$('#complete_report_nice_work .taking_action_next_button')[0]);
    hideElement(
        $$('#complete_report_nice_work .taking_action_pagenumber')[0]);
}

function set_print_version_off() {
    hideElement('print_version_off');
    showElement('print_version_on');
    showElement('sidebar_left');
    showElement('header');
    showElement('subnav');
    showElement($$('h2')[0]);
    showElement('nice_work_blurb');
    showElement($$('.content-nav')[0]);

    showElement(
        $$('#complete_report_nice_work .taking_action_prev_button')[0]);
    showElement(
        $$('#complete_report_nice_work .taking_action_next_button')[0]);
    showElement(
        $$('#complete_report_nice_work .taking_action_pagenumber')[0]);
}

function the_classlist(el) {
    var result = '';
    for (var i = 0; i < el.classList.length; i++) {
        result = result + '.' + el.classList[i];
    }
    return result;
}

function set_up_form_field(field) {
    // on change, update the state and set the content on the Nice Work page to
    // its content.

    if (field === undefined) {
        return;
    }
    disconnectAll(field); // in case this gets called more than once.
    var css_classes = the_classlist(field);
    var editable_version = $$('.form_fields_are_editable ' + css_classes)[0];
    var not_editable_version =
        $$('.form_fields_are_not_editable ' + css_classes)[0];

    // load and display values from game state if they exist:
    if (editable_version !== undefined) {
        reporting_form_editable_textfield_connect(editable_version);
        if (game_state[css_classes] !== undefined) {
            editable_version.value = game_state[css_classes];
        }
    }
    if (not_editable_version !== undefined) {
        if (game_state[css_classes] !== undefined) {
            not_editable_version.value = game_state[css_classes];
        }
    }

    // make the non-editable version read-only:
    setNodeAttribute(not_editable_version, 'readonly', 'readonly');
}

function reporting_form_editable_textfield_connect(f) {
    connect(f, 'onchange', reporting_form_editable_textfield_changed);
}

function reporting_form_editable_textfield_changed(e) {
    var contents = e.src().value;
    var css_classes = the_classlist(e.src());
    var not_editable_version =
        $$('.form_fields_are_not_editable ' + css_classes)[0];

    // set the non-editable fields on the 'Nice Work' page to reflect the new
    // contents.
    not_editable_version.value = contents;
}

function load_step(step_name) {
    // Save the current step name.
    current_step = step_name;

    map(hideElement, $$('.activity_step'));

    showElement($$('div#' + step_name + '.activity_step')[0]);
    if (steps[step_name] !== undefined) {
        steps[step_name].load();
    }
    maybeEnableNext();
    if (!nav_ready) {
        // this shouldn't run every time you change stpes.
        // it chould change when you load the page.
        forEach(list(range(array_of_steps.length)), function(a) {
            set_up_nav(array_of_steps, a);
        });
        nav_ready = true;
    }
    if (current_step !== 'case_summary') {
        // per bug # 83956:
        // hide the next button except on the last page.
        hideElement($('next'));
    }
}

function set_up_nav(array_of_steps, step_number) {
    // this is run on page load, but not on step load.
    var prev_step = step_name;
    var next_step = step_name;
    var step_name = array_of_steps[step_number];
    if (step_number > 0) {
        prev_step = array_of_steps[step_number - 1];
    }
    if (step_number <= array_of_steps.length) {
        next_step = array_of_steps[step_number + 1];
    }

    var prev_button = findChildElements($(step_name),
        ['.taking_action_prev_button'])[0];
    if (prev_button !== undefined) {
        connect(prev_button, 'onclick', partial(load_step, prev_step));
    }

    var next_button = findChildElements($(step_name),
        ['.taking_action_next_button'])[0];
    if (next_button !== undefined) {
        connect(next_button, 'onclick', partial(saveState, next_step));
    }
}

function connect_action(c) {
    connect(c, 'onclick', action_button_clicked);
}

function action_button_clicked(c) {
    var which_class = which_of_these_css_classes(c.src(),
            first_round_action_css_classes);

    if (which_class === 'first_round_action_1') {
        showElement(
            $$('.choose_action.action_explanation.first_round_action_1')[0]);
    } else if (which_class === 'first_round_action_2') {
        showElement(
            $$('.choose_action.action_explanation.first_round_action_2')[0]);
    } else if (which_class === 'first_round_action_3') {
        showElement(
            $$('.choose_action.action_explanation.first_round_action_3')[0]);
    } else if (which_class === 'first_round_action_4') {
        showElement(
            $$('.choose_action.action_explanation.first_round_action_4')[0]);
    }
}

function connect_action_round_2(c) {
    connect(c, 'onclick', action_button_clicked_round_2);
}

function action_button_clicked_round_2(c) {
    var which_class = which_of_these_css_classes(c.src(),
            second_round_action_css_classes);
    if (which_class === 'second_round_action_1') {
        showElement($$('.action_explanation.second_round_action_1')[0]);
    } else if (which_class === 'second_round_action_2') {
        showElement($$('.action_explanation.second_round_action_2')[0]);
    } else if (which_class === 'second_round_action_3') {
        showElement($$('.action_explanation.second_round_action_3')[0]);
    } else if (which_class === 'second_round_action_4') {
        showElement($$('.action_explanation.second_round_action_4')[0]);
    }
}

function init_taking_action() {
    step_to_show_first = array_of_steps[0];
    var default_load = {
        'load': function() {
        }
    };
    forEach(array_of_steps, function(a) {
        steps[a] = default_load;
    });
    steps.review_case_history = {
        'load': function() {
            map(observation_checkbox_connect, $$('.checkbox.observation'));
            map(criteria_checkbox_connect, $$('.checkbox.criteria'));
            map(other_observations_textfield_connect,
                $$('.other_observations'));
        }
    };
    steps.choose_action = {
        'load': function() {
            map(connect_action, $$('.first_round_action'));
        }
    };

    var complete_report_load = {
        'load': function() {
            set_up_all_form_fields();
            nice_work_set_up_toggle();
        }
    };

    steps.complete_report_top_of_form = complete_report_load;
    steps.complete_report_middle_of_form = complete_report_load;
    steps.complete_report_bottom_of_form = complete_report_load;
    steps.complete_report_nice_work = complete_report_load;

    steps.next_steps = {
        'load': function() {
            map(connect_action_round_2, $$('.second_round_action'));
        }
    };
}
