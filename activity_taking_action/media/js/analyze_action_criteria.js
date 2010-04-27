if (typeof(steps) == "undefined") {
    steps = {}
}
steps ['analyze_action_criteria'] =  {
    'load': function () {
        logDebug ("hi analyze_action_criteria");
        //connect ('analyze_action_criteria_next', 'onclick', partial(load_step,'choose_action'));
    }
}


