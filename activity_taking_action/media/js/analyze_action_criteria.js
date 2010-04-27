if (typeof(steps) == "undefined") {
    steps = {}
}

step_name = 'analyze_action_criteria';
next_step = 'choose_action';


steps[step_name] = {
    'load': partial (new_load, step_name, next_step)
}
