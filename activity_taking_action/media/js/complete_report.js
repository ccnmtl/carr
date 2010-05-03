steps['complete_report'] = {
    'load': function () {
        new_load ('complete_report', 'case_summary');
        connect ( $('show_expert_form'), 'onclick', function (a) {
            logDebug ('hey');
            showElement ($$('.report_form.expert_form')[0]);
        });
    }
}
