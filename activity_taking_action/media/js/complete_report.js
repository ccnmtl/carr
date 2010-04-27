if (typeof(steps) == "undefined") {
    steps = {}
}
step_name = 'complete_report';
next_step = 'case_summary';

steps[step_name] = {
    'load': partial (new_load, step_name, next_step)
}
