if (typeof(steps) == "undefined") {
    steps = {}
}
step_name = 'next_steps';
next_step = 'complete_report';

steps[step_name] = {
    'load': partial (new_load, step_name, next_step)
}
