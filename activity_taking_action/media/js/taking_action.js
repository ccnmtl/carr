function debug(string)
{
    if (false)
      log("DEBUG " + string)
}


function maybeEnableNext()
{
   gonext = false
 
   if (validate()) {
    gonext = true;
   }
   
   if (gonext){
         setStyle('next', {'display': 'inline'}) 
   }
  else
  {
     setStyle('next', {'display': 'none'}) 
  }
}

function load_step (step_name) {
    logDebug ("loading " + step_name);
    map (hideElement, $$('.activity_step'))
    showElement($$('div#' + step_name +  '.activity_step')[0] );
    if (steps[step_name] != undefined) {
        steps[step_name].load()
    }
    else {
        logDebug("not defined.");
    }
}




function loadStateSuccess(doc)
{
  debug('loadStateSuccess')
  logDebug (serializeJSON(doc));
  default_step = 'review_case_history';
 //default_step = 'next_steps';
  
  current_step = doc['current_step'] || default_step;
  load_step (current_step)
  
  //map (hideElement, $$('.activity_step'))
   
  /*
  case_name =  $('case_name').innerHTML;
   
   if (doc && doc[case_name])
   {
    state_for_this_page = doc[case_name];
    logDebug (serializeJSON(state_for_this_page));
   }
   if (state_for_this_page['answered']) {
        if (state_for_this_page['answered'] == 'yes') {
            addElementClass($('answer_yes'), 'button_selected');
        }
        else if (state_for_this_page['answered'] == 'no') {
            addElementClass($('answer_no'), 'button_selected');
        }
    }
   if (state_for_this_page['factors']) {
        factors_as_string = state_for_this_page['factors'].join (',');
        logDebug (factors_as_string); 
   }
   if (factors_as_string.match(/patterns/) != null) {
            addElementClass($('patterns'), 'button_selected');
   }
   if (factors_as_string.match(/severity/) != null) {
            addElementClass($('severity'), 'button_selected');
   }
   if (factors_as_string.match(/location/) != null) {
            addElementClass($('location'), 'button_selected');
   }
   if (factors_as_string.match(/explanation/) != null) {
            addElementClass($('explanation'), 'button_selected');
   }
   */
   
  maybeEnableNext()
}

function loadStateError(err)
{
   debug("loadStateError")
   // @todo: Find a spot to display an error or decide just to fail gracefully
   // $('errorMsg').innerHTML = "An error occurred loading your state (" + err + "). Please start again."
}



function loadState()
{
   debug("loadState")
   url = 'http://' + location.hostname + ':' + location.port + "/activity/taking_action/load/"
   deferred = loadJSONDoc(url)
   deferred.addCallbacks(loadStateSuccess, loadStateError)
   
   /*
   hide_answer();
   
   
  connect ('answer_yes', 'onclick', partial (like_checkbox, 'button_selected', 'answer_button', 'answer_yes'))
  connect ('answer_no',  'onclick', partial (like_checkbox, 'button_selected', 'answer_button', 'answer_no'))
  
  
  connect ('patterns',      'onclick', partial (toggleElementClass,'button_selected',    'patterns' ));
  connect ('severity',      'onclick', partial (toggleElementClass,'button_selected',    'severity' ));
  connect ('location',      'onclick', partial (toggleElementClass,'button_selected',    'location' ));
  connect ('explanation',   'onclick', partial (toggleElementClass,'button_selected',    'explanation' ));

  connect('submit_div', 'onclick', show_answer);
 */
  maybeEnableNext();
}


function like_checkbox(selected_class, all_button_class, the_element) {
    map (function(a) {removeElementClass( a,selected_class);}, $$('.' + all_button_class))
    addElementClass( $(the_element), selected_class);
}


//toggleElement
function hide_answer()
{
    //hideElement('feedback_div');
/*
   if (!$('dosage_correct'))
      $("dosage").focus()
      */
}


function numeric(field) {
    var regExpr = new RegExp("^[0-9]$");
    if (!regExpr.test(field.value)) 
    {
      // Case of error
      field.value = "";
    }
}

function validate() {
    // make sure either yes or no is selected.
    /*
    return (
        hasElementClass($('answer_yes'), 'button_selected')
            || hasElementClass($('answer_no'), 'button_selected'));
            */
}


function answer_is_correct() {
   
    /*
    answer_is_yes = ($('correct_answer').innerHTML.toLowerCase().match(/yes/))
    factors_include_severity = ($('correct_factors').innerHTML.toLowerCase().match(/severity/))
    factors_include_location = ($('correct_factors').innerHTML.toLowerCase().match(/location/))
    factors_include_patterns = ($('correct_factors').innerHTML.toLowerCase().match(/patterns/))
    factors_include_explanation = ($('correct_factors').innerHTML.toLowerCase().match(/explanation/))
    
    if (answer_is_yes) {
        if (hasElementClass($('answer_no'), 'button_selected')) { return false };
    }
    else {
        if (hasElementClass($('answer_yes'), 'button_selected')) { return false };
    }
    
    logDebug ("yes no answer is correct");
    if (factors_include_severity) {
        if (! hasElementClass($('severity'), 'button_selected')) { return false };
    }
    if (factors_include_location) {
        if (! hasElementClass($('location'), 'button_selected')) { return false };
    }
    if (factors_include_patterns) {
        if (! hasElementClass($('patterns'), 'button_selected')) { return false };
    }
    if (factors_include_explanation) {
        if (! hasElementClass($('explanation'), 'button_selected')) { return false };
    }
    */
    //patterns, severity, body location, explanation credibility
    logDebug ("ok factors are correct too");
    return true;

}

function show_answer() {
/*
    if (!validate()) {
        alert ("Please choose yes or no.");
        return;
    }
    hideElement ('submit_div');
    if (answer_is_correct()) {
        $("your_answer_was").innerHTML = "Your answer is correct.";
    }
    else {
        $("your_answer_was").innerHTML = "Your answer is incorrect.";
    
    }
    showElement ('feedback_div');
  */  
      maybeEnableNext();
}


MochiKit.Signal.connect(window, "onload", loadState)
//MochiKit.Signal.connect(window, "onload", setfocus)

function saveState()
{
/*
  case_name =  $('case_name').innerHTML;
  
  debug("saveState")
  url = 'http://' + location.hostname + ':' + location.port + "/activity/taking_action/save/"

   debug("saveState");
   doc = {}
   
   if (hasElementClass($('answer_yes'), 'button_selected'))
   {
        doc ['answered'] = 'yes';
   } else {
        doc ['answered'] = 'no';
   }
   
   doc ['factors'] = []
   if (hasElementClass($('severity'),    'button_selected')) { doc ['factors'].push (   'severity') };
   if (hasElementClass($('location'),    'button_selected')) { doc ['factors'].push (   'location') };
   if (hasElementClass($('patterns'),    'button_selected')) { doc ['factors'].push (   'patterns') };
   if (hasElementClass($('explanation'), 'button_selected')) { doc ['factors'].push ('explanation') };
   
   
   
  var sync_req = new XMLHttpRequest();  
  sync_req.onreadystatechange= function() { if (sync_req.readyState!=4) return false; }         
  sync_req.open("POST", url, false);
  
  what_to_send = {}
  what_to_send [case_name ] = doc
  
  
  sync_req.send(queryString({'json':JSON.stringify(what_to_send , null)}));
   */
}

MochiKit.Signal.connect(window, "onbeforeunload", saveState)
