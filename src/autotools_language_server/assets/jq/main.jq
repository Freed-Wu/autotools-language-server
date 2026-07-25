$nodes[0].type as $type |
if $type == "macro_name" or ($complete and $type == "code") then
  .properties
else
  {}
end | to_entries[] |
if .key | ($nodes[0].text as $text | if $complete then startswith($text) else . == $text end) then
  {
    label: .key,
    insert_text: .key,
    kind: $enums.CompletionItemKind.Function,
    documentation: {kind: "markdown", value: .value.description}
  }
else
  empty
end
