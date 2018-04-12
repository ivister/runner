" user : an
" version : v0.5 (2016_03_31)

" common
"================================
set nocompatible

" Enable filetype plugins
filetype on
filetype plugin on

set wrap "split line
set linebreak

" Turn backup off, since most stuff is in SVN, git etc anyway
set nobackup
set nowb
set noswapfile

" No annoying sound on errors
set noerrorbells
set novisualbell "Не мигать
set t_vb= "Не пищать!
set tm=500 " time out in milliseconds

set lazyredraw " Don't redraw while executing macros (good performance)

" usual backspace
set backspace=indent,eol,start whichwrap+=<,>,[,]

set encoding=utf-8 " default encoding
set fileencodings=utf8,cp1251 "other possible encodings

set foldcolumn=1 " column for hidden code blocks

" show $ sign while change ("cw", "shift+c")
set cpoptions+=$

" tabs
"================================
set tabstop=4 " 1 tab == 4 spaces
set shiftwidth=4
set smarttab " Be smart when using tabs ;)
set expandtab " Use spaces instead of tabs
set softtabstop=4
set showtabline=0 " Вырубаем черточки на табах

set autoindent

" Useful funcs
"================================
" Autocomplete by tab (from wiki)
function! InsertTabWrapper(direction)
    let col = col('.') - 1
    if !col || getline('.')[col - 1] !~ '\k'
        return "\<tab>"
    elseif "backward" == a:direction
        return "\<c-p>"
    else
        return "\<c-n>"
    endif
 endfunction
 inoremap <tab> <c-r>=InsertTabWrapper ("forward")<cr>
 inoremap <s-tab> <c-r>=InsertTabWrapper ("backward")<cr>
set complete=""
set complete+=.
set complete+=k
set complete+=b
set complete+=t

" start on line before close
au BufReadPost * if line("'\'") > 0 | if line("'/'") <= line("$") | exe("norm '\"") | else | exe "norm $" | endif| endif

" Returns true if paste mode is enabled
function! HasPaste()
    if &paste
        return 'PASTE MODE  '
    endif
    return ''
endfunction

" python
"================================
" highlight everything
let python_highlight_all = 1

" omnicomletion for Python (and js, html, css)
autocmd FileType python set omnifunc=pythoncomplete#Complete

" Delete trailing whitespace on save (only .py files)
autocmd BufWritePre *.py normal m`:%s/\s\+$//e ``

"В .py файлах включаем умные отступы после ключевых слов
autocmd BufRead *.py set smartindent cinwords=if,elif,else,for,while,try,except,finally,def,class


" maps
"================================
map <F2> :w<cr>
imap <F2> <esc>:w<cr>:star<cr>
" for C/C++
" compile current file
map <F3> :w<cr>:!gcc -Wall -o %< % <cr>
imap <F3> <esc>:w<cr>:!gcc -Wall -o %< % <cr>:star<cr>
" execute binary for current file
map <F4> :!./%< <cr>
imap <F4> <esc>:!./%< <cr>

map <F10> :wq<cr>
imap <F10> <esc>:wq<cr>

" Map <Space> to / (search) and Ctrl-<Space> to ? (backwards search)
map <space> /
map <c-space> ?

" map for Russian hotkeys
" mapping it (after it can switch ru-en with ctrl+^ mean ctrl+shift+6)
set keymap=russian-jcukenwin
set iminsert=0
set imsearch=0

" search
"================================
set hlsearch " Highlight search results
set incsearch " Makes search act like search in modern browsers
set smartcase " When searching try to be smart about cases
set ignorecase " Ignore case when searching

" colorscheme
"================================
syntax on
"colorscheme solarized
try
    colorscheme desert
catch
endtry

set background=dark

set number "enable line count
highlight LineNr term=bold cterm=NONE ctermfg=DarkGrey ctermbg=NONE gui=NONE guifg=DarkGrey guibg=NONE

" change cursor color for Russian locale
" works with GUI only
" to get last place where cursor changed type
" :verbose :hi :lCursor
highlight lCursor guifg=NONE guibg=Cyan

" info line
set viminfo='10,\"100,:20,%,n~/.viminfo

"Always show current position
set ruler

" For regular expressions turn magic on
"set magic

" In many terminal emulators the mouse works just fine, thus enable it.
if has('mouse')
  set mouse=a
endif

" useful configs:
" https://github.com/amix/vimrc/blob/master/vimrcs/basic.vim
