(
 (include_directive
   filenames: (list (word) @path)
   ) @include
 (#match? @include "^include")
 )
; ex: filetype=query
