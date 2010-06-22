

fieldz = [ ];



steps['complete_report'] = {
    'load': function () {
        new_load ('complete_report', 'case_summary');
        connect ( $('show_expert_form'), 'onclick', function (a) {
            showElement ($$('.report_form.expert_form')[0]);
        });
        //L = Math.round(getElementPosition( $('scrolling_ldss_form')).x)
        //T = Math.round(getElementPosition( $('scrolling_ldss_form')).y)
        //W = getElementDimensions( $('scrolling_ldss_form')).w
        //H = getElementDimensions( $('scrolling_ldss_form')).h
        
        
        // hard-coding these: otherwise cross-browser rendering details mess up the names of the fields
        L = 226;
        T = 195; 
        W = 650;
        H = 870;
        
        for (i = L; i < L + W; i += 60) {
            for (j = T; j < (T + H  - 20) ; j += 20) {
                fieldz.push ( [ i, j ] );
            }
        }
        map (magic_field, fieldz);
        connect  ('show_expert_form', 'onclick', toggle_expert_form);
    }
    
}



function show_expert_form() {

    map (hideElement , $$('.positioner_div'))
    updateNodeAttributes($('scrolling_ldss_form'), {'style': { 'background-image': 'url(/site_media/img/expert_ldss.png)'}});
    $('show_or_hide').innerHTML = "Hide"
}

function hide_expert_form () {
    map (showElement , $$('.positioner_div'))
    updateNodeAttributes($('scrolling_ldss_form'), {'style': { 'background-image': 'url(/site_media/img/ldss.png)'}});
    $('show_or_hide').innerHTML = "Show"
}

function toggle_expert_form() {
    if ( $('show_or_hide').innerHTML == 'Show') {
        show_expert_form();
    }
    else {
        hide_expert_form();
    }
}


function magic_field ( params ){
    //return 
    
    field_id = 'form_pre_field_' + params[0] + '_' + params[1];
    
    val = (game_state[field_id] == undefined) ? '': game_state[field_id] ;
    logDebug (field_id);
    new_div =  DIV ( { 'class' : 'positioner_div' }, 
    PRE({
                'id' : field_id,
                'contenteditable':'true',
                'class':'magic_form'
            },
            val)
    );
   $('magic_fields_go_here').appendChild(new_div);   
   params = {'style':
        {'left':  (params[0]  + 'px'),
         'top':   (params[1]  + 'px' ),
         'width': '60px',
         'height':'20px'
        }}
   updateNodeAttributes(new_div, params  );
}


