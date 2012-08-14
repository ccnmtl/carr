
steps['next_steps'] = {
    'load': function () {
        new_load ('next_steps', 'complete_report_overview');
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
