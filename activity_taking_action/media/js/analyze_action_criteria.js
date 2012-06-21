steps['analyze_action_criteria'] = {
    'load': function () {
        new_load ('analyze_action_criteria', 'choose_action');
        connect  ('review_case_button', 'onclick', review_case);
    }
}

    
function review_case () {
    load_step ('review_case_history')

}
