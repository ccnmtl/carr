if (typeof(steps) == "undefined") {
    steps = {}
}
steps ['choose_action'] =  {
    'load': function () {
        logDebug ("hi choose action");
        connect ('choose_action_next', 'onclick', partial(load_step,'action_feedback'));
    }
}


