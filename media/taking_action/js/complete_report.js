
/* NO LONGER USED */
fieldz = [ ];



steps['complete_report'] = {
    'load': function () {
    
        // CHANGING THIS:
        //new_load ('complete_report', 'case_summary');
        
        new_load ('complete_report', 'complete_report_overview');
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
        
        // if the 
        form_already_filled_out = false;
        form_already_filled_out = validate();
        
        make_fields_editable = !form_already_filled_out;
        
        if (make_fields_editable) {
          map (magic_field_editable,     fieldz);
        } else {
          map (magic_field_not_editable, fieldz);
       
        }      
        
        connect  ('show_expert_form', 'onclick', toggle_expert_form);
    }
    
}



function show_expert_form() {
    map (hideElement , $$('.positioner_div'))
    updateNodeAttributes($('scrolling_ldss_form'), {'style': { 'background-image': 'url(/media/img/expert_ldss.png)'}});
    $('show_or_hide').innerHTML = "Hide"
}

function hide_expert_form () {
    map (showElement , $$('.positioner_div'))
    updateNodeAttributes($('scrolling_ldss_form'), {'style': { 'background-image': 'url(/media/img/ldss.png)'}});
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


function magic_field_editable ( params ) {
    magic_field ( params, true);
}

function magic_field_not_editable ( params ) {
    magic_field ( params, false);
}


function magic_field ( params, editable ){
    //return 
    
    if (editable) {
        contenteditable_str = 'true';
    }
    else {
        contenteditable_str = 'false';    
    }
    
    field_id = 'form_pre_field_' + params[0] + '_' + params[1];
    
    val = (game_state[field_id] == undefined) ? '': game_state[field_id] ;
    //logDebug (field_id);
    if (val != '') {
        val = htmlDecode (val)
    }
    
    new_div =  DIV ( { 'class' : 'positioner_div' }, 
    PRE({
                'id' : field_id,
                'contenteditable':contenteditable_str,
                'class':'magic_form'
            },
            val
            )
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

// see http://stackoverflow.com/questions/1912501/unescape-html-entities-in-javascript
// for this recipe.
function htmlDecode(input){
  var e = document.createElement('div');
  e.innerHTML = input;
  return e.childNodes.length === 0 ? "" : e.childNodes[0].nodeValue;
}

