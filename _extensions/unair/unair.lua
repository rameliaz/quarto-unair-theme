-- Passes data from the build to theme.html, which reads it back from <meta>
-- tags. JavaScript in an include-after-body file can't see document metadata
-- or the extension's own folder directly.
--
-- 1. The optional `short-title` YAML field, used to label the right-hand
--    brand sidebar. Usage (YAML header): short-title: "Open Science in Psychology"
-- 2. The two logos, embedded as data URIs. Loading them by path would break
--    whenever the rendered page doesn't sit next to `_extensions/` (a deck in a
--    subfolder, `output-dir`, `embed-resources`), since `_extensions/` is
--    never copied to the output.

local function escape_attr(s)
  return (s:gsub('&', '&amp;'):gsub('"', '&quot;'):gsub('<', '&lt;'):gsub('>', '&gt;'))
end

local function logo_data_uri(file)
  local f = io.open(quarto.utils.resolve_path(file), 'rb')
  if not f then
    quarto.log.warning('unair: could not read ' .. file .. '; slides that use it will have no logo')
    return nil
  end
  local bytes = f:read('a')
  f:close()
  return 'data:image/png;base64,' .. quarto.base64.encode(bytes)
end

function Meta(meta)
  if not quarto.doc.is_format('revealjs') then
    return meta
  end

  if meta['short-title'] then
    local short_title = pandoc.utils.stringify(meta['short-title'])
    if short_title ~= '' then
      quarto.doc.include_text('in-header',
        '<meta name="unair-short-title" content="' .. escape_attr(short_title) .. '">')
    end
  end

  for name, file in pairs({ ['unair-logo'] = 'logo.png', ['unair-logo-white'] = 'logo_white.png' }) do
    local uri = logo_data_uri(file)
    if uri then
      quarto.doc.include_text('in-header', '<meta name="' .. name .. '" content="' .. uri .. '">')
    end
  end

  return meta
end
