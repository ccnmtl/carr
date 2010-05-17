fieldz = [
    [0,0],
    [10, 0],
    [20, 0]
];

steps['complete_report'] = {
    'load': function () {
        new_load ('complete_report', 'case_summary');
        connect ( $('show_expert_form'), 'onclick', function (a) {
            showElement ($$('.report_form.expert_form')[0]);
        });
        
        
    }
}



function magic_field ( params ){
    return PRE({'contenteditable':'true', 'class':'magic_form'})

}
