" Configuration file for vim
set modelines=0		" CVE-2007-2438

" Normally we use vim-extensions. If you want true vi-compatibility
" remove change the following statements
set nocompatible	" Use Vim defaults instead of 100% vi compatibility
set backspace=2		" more powerful backspacing

" Don't write backup file if vim is being called by "crontab -e"
au BufWrite /private/tmp/crontab.* set nowritebackup nobackup
" Don't write backup file if vim is being called by "chpass"
au BufWrite /private/etc/pw.* set nowritebackup nobackup

set number
set relativenumber
set cursorline
set wrap
set linebreak

set showmatch
set hlsearch
set incsearch

set laststatus=2
set ruler
set showmode
set showcmd
set encoding=utf-8
set t_Co=256

syntax on
filetype indent on
filetype on

" indent
set autoindent
set tabstop=4
set shiftwidth=4
set expandtab
set softtabstop=4
