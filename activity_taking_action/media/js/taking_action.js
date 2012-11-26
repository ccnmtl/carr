
//default_step = 'review_case_history';
//default_step = 'complete_report_nice_work';


default_step = 'complete_report_expert';


//default_step = 'complete_report_overview';
//default_step = 'complete_report_overview';
//default_step = 'complete_report_top_of_form';
//default_step = 'complete_report_bottom_of_form';

game_state = {}


function debug(string)
{
    if (true) {
      log("DEBUG " + string)
    }
}


function maybeEnableNext()
{
  gonext = true;
   
   if (gonext){
     setStyle('next', {'display': 'inline'});
     showElement($('conclusion'));
     hideElement ($('span_conclusion'));
   }
  else {
     setStyle('next', {'display': 'none'});
     hideElement($('conclusion'));
     showElement ($('span_conclusion'));
  }
}

// filter (function (a) { return a.value != '';}, $$ ('.form_fields_are_editable .ldss_form_input'));

function validate() {

    // we have stored form info for this user:
    if (filter(function (a) { return a.substring (0, 16) == '.ldss_form_input' }, keys(game_state)).length > 0) {
      return true
    }
    // OR the user has typed info into the form although it's not yet stored:
    if (filter (function(a) {return (a.value.trim() != '')}, $$('.form_fields_are_editable .ldss_form_input') ).length > 0) {
      return true;
    }
  return false;  
}





function loadStateSuccess(doc)
{
  game_state = doc;
  
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
        //logDebug ("Student answer found.");
        game_state = student_response;
        current_step = "complete_report"
        load_step ("complete_report")
        return;
   }
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

MochiKit.Signal.connect(window, "onload", loadState);
//MochiKit.Signal.connect(window, "onload", setfocus)

function new_ldss_form_fields_to_save() {
    results = {};
    filled_out_fields = filter (function (a) { return a.value != '';}, $$ ('.form_fields_are_editable .ldss_form_input'));
    map( function (a) {results[the_classlist(a)] = a.value}, filled_out_fields);
    return results;
}

function deprecated_ldss_form_fields_to_save () {
    results = {};
    filled_out_fields = filter (function (a) { return a.innerHTML != '';}, $$('.magic_form'));
    //logDebug (filled_out_fields);
    map( function (a) {results[a.id] = a.innerHTML}, filled_out_fields);
    return results;
}

function saveState()
{
  console.log ('saving state');
  if (typeof student_response != "undefined") {
      return;      
  }
  url = 'http://' + location.hostname + ':' + location.port + "/activity/taking_action/save/";

  //doc = ldss_form_fields_to_save();
  doc = new_ldss_form_fields_to_save();

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


