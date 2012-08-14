



function set_up_all_form_fields () {

    
    // Get all the fields on the Nice Work page:
    new_form_fields_top =    $$ ('#complete_report_top_of_form    .ldss_form_input')
    new_form_fields_middle = $$ ('#complete_report_middle_of_form .ldss_form_input')
    new_form_fields_bottom = $$ ('#complete_report_bottom_of_form .ldss_form_input')

    forEach (new_form_fields_top,    set_up_form_field );
    forEach (new_form_fields_middle, set_up_form_field );
    forEach (new_form_fields_bottom, set_up_form_field );
    

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
    
    //console.log (field.classList);
    disconnectAll(field); // in case this gets called more than once.
    
    css_classes = the_classlist (field);
    
    editable_version = $$('.form_fields_are_editable '     + css_classes)[0];
    not_editable_version  = $$('.form_fields_are_not_editable ' + css_classes)[0];

    reporting_form_editable_textfield_connect (editable_version);
    
    // make the not editable version read-only:
    setNodeAttribute(not_editable_version, "readonly", "readonly");
    
    
    // load and display values from game state if they exist:
    if (game_state [css_classes] != undefined) {
        editable_version.value = game_state [css_classes];
        not_editable_version.value   = game_state [css_classes];
    }
    
    //connect (editable_version, 
    
    //console.log ('ok now');
    //console.log ($$('#complete_report_nice_work ' + the_classlist_1)[0])
    
}

function reporting_form_editable_textfield_connect (f) {
    // console.log ('connecting' + f);
    connect (f, 'onchange', reporting_form_editable_textfield_changed);
}

function reporting_form_editable_textfield_changed(e) {
    contents = e.src().value;
    //console.log (contents);
    //console.log (the_classlist(e.src()));
    
    
    css_classes = the_classlist (e.src());
    not_editable_version  = $$('.form_fields_are_not_editable ' + css_classes)[0];
    
    // set the non-editable fields on the "Nice Work" page to reflect the contents.
    not_editable_version.value = contents;
    
    //map (partial (set_contents, contents), $$('.other_observations'));
    //   do other fun stuff with e.src() e.g. save the state of the app.
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
    }
}
