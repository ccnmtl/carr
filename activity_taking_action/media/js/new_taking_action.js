function set_up_all_form_fields () {
    // Get all the fields on the Nice Work page:
    new_form_fields_top =    $$ ('#complete_report_top_of_form    .ldss_form_input')
    new_form_fields_middle = $$ ('#complete_report_middle_of_form .ldss_form_input')
    new_form_fields_bottom = $$ ('#complete_report_bottom_of_form .ldss_form_input')

    forEach (new_form_fields_top,    set_up_form_field );
    forEach (new_form_fields_middle, set_up_form_field );
    forEach (new_form_fields_bottom, set_up_form_field );
    
    // For faculty reviewing student response to form:
    student_response_form_fields = $$('#student_response_form .ldss_form_input');
    forEach (student_response_form_fields, set_up_form_field );
}

function the_classlist (el) {
    result = '';
    for (var i = 0; i < el.classList.length; i++) {
        result = result + '.' + el.classList[i]
    }
    return result;
}


function set_up_form_field ( field) {
    // on change,  update the state and set the content on the Nice Work page to its content.
    
    if (field == undefined ) {
        return;
    }
    disconnectAll(field); // in case this gets called more than once.
    css_classes = the_classlist (field);
    editable_version = $$('.form_fields_are_editable '     + css_classes)[0];
    not_editable_version  = $$('.form_fields_are_not_editable ' + css_classes)[0];

    // load and display values from game state if they exist:
    if (editable_version != undefined ) {
        reporting_form_editable_textfield_connect (editable_version);
        if (game_state [css_classes] != undefined) {
            editable_version.value = game_state [css_classes];
        }
    }
    if (not_editable_version != undefined ) {
        if (game_state [css_classes] != undefined) {
            not_editable_version.value   = game_state [css_classes];
        }
    }
    
    // make the non-editable version read-only:
    setNodeAttribute(not_editable_version, "readonly", "readonly");
}

function reporting_form_editable_textfield_connect (f) {
    connect (f, 'onchange', reporting_form_editable_textfield_changed);
}

function reporting_form_editable_textfield_changed(e) {
    
    contents = e.src().value;
    css_classes = the_classlist (e.src());
    not_editable_version  = $$('.form_fields_are_not_editable ' + css_classes)[0];
    
    // set the non-editable fields on the "Nice Work" page to reflect the new contents.
    console.log ('css_classes');
    console.log (contents);
    not_editable_version.value = contents;
}

var array_of_steps =  [
    'review_case_history',
    'analyze_action_criteria',
    'choose_action',
    'next_steps',
    'complete_report_overview',
    'complete_report_top_of_form',
    'complete_report_middle_of_form',
    'complete_report_bottom_of_form',
    'complete_report_nice_work',
    'complete_report_expert'
];
/*
set_up_nav (array_of_steps, 0);
set_up_nav (array_of_steps, 1);
set_up_nav (array_of_steps, 2);
set_up_nav (array_of_steps, 3);
set_up_nav (array_of_steps, 4);
set_up_nav (array_of_steps, 5);
set_up_nav (array_of_steps, 6);
set_up_nav (array_of_steps, 7);
set_up_nav (array_of_steps, 8);
set_up_nav (array_of_steps, 9);
*/
var nav_ready= false;

function load_step (step_name) {
    console.log ("load step clicked");
    console.log (step_name);
    map (hideElement, $$('.activity_step'))
    showElement($$('div#' + step_name +  '.activity_step')[0] );
    if (steps[step_name] != undefined) {
        steps[step_name].load()
    }
    else {
        logDebug("not defined.");
    }
    maybeEnableNext();
    if (!nav_ready) {
        set_up_all_navs ();
    }
}

function set_up_all_navs () {
    set_up_nav (array_of_steps, 0);
    set_up_nav (array_of_steps, 1);
    set_up_nav (array_of_steps, 2);
    set_up_nav (array_of_steps, 3);
    set_up_nav (array_of_steps, 4);
    set_up_nav (array_of_steps, 5);
    set_up_nav (array_of_steps, 6);
    set_up_nav (array_of_steps, 7);
    set_up_nav (array_of_steps, 8);
    set_up_nav (array_of_steps, 9);
    nav_ready = true;
}

