" script encoding
scriptencoding utf-8

" load control
if !exists('g:loaded_QiitaPy')
    finish
endif
let g:loaded_QiitaPy = 1

" evacuate user setting temporarily
let s:save_cpo = &cpo
set cpo&vim

python3 import sys
python3 sys.path.append(vim.eval('expand("<sfile>:h:h")') + "/src/python3")
py3file <sfile>:h:h/src/python3/QiitaPy.py

function! QiitaPy#QiitaPy(...)
    let option = (a:0 >= 2) ? a:000[1:] : []
    python3 qiitaPy(vim.eval("a:1"), vim.eval("option"))
endfunction

function! QiitaPy#commandList(lead, line, pos)
    return ["config", "post", "list", "edit", "template"]
endfunction

" restore user setting
let &cpo = s:save_cpo
unlet s:save_cpo

