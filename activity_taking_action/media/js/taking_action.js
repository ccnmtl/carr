
//default_step = 'review_case_history';
default_step = 'complete_report';
game_state = {}


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
     setStyle('next', {'display': 'inline'});
     logDebug ('you can go');
     showElement($('conclusion'));
     hideElement ($('span_conclusion'));
   }
  else {
     setStyle('next', {'display': 'none'});
     logDebug ('you cant go');
     hideElement($('conclusion'));
     showElement ($('span_conclusion'));
  }
}

function validate() {
    if (filter(function (a) { return a.substring (0, 14) == 'form_pre_field' }, keys(game_state)).length > 0) {
      return true
    }
    if (filter (function(a) {return (a.innerHTML.trim() != '')}, $$('.magic_form') ).length > 0) {
      return true;
    }
  return false;
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
    maybeEnableNext();
}




function loadStateSuccess(doc)
{
  game_state = doc;
  
  debug('loadStateSuccess')
  logDebug (serializeJSON(doc));
  //
 
  //current_step = doc['current_step'] || default_step;
  current_step = default_step;
  load_step (current_step)
  
  //map (hideElement, $$('.activity_step'))
  if (hide_expert_form_toggle_button) {
     hideElement($('show_expert_form'));
  }
}

function loadStateError(err)
{
   debug("loadStateError")
   // @todo: Find a spot to display an error or decide just to fail gracefully
   // $('errorMsg').innerHTML = "An error occurred loading your state (" + err + "). Please start again."
}


function loadState()
{
    if (typeof student_response != "undefined") {
        logDebug ("Student answer found.");
        game_state = student_response;
        current_step = "complete_report"
        load_step ("complete_report")
        return;
    }


   //debug("loadState")
   url = 'http://' + location.hostname + ':' + location.port + "/activity/taking_action/load/"
   deferred = loadJSONDoc(url)
   deferred.addCallbacks(loadStateSuccess, loadStateError)
   
  maybeEnableNext();  
}


function like_checkbox(selected_class, all_button_class, the_element) {
    map (function(a) {removeElementClass( a,selected_class);}, $$('.' + all_button_class))
    addElementClass( $(the_element), selected_class);
}




function show_answer() {
      maybeEnableNext();
}


MochiKit.Signal.connect(window, "onload", loadState)
//MochiKit.Signal.connect(window, "onload", setfocus)



function ldss_form_fields_to_save () {
    results = {}
    filled_out_fields = filter (function (a) { return a.innerHTML != '';}, $$('.magic_form'))
    //logDebug (filled_out_fields);
    map( function (a) {results[a.id] = a.innerHTML}, filled_out_fields);
    return results;
}


function saveState()
{
  if (typeof student_response != "undefined") {
      return;      
  }
  url = 'http://' + location.hostname + ':' + location.port + "/activity/taking_action/save/"

  doc = ldss_form_fields_to_save()
   
  if (validate()) {
       doc['complete'] = 'true' 
  }
  
  doc ['current_step'] = current_step;
  
  var sync_req = new XMLHttpRequest();  
  sync_req.onreadystatechange= function() { if (sync_req.readyState!=4) return false; }         
  sync_req.open("POST", url, false);
    
  sync_req.send(queryString({'json':JSON.stringify(doc , null)}));
   
}


MochiKit.Signal.connect(window, "onbeforeunload", saveState)
