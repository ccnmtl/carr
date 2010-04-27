if (typeof(steps) == "undefined") {
    steps = {}
}
step_name = 'choose_action';
next_step = 'next_steps';

steps[step_name] = {
    'load': partial (new_load, step_name, next_step)
}
