---@type ChadrcConfig
local M = {}

M.ui = {
  theme = 'onedark',
  telescope = { style = "bordered" }
}

M.plugins = "custom.plugins"

M.mappings = require "custom.mappings"

return M
