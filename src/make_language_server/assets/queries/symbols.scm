; Document symbols query for Makefiles
; Captures targets (rules), variables, and define directives (functions)

; Targets/Rules
(rule
  (targets
    (word) @target.name
    )
  ) @target

; Variable assignments
(variable_assignment
  name: (word) @variable.name
  ) @variable

; Define directives (multi-line functions/macros)
(define_directive
  name: (word) @function.name
  ) @function
