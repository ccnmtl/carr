APP=carr
JS_FILES=media/js/quiz/ media/taking_action/js media/bruise_recon/js media/js/dragdropreorder.js
MAX_COMPLEXITY=7

all: eslint jenkins

include *.mk
