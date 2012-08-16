



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
    // isn't there a better way of doing this?
    result = '';
    for (var i = 0; i < el.classList.length; i++) {
        //console.log ( el.classList[i])
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


steps['complete_report_overview'] = {
    'load': function () {
        new_load ('complete_report_overview', 'complete_report_top_of_form');
        
    }
}

steps['complete_report_top_of_form'] = {
    'load': function () {
        new_load ('complete_report_top_of_form', 'complete_report_middle_of_form');
        set_up_all_form_fields();
    }
}

steps['complete_report_middle_of_form'] = {
    'load': function () {
        new_load ('complete_report_middle_of_form', 'complete_report_bottom_of_form');
    }
}

steps['complete_report_bottom_of_form'] = {
    'load': function () {
        new_load ('complete_report_bottom_of_form', 'complete_report_nice_work');
    }
}

steps['complete_report_nice_work'] = {
    'load': function () {
        new_load ('complete_report_nice_work', 'complete_report_expert');
    }
}

steps['complete_report_expert'] = {
    'load': function () {
        new_load ('complete_report_expert', 'case_summary');
        connect  ('back_to_my_version_button', 'onclick', go_back_to_my_version);
    }
}



    
function go_back_to_my_version () {
    load_step ('complete_report_nice_work');
}

