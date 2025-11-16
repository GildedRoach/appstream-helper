-- Some of these functions were taken from the Fedora fonts packaging scripts
-- not installed at the moment, we currently inline everything
-- in the macro defs
-- TODO: Refactor to use this module in the future
local macrodefs = {
    appstream_id = "appstream_id",
    appstream_name_pretty = "appstream_name_pretty",
    appstream_component_type = "appstream_component_type",
}

local function get_macro(macro_name)
    local macro_value = rpm.expand("%{" .. macro_name .. "}")
    if macro_value == ("%%{" .. macro_name .. "}") then
        return nil
    end
    return macro_value
end

return {
    macrodefs = macrodefs,
}