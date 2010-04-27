function new_load (step_name, next_step) {
        next_button = findChildElements($(step_name), [".taking_action_next_button"])[0]
        connect (next_button, 'onclick', partial(load_step,next_step));
}

