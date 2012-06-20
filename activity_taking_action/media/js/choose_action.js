steps['choose_action'] = {
    'load': function () {
        new_load ('choose_action', 'next_steps');
        map (connect_action,  $$('.first_round_action'));
        }
}

function connect_action (c) {
    connect(c,  'onclick', action_button_clicked);
}

function action_button_clicked(c) {
    logDebug (c.src());
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

