" script encoding
scriptencoding utf-8

" load control
if exists('g:loaded_QiitaPy')
    finish
endif
let g:loaded_QiitaPy = 1

" evacuate user setting temporarily
let s:save_cpo = &cpo
set cpo&vim

" commands
command! -nargs=+ -complete=customlist,QiitaPy#commandList QiitaPy call QiitaPy#QiitaPy(<f-args>)

" restore user setting
let &cpo = s:save_cpo
unlet s:save_cpo

