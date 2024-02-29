(define_directive
  name: (word) @function.def
  ) @function

(variable_assignment
  name: (word) @variable.def
  ) @variable

(rule
  (targets
    (word) @rule.def
    )
  normal: (prerequisites
            (word) @rule.call
            )
  ) @rule

(function_call
  (arguments
    argument: (text) @function.arg
    )
  )

(variable_reference
  (word) @variable.call
  )
