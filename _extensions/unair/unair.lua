-- Exposes the optional `short-title` YAML field to theme.html, which reads it
-- back from a <meta> tag to label the right-hand brand sidebar. JavaScript in
-- an include-after-body file can't see document metadata directly.
-- Usage (YAML header): short-title: "Open Science in Psychology"

local function escape_attr(s)
  return (s:gsub('&', '&amp;'):gsub('"', '&quot;'):gsub('<', '&lt;'):gsub('>', '&gt;'))
end

function Meta(meta)
  if meta['short-title'] then
    local short_title = pandoc.utils.stringify(meta['short-title'])
    if short_title ~= '' then
      quarto.doc.include_text('in-header',
        '<meta name="unair-short-title" content="' .. escape_attr(short_title) .. '">')
    end
  end
  return meta
end
