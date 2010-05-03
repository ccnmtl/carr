steps['review_case_history'] = {
    'load': function () {
        new_load ('review_case_history', 'analyze_action_criteria');
        map (observation_checkbox_connect, $$('.checkbox.observation'));
        map (criteria_checkbox_connect, $$('.checkbox.criteria'));
        map (other_observations_textfield_connect, $$('.other_observations'));
    }
}


//function check_or_uncheck (c


