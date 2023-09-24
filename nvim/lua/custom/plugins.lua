local plugins = {
  {
    "nvim-treesitter/nvim-treesitter",
    opts = {
      ensure_installed = {
        "c",
        "c_sharp",
        "cpp",
        "java",
        "python",
        "rust"
      }
    }
  },
  {
    "williamboman/mason.nvim",
    opts = {
      ensure_installed = {
        "pyright"
      }
    }
  },
  {
    "neovim/nvim-lspconfig",
    config = function()
      require "plugins.configs.lspconfig"
      require "custom.configs.lspconfig"
    end
  },
  {
    "github/copilot.vim",
    event = "VimEnter",
    config = function()
      -- Tab mapping is already used by NvChad
      vim.g.copilot_no_tab_map = true
      vim.g.copilot_assume_mapped = true
      vim.g.copilot_tab_fallback = ""
      -- The new mapping is set to another key in lua/custom/mappings
    end
  }
}

return plugins
