" script encoding
scriptencoding utf-8

" load control
if exists('g:loaded_qiitapy')
    finish
endif
let g:loaded_qiitapy = 1

" evacuate user setting temporarily
let s:save_cpo = &cpo
set cpo&vim

" commands
command! -nargs=+ QiitaPy call qiitapy#qiitapy(<f-args>)

" restore user setting
let &cpo = s:save_cpo
unlet s:save_cpo

