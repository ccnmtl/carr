

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
  game_state = doc;
  
  debug('loadStateSuccess')
  logDebug (serializeJSON(doc));
  //default_step = 'review_case_history';
 
  current_step = doc['current_step'] || default_step;
  load_step (current_step)
  
  //map (hideElement, $$('.activity_step'))
  
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
   
  maybeEnableNext();
}


function like_checkbox(selected_class, all_button_class, the_element) {
    map (function(a) {removeElementClass( a,selected_class);}, $$('.' + all_button_class))
    addElementClass( $(the_element), selected_class);
}



function validate() {
    // make sure either yes or no is selected.
    /*
    return (
        hasElementClass($('answer_yes'), 'button_selected')
            || hasElementClass($('answer_no'), 'button_selected'));
            */
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

  
  debug("saveState")
  url = 'http://' + location.hostname + ':' + location.port + "/activity/taking_action/save/"

   debug("saveState");
   
   doc = ldss_form_fields_to_save()
   doc ['current_step'] = current_step;

   
   logDebug (serializeJSON(doc))
  var sync_req = new XMLHttpRequest();  
  sync_req.onreadystatechange= function() { if (sync_req.readyState!=4) return false; }         
  sync_req.open("POST", url, false);
  
    
  sync_req.send(queryString({'json':JSON.stringify(doc , null)}));
   
}

MochiKit.Signal.connect(window, "onbeforeunload", saveState)
