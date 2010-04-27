if (typeof(steps) == "undefined") {
    steps = {}
}
steps ['review_case_history'] =  {
    'load': function () {
        logDebug ("hi case history");
        connect ('review_case_history_next', 'onclick', partial(load_step,'analyze_action_criteria'));
    }
    

}


