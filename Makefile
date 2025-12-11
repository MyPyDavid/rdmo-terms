COMMANDS = build index elements element static assets clean serve

.PHONY: $(COMMANDS)

$(COMMANDS):
	rdmo-terms $@
