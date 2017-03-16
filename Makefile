APP=carr
JS_FILES=media/js/quiz/ media/taking_action/js media/bruise_recon/js media/js/dragdropreorder.js media/js/hs.js
MAX_COMPLEXITY=7

all: jenkins

include *.mk

eslint: $(JS_SENTINAL)
	$(NODE_MODULES)/.bin/eslint $(JS_FILES)

.PHONY: eslint