function set_up_nav (array_of_steps, step_number) {
    var prev_step = step_name;
    var next_step = step_name;
    
    console.log ("Setting up nav. Step number is:");
    console.log ("current " , step_number);
    //console.log (array_of_steps);
    
    var step_name = array_of_steps [step_number];
    //console.log ("step name is");
    console.log ("step name is ", step_name);
    
    //console.log (step_number);
    if (step_number >  0) {
        prev_step = array_of_steps [step_number - 1];
        console.log ("prev ", prev_step);
    }
    if (step_number < array_of_steps.length ) {
        next_step = array_of_steps [step_number + 1];
        console.log ("next ", next_step);
    }
    
    next_button = findChildElements($(step_name), [".taking_action_next_button"])[0]
    if (next_button != undefined) {
        connect (next_button, 'onclick', partial(load_step, next_step ));
    }
    else {
        console.log('not found');
    }
    
    prev_button = findChildElements($(step_name), [".taking_action_prev_button"])[0]
    //console.log( prev_button)
    if (prev_button != undefined) {
        connect (prev_button, 'onclick', partial(load_step, prev_step ));
    } else {
        console.log('not found');
    }
    
}

function closure_thing (array_of_steps, the_number) {
    console.log ("creating a function with " + the_number);
    var result = function () {  return show_step (array_of_steps, the_number);}
    return result;
}

/*********/
steps['review_case_history'] = {
     
    'load': function () {
        map (observation_checkbox_connect,         $$('.checkbox.observation'));
        map (criteria_checkbox_connect,            $$('.checkbox.criteria'   ));
        map (other_observations_textfield_connect, $$('.other_observations'  ));
    }
}

/*********/

steps['analyze_action_criteria'] = {
    'load': function () {
    }
}

/*********/

steps['choose_action'] = {
    'load': function () {
        map (connect_action,  $$('.first_round_action'));
        }
}

function connect_action (c) {
    connect(c,  'onclick', action_button_clicked);
}

function action_button_clicked(c) {
    which_class = which_of_these_css_classes(c.src(), first_round_action_css_classes);
    logDebug (which_class);
    if (which_class == 'first_round_action_1') {
        showElement ($$('.choose_action.action_explanation.first_round_action_1')[0]);
    } else if (which_class == 'first_round_action_2') {
        showElement ($$('.choose_action.action_explanation.first_round_action_2')[0]); 
    } else if (which_class == 'first_round_action_3') {
        showElement ($$('.choose_action.action_explanation.first_round_action_3')[0]); 
    } else if (which_class == 'first_round_action_4') {
        showElement ($$('.choose_action.action_explanation.first_round_action_4')[0]); 
    }
}

/*********/



//var goat = closure_thing (array_of_steps, the_number); // goat is a function

steps['next_steps'] = {
    'load': function () {
        
        map (connect_action_round_2,  $$('.second_round_action'));
        
    }
}

function connect_action_round_2 (c) {
    connect(c,  'onclick', action_button_clicked_round_2);
}

function action_button_clicked_round_2(c) {
    which_class = which_of_these_css_classes(c.src(), second_round_action_css_classes);
    if (       which_class == 'second_round_action_1') {
        showElement($$('.action_explanation.second_round_action_1')[0]);
    } else if (which_class == 'second_round_action_2') {
        showElement($$('.action_explanation.second_round_action_2')[0]);
    } else if (which_class == 'second_round_action_3') {
        showElement($$('.action_explanation.second_round_action_3')[0]);
    } else if (which_class == 'second_round_action_4') {
        showElement($$('.action_explanation.second_round_action_4')[0]);
    }
}
/*

*/
/*********/


steps['complete_report_overview'] = {
    'load': function () {
    }
}

/*********/


steps['complete_report_top_of_form'] = {
    'load': function () {
        set_up_all_form_fields();
    }
}

/*********/


steps['complete_report_middle_of_form'] = {
    'load': function () {
        set_up_nav (array_of_steps, the_number);
    }
}

/*********/

steps['complete_report_bottom_of_form'] = {
    'load': function () {
    }
}

/*********/


steps['complete_report_nice_work'] = {
    'load': function () {
    }
}

/*********/


steps['complete_report_expert'] = {
    'load': function () {
    }
}

/*********/


steps['case_summary'] = {
    'load': function () {
    }
}

/*
set_up_nav (array_of_steps, 0);
set_up_nav (array_of_steps, 1);
set_up_nav (array_of_steps, 2);
set_up_nav (array_of_steps, 3);
set_up_nav (array_of_steps, 4);
set_up_nav (array_of_steps, 5);
set_up_nav (array_of_steps, 6);
set_up_nav (array_of_steps, 7);
set_up_nav (array_of_steps, 8);
set_up_nav (array_of_steps, 9);
*/
console.log ('done with new_');

