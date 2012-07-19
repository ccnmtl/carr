
steps['complete_report_overview'] = {
    'load': function () {
        new_load ('complete_report_overview', 'complete_report_top_of_form');
    }
}

steps['complete_report_top_of_form'] = {
    'load': function () {
        new_load ('complete_report_top_of_form', 'complete_report_middle_of_form');
    }
}

steps['complete_report_middle_of_form'] = {
    'load': function () {
        new_load ('complete_report_middle_of_form', 'complete_report_bottom_of_form');
    }
}

steps['complete_report_bottom_of_form'] = {
    'load': function () {
        new_load ('complete_report_bottom_of_form', 'complete_report_nice_work');
    }
}

steps['complete_report_nice_work'] = {
    'load': function () {
        new_load ('complete_report_nice_work', 'complete_report_expert');
    }
}

steps['complete_report_expert'] = {
    'load': function () {
        new_load ('complete_report_expert', 'case_summary');
    }
}
