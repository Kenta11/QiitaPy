" script encoding
scriptencoding utf-8

" load control
if !exists('g:loaded_qiitapy')
    finish
endif
let g:loaded_qiitapy = 1

" evacuate user setting temporarily
let s:save_cpo = &cpo
set cpo&vim

python3 import sys
python3 import vim
python3 sys.path.append(vim.eval('expand("<sfile>:h:h")') + "/src/python3")
py3file <sfile>:h:h/src/python3/qiitapy.py

function qiitapy#qiitapy(command)
    python3 qiitaPy(vim.eval("a:command"))
endfunction

" restore user setting
let &cpo = s:save_cpo
unlet s:save_cpo

