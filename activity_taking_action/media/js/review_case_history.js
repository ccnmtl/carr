if (typeof(steps) == "undefined") {
    steps = {}
}

step_name = 'review_case_history';
next_step = 'analyze_action_criteria';


steps[step_name] = {
    'load': partial (new_load, step_name, next_step)
}
